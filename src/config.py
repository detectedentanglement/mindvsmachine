"""
Configuration settings for Mind vs Machine RNG
"""

# Default RNG settings
DEFAULT_MIN_VALUE = 0
DEFAULT_MAX_VALUE = 99

# Game modes
GAME_MODES = {
    "exact_match": "Exact Match",
    "range_prediction": "Range Prediction",
    "high_low": "High/Low",
}

# RNG algorithms
RNG_ALGORITHMS = {
    "standard": "Standard Python Random",
    "secrets": "Cryptographic Random",
    "time_based": "Time-Based Seed",
}

# UI Settings
MAX_HISTORY_DISPLAY = 50
CHART_HEIGHT = 400

# Statistics settings
STAT_BINS = 10

# Special numbers (theme: 47)
SPECIAL_NUMBER = 47
SPECIAL_MINUTE = 47

# Color scheme
COLORS = {
    "success": "#00ff00",
    "failure": "#ff0000",
    "neutral": "#888888",
    "special": "#FFD700",
}

# Data persistence
DATA_DIR = "data"
SESSION_FILE = f"{DATA_DIR}/sessions.json"
EXPORT_DIR = f"{DATA_DIR}/exports"
