import os


def _env_bool(val):
    return val.lower() in ["1", "yes", "true", "t", "y"]


def env_snapshot_update():
    return _env_bool(os.environ.get("SNAPSHOT_UPDATE", "false"))
