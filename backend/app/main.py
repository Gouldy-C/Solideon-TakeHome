from database.db import test_db
import utils.config_loader as cfg
from pathlib import Path

path = Path(__file__).parent / "config/v0.1"
cfg.init_load(path)


def main() -> None:
    test_db()
    print(cfg.CONFIG["equations_vars"]["distance_a"])


if __name__ == "__main__":
    main()