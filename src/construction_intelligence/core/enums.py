from enum import StrEnum, auto


class ProjectOrigin(StrEnum):
    """Where a project was discovered."""

    OSM = "osm"
    WEB = "web"


class ConfidenceLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ProjectStatus(StrEnum):
    """Lifecycle state of a construction project."""

    PLANNED = auto()
    PERMITTED = auto()
    UNDER_CONSTRUCTION = auto()
    PAUSED = auto()
    COMPLETED = auto()
    CANCELLED = auto()


class ProjectCategory(StrEnum):
    """High-level type of construction project."""

    ROAD = auto()
    BRIDGE = auto()
    RAIL = auto()
    AIRPORT = auto()
    PORT = auto()
    BUILDING = auto()
    UTILITY = auto()
    OTHER = auto()