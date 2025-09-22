from pathlib import Path
from dynaconf import Dynaconf

BASE_DIR = Path(__file__).resolve().parent

CONF = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['env.toml', '.secrets.toml'],
    environments=True,
    root_path=BASE_DIR
)