"""
RNG Engine with multiple randomness algorithms
"""
import random
import secrets
import time
from datetime import datetime
from typing import Optional


class RNGEngine:
    """Random Number Generator with multiple algorithms"""

    def __init__(self, algorithm: str = "standard"):
        """
        Initialize RNG engine with specified algorithm

        Args:
            algorithm: One of 'standard', 'secrets', 'time_based'
        """
        self.algorithm = algorithm
        self.last_seed = None

    def generate(self, min_val: int, max_val: int) -> int:
        """
        Generate a random number using the selected algorithm

        Args:
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive)

        Returns:
            Random integer between min_val and max_val

        Raises:
            ValueError: If min_val > max_val
        """
        if min_val > max_val:
            raise ValueError(f"min_val ({min_val}) cannot be greater than max_val ({max_val})")

        try:
            if self.algorithm == "standard":
                return random.randint(min_val, max_val)

            elif self.algorithm == "secrets":
                # Cryptographically strong random
                return secrets.randbelow(max_val - min_val + 1) + min_val

            elif self.algorithm == "time_based":
                # Time-based seeded random (demonstrating "influence")
                seed = int(time.time() * 1000000) % 1000000
                self.last_seed = seed
                random.seed(seed)
                result = random.randint(min_val, max_val)
                random.seed()  # Reset to system time
                return result

            else:
                # Default fallback
                return random.randint(min_val, max_val)

        except Exception as e:
            # Fallback to standard random on any error
            print(f"Error in RNG generation: {e}")
            return random.randint(min_val, max_val)

    def get_algorithm_info(self) -> dict:
        """Get information about the current algorithm"""
        info = {
            "standard": {
                "name": "Standard Python Random",
                "description": "Mersenne Twister pseudo-random number generator",
                "predictable": True,
            },
            "secrets": {
                "name": "Cryptographic Random",
                "description": "Cryptographically strong random using OS entropy",
                "predictable": False,
            },
            "time_based": {
                "name": "Time-Based Seed",
                "description": "Seeded with microsecond-precision timestamp",
                "predictable": "Partially",
            },
        }
        return info.get(self.algorithm, info["standard"])

    @staticmethod
    def is_special_time() -> bool:
        """Check if current time is at the 47th minute (theme reference)"""
        return datetime.now().minute == 47


def validate_range(min_val: int, max_val: int) -> tuple[bool, Optional[str]]:
    """
    Validate min/max range

    Returns:
        Tuple of (is_valid, error_message)
    """
    if min_val > max_val:
        return False, f"Minimum ({min_val}) cannot be greater than maximum ({max_val})"

    if max_val - min_val < 1:
        return False, "Range must contain at least 2 numbers"

    if max_val - min_val > 10000:
        return False, "Range too large (max 10,000 numbers)"

    return True, None
