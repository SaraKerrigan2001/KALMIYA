import os
from decouple import Config, RepositoryEnv, UndefinedValueError

# Load .env from the KALMIYA_System directory
ENV_PATH = os.path.join(os.path.dirname(__file__), '..', 'KALMIYA_System', '.env')
config = Config(RepositoryEnv(ENV_PATH))

REQUIRED_KEYS = [
    "BOTNAME",
    "KALMIYA_ENABLE_SERVER",
    "KALMIYA_SERVER_PORT",
    "KALMIYA_ENABLE_WALLPAPER",
]

def get_config(key: str, default=None):
    """Fetch a configuration value, raising a clear error if missing and no default provided."""
    try:
        return config(key, default=default)
    except UndefinedValueError:
        if default is not None:
            return default
        raise RuntimeError(f"Missing required configuration key: {key}")

def validate_all():
    """Validate that all required keys are present. Raises RuntimeError on failure."""
    missing = []
    for key in REQUIRED_KEYS:
        try:
            _ = config(key)
        except UndefinedValueError:
            missing.append(key)
    if missing:
        raise RuntimeError(f"Configuration validation failed – missing keys: {', '.join(missing)}")
    return True
