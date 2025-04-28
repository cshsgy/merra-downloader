import os
from dotenv import load_dotenv
from typing import Dict, Any
import json

class Config:
    def __init__(self, config_file: str = "config.json"):
        load_dotenv()
        self.username = os.getenv("MERRA_USERNAME")
        self.password = os.getenv("MERRA_PASSWORD")
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "time_range": {
                    "start": "2020-01-01",
                    "end": "2020-01-31"
                },
                "box": {
                    "north": 90,
                    "south": -90,
                    "east": 180,
                    "west": -180
                },
                "variables": ["O3", "CO", "NO2"],
                "product": "M2I3NPASM"
            }

    def save_config(self, config: Dict[str, Any]):
        """Save configuration to JSON file."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
        self.config = config

    def get_credentials(self) -> tuple:
        """Get MERRA credentials."""
        if not self.username or not self.password:
            raise ValueError("MERRA credentials not found. Please set MERRA_USERNAME and MERRA_PASSWORD environment variables.")
        return self.username, self.password 