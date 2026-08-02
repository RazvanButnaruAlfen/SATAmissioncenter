from enum import Enum, auto


class ScannerState(Enum):
    IDLE = auto()
    CONNECTING = auto()
    SEARCHING = auto()
    TARGET_FOUND = auto()
    STABILIZING = auto()
    SCANNING = auto()
    ANALYZING = auto()
    RESULT = auto()
