from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


# Gateway defaults
DEFAULT_TIMEOUT_MS = 60000
MAX_RETRIES = 3
DEFAULT_CACHE_TTL = 300
