"""
Analytics and statistics module for Mind vs Machine RNG
"""
from collections import Counter
from datetime import datetime
from typing import List, Dict, Optional
import json
import os


class GameSession:
    """Represents a single game attempt"""

    def __init__(
        self,
        prediction: Optional[int],
        generated: int,
        timestamp: Optional[str] = None,
        game_mode: str = "exact_match",
        min_val: int = 0,
        max_val: int = 99,
        algorithm: str = "standard",
    ):
        self.prediction = prediction
        self.generated = generated
        self.timestamp = timestamp or datetime.now().isoformat()
        self.game_mode = game_mode
        self.min_val = min_val
        self.max_val = max_val
        self.algorithm = algorithm

    def is_hit(self) -> bool:
        """Check if prediction matched generated number"""
        if self.prediction is None:
            return False
        return self.prediction == self.generated

    def distance(self) -> Optional[int]:
        """Calculate distance between prediction and generated number"""
        if self.prediction is None:
            return None
        return abs(self.prediction - self.generated)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "prediction": self.prediction,
            "generated": self.generated,
            "timestamp": self.timestamp,
            "game_mode": self.game_mode,
            "min_val": self.min_val,
            "max_val": self.max_val,
            "algorithm": self.algorithm,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create GameSession from dictionary"""
        return cls(**data)


class Analytics:
    """Statistical analysis for game sessions"""

    def __init__(self, sessions: List[GameSession]):
        self.sessions = sessions

    def total_attempts(self) -> int:
        """Total number of attempts"""
        return len(self.sessions)

    def total_predictions(self) -> int:
        """Total number of attempts with predictions"""
        return len([s for s in self.sessions if s.prediction is not None])

    def total_hits(self) -> int:
        """Total number of exact matches"""
        return len([s for s in self.sessions if s.is_hit()])

    def hit_rate(self) -> float:
        """Percentage of exact matches"""
        predictions = self.total_predictions()
        if predictions == 0:
            return 0.0
        return (self.total_hits() / predictions) * 100

    def average_distance(self) -> Optional[float]:
        """Average distance from prediction"""
        distances = [s.distance() for s in self.sessions if s.distance() is not None]
        if not distances:
            return None
        return sum(distances) / len(distances)

    def number_frequency(self) -> Dict[int, int]:
        """Frequency of each generated number"""
        return dict(Counter(s.generated for s in self.sessions))

    def hot_numbers(self, top_n: int = 5) -> List[tuple]:
        """Most frequently generated numbers"""
        freq = self.number_frequency()
        return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def cold_numbers(self, top_n: int = 5, min_val: int = 0, max_val: int = 99) -> List[int]:
        """Least frequently generated numbers"""
        freq = self.number_frequency()
        all_numbers = set(range(min_val, max_val + 1))
        generated_numbers = set(freq.keys())
        never_generated = all_numbers - generated_numbers

        # Return never generated first, then least frequent
        if len(never_generated) >= top_n:
            return sorted(list(never_generated))[:top_n]

        cold = sorted(freq.items(), key=lambda x: x[1])
        cold_nums = [num for num, _ in cold]
        return list(never_generated) + cold_nums[: top_n - len(never_generated)]

    def current_streak(self) -> int:
        """Current streak of hits"""
        streak = 0
        for session in reversed(self.sessions):
            if session.is_hit():
                streak += 1
            else:
                break
        return streak

    def longest_streak(self) -> int:
        """Longest streak of hits"""
        max_streak = 0
        current = 0
        for session in self.sessions:
            if session.is_hit():
                current += 1
                max_streak = max(max_streak, current)
            else:
                current = 0
        return max_streak

    def special_number_count(self, special_num: int = 47) -> int:
        """Count occurrences of special number"""
        return len([s for s in self.sessions if s.generated == special_num])

    def get_distribution_data(self, bins: int = 10) -> Dict[str, List]:
        """Get data for distribution chart"""
        generated_numbers = [s.generated for s in self.sessions]
        if not generated_numbers:
            return {"bins": [], "counts": []}

        min_num = min(generated_numbers)
        max_num = max(generated_numbers)
        bin_size = max(1, (max_num - min_num + 1) // bins)

        bin_edges = []
        bin_counts = []

        for i in range(bins):
            bin_start = min_num + i * bin_size
            bin_end = bin_start + bin_size - 1
            if i == bins - 1:
                bin_end = max_num

            count = len([n for n in generated_numbers if bin_start <= n <= bin_end])
            bin_edges.append(f"{bin_start}-{bin_end}")
            bin_counts.append(count)

        return {"bins": bin_edges, "counts": bin_counts}


class SessionManager:
    """Manage session data persistence"""

    def __init__(self, filepath: str = "data/sessions.json"):
        self.filepath = filepath
        self._ensure_directory()

    def _ensure_directory(self):
        """Create data directory if it doesn't exist"""
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def save_sessions(self, sessions: List[GameSession]) -> bool:
        """Save sessions to file"""
        try:
            data = [s.to_dict() for s in sessions]
            with open(self.filepath, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving sessions: {e}")
            return False

    def load_sessions(self) -> List[GameSession]:
        """Load sessions from file"""
        try:
            if not os.path.exists(self.filepath):
                return []

            with open(self.filepath, "r") as f:
                data = json.load(f)
                return [GameSession.from_dict(s) for s in data]
        except Exception as e:
            print(f"Error loading sessions: {e}")
            return []

    def export_to_csv(self, sessions: List[GameSession], output_path: str) -> bool:
        """Export sessions to CSV format"""
        try:
            import csv

            with open(output_path, "w", newline="") as f:
                if not sessions:
                    return True

                writer = csv.DictWriter(f, fieldnames=sessions[0].to_dict().keys())
                writer.writeheader()
                for session in sessions:
                    writer.writerow(session.to_dict())
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
