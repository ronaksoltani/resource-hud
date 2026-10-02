import argparse
import time

from rich.live import Live

from .monitor import Monitor, render


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Watch local CPU, memory, disk, and network metrics.")
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--iterations", type=int, default=60, help="0 runs until Ctrl+C")
    parser.add_argument("--disk", default="/", help="mount path to report")
    args = parser.parse_args(argv)
    if args.interval <= 0 or args.iterations < 0:
        parser.error("interval must be positive and iterations cannot be negative")
    monitor = Monitor(args.disk)
    count = 0
    try:
        with Live(render(monitor.sample()), refresh_per_second=4) as live:
            while args.iterations == 0 or count < args.iterations:
                live.update(render(monitor.sample()), refresh=True)
                count += 1
                time.sleep(args.interval)
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
