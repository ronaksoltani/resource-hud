from __future__ import annotations

import time
from dataclasses import dataclass

import psutil
from rich.table import Table


@dataclass(frozen=True)
class Snapshot:
    cpu_percent: float
    memory_percent: float
    memory_used: int
    memory_total: int
    disk_percent: float
    disk_used: int
    disk_total: int
    sent_per_second: float
    received_per_second: float


def format_bytes(amount: float) -> str:
    value = float(amount)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if abs(value) < 1024 or unit == "TiB":
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} TiB"


class Monitor:
    def __init__(self, disk_path: str = "/"):
        self.disk_path = disk_path
        self.previous_net = psutil.net_io_counters()
        self.previous_time = time.monotonic()

    def sample(self) -> Snapshot:
        current_net = psutil.net_io_counters()
        now = time.monotonic()
        elapsed = max(now - self.previous_time, 0.001)
        memory, disk = psutil.virtual_memory(), psutil.disk_usage(self.disk_path)
        result = Snapshot(psutil.cpu_percent(interval=None), memory.percent, memory.used, memory.total,
                          disk.percent, disk.used, disk.total,
                          (current_net.bytes_sent - self.previous_net.bytes_sent) / elapsed,
                          (current_net.bytes_recv - self.previous_net.bytes_recv) / elapsed)
        self.previous_net, self.previous_time = current_net, now
        return result


def render(snapshot: Snapshot) -> Table:
    table = Table(title="Resource HUD · live", expand=True)
    table.add_column("Resource", style="cyan")
    table.add_column("Usage", justify="right")
    table.add_column("Details", justify="right", style="dim")
    table.add_row("CPU", f"{snapshot.cpu_percent:.1f}%", "current sample")
    table.add_row("Memory", f"{snapshot.memory_percent:.1f}%",
                  f"{format_bytes(snapshot.memory_used)} / {format_bytes(snapshot.memory_total)}")
    table.add_row("Disk", f"{snapshot.disk_percent:.1f}%",
                  f"{format_bytes(snapshot.disk_used)} / {format_bytes(snapshot.disk_total)}")
    table.add_row("Network ↓", format_bytes(snapshot.received_per_second) + "/s", "received")
    table.add_row("Network ↑", format_bytes(snapshot.sent_per_second) + "/s", "sent")
    return table
