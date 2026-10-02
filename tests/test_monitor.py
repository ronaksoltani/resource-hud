from resource_hud.monitor import Snapshot, format_bytes, render


def test_byte_format_and_dashboard_rows():
    assert format_bytes(1024) == "1.0 KiB"
    snapshot = Snapshot(25.0, 50.0, 50, 100, 60.0, 60, 100, 10, 20)
    table = render(snapshot)
    assert table.row_count == 5


def test_large_byte_values_scale_to_binary_units():
    assert format_bytes(1024**2) == "1.0 MiB"
