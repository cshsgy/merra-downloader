import os
from dotenv import load_dotenv
from typing import Dict, Any
import json
from pathlib import Path

class Config:
    def __init__(self, config_file: str = "config.json"):
        # Load .env file from the same directory as config.py
        env_path = Path(__file__).parent / ".env"
        if not env_path.exists():
            raise FileNotFoundError(
                f"Credentials file not found at {env_path}. "
                "Please create a .env file with MERRA_USERNAME and MERRA_PASSWORD."
            )
        
        # Load environment variables from .env file
        load_dotenv(env_path)
        
        # Get credentials
        self.username = os.getenv("MERRA_USERNAME")
        self.password = os.getenv("MERRA_PASSWORD")
        
        # Validate credentials
        if not self.username or not self.password:
            raise ValueError(
                "MERRA credentials not found in .env file. "
                "Please ensure MERRA_USERNAME and MERRA_PASSWORD are set."
            )
        
        self.config_file = config_file
        self.config = self._load_config()
        self.base_url = "https://goldsmr5.gesdisc.eosdis.nasa.gov/opendap/MERRA2/"

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                
                # Validate required fields
                required_fields = ["time_range", "box", "variables", "product"]
                for field in required_fields:
                    if field not in config:
                        raise ValueError(f"Missing required field in config: {field}")
                
                # Validate time range format
                if not all(key in config["time_range"] for key in ["start", "end"]):
                    raise ValueError("time_range must contain 'start' and 'end' dates")
                
                # Validate box coordinates
                if not all(key in config["box"] for key in ["north", "south", "east", "west"]):
                    raise ValueError("box must contain 'north', 'south', 'east', and 'west' coordinates")
                
                return config
                
        except FileNotFoundError:
            print(f"Config file {self.config_file} not found. Using default configuration.")
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
                "product": "M2I3NPASM.5.12.4"
            }

    def save_config(self, config: Dict[str, Any]):
        """Save configuration to JSON file."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
        self.config = config

    def get_credentials(self) -> tuple:
        """Get MERRA credentials."""
        return self.username, self.password 