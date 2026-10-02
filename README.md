# Terminal Resource HUD

An updating terminal dashboard for CPU, memory, disk, and network counters using `psutil` and Rich. Run it for a fixed number of refreshes or stop it with Ctrl+C.

## Quick start

```bash
python -m venv .venv
python -m pip install -e .
resource-hud --interval 1 --iterations 60
```

Use `--iterations 0` to keep refreshing until interrupted. Network figures show bytes transferred since the previous sample, not a prediction of internet speed.

## Learning notes

This project practices polling APIs, elapsed-time calculations, formatting bytes, and using Rich `Live` to redraw a terminal table without printing an endless stream of rows.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## License

MIT. See [LICENSE](LICENSE).
