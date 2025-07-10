"""Configuration management module for MAT."""
import json
import os
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class ConfigData:
    """Data class for configuration settings."""
    selected_text: str = ""
    dropdown: str = ""
    radioMode: int = 0
    radioStylize: int = 0
    radioChaos: int = 0
    check_vars: Dict[str, int] = None
    window_x: int = 0
    window_y: int = 0
    window_width: int = 900
    window_height: int = 600
    theme: str = "dark"
    auto_save_interval: int = 10000
    
    def __post_init__(self):
        if self.check_vars is None:
            self.check_vars = {"1": 0, "2": 0, "3": 0, "4": 0}

class ConfigManager:
    """Manages application configuration with validation and error handling."""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self._default_config = ConfigData()
    
    def save_config(self, config_data: ConfigData) -> bool:
        """Save configuration to file with error handling."""
        try:
            config_dict = asdict(config_data)
            with open(self.config_path, 'w', encoding='utf-8') as file:
                json.dump(config_dict, file, indent=4)
            self.logger.info("Configuration saved successfully")
            return True
        except (IOError, json.JSONEncodeError) as e:
            self.logger.error(f"Failed to save configuration: {e}")
            return False
    
    def load_config(self) -> ConfigData:
        """Load configuration from file with fallback to defaults."""
        if not os.path.exists(self.config_path):
            self.logger.info("Config file not found, using defaults")
            return self._default_config
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config_dict = json.load(file)
            
            # Validate and merge with defaults
            validated_config = self._validate_config(config_dict)
            self.logger.info("Configuration loaded successfully")
            return ConfigData(**validated_config)
            
        except (IOError, json.JSONDecodeError, TypeError) as e:
            self.logger.error(f"Failed to load configuration: {e}")
            return self._default_config
    
    def _validate_config(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration data and provide defaults for missing values."""
        default_dict = asdict(self._default_config)
        
        # Merge with defaults
        for key, default_value in default_dict.items():
            if key not in config_dict:
                config_dict[key] = default_value
            elif key == "check_vars" and not isinstance(config_dict[key], dict):
                config_dict[key] = default_value
        
        # Validate ranges
        config_dict["radioMode"] = max(0, min(2, config_dict.get("radioMode", 0)))
        config_dict["radioStylize"] = max(0, min(5, config_dict.get("radioStylize", 0)))
        config_dict["radioChaos"] = max(0, min(4, config_dict.get("radioChaos", 0)))
        
        return config_dict
