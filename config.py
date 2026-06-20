"""
J.A.R.V.I.S Configuration
"""
import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "jarvis_config.json")

DEFAULT_CONFIG = {
    "api_key": "",
    "wake_word": "jarvis",
    "voice_enabled": True,
    "speech_rate": 150,
    "speech_volume": 0.9,
    "model": "claude-sonnet-4-20250514",
    "username": "Sir",
    "auto_start": False,
    "theme": "dark",
    "window_opacity": 0.95,
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                cfg = json.load(f)
                # Merge with defaults for any missing keys
                for k, v in DEFAULT_CONFIG.items():
                    if k not in cfg:
                        cfg[k] = v
                return cfg
        except:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
