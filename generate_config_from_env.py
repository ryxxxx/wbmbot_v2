#!/usr/bin/env python3
"""
Generate WBM config file from Coolify environment variables.
This script reads environment variables and creates a wbm_config.json file.
"""

import os
import json
import sys
from pathlib import Path


def get_env_var(key, default=None, required=False):
    """Get environment variable with optional default and required check."""
    value = os.getenv(key, default)
    if required and value is None:
        print(f"ERROR: Required environment variable {key} is not set")
        sys.exit(1)
    return value


def parse_emails(email_string):
    """Parse comma-separated email string into list."""
    if not email_string:
        return []
    return [email.strip() for email in email_string.split(',') if email.strip()]


def parse_exclude_list(exclude_string):
    """Parse comma-separated exclude string into list."""
    if not exclude_string:
        return []
    return [item.strip().lower() for item in exclude_string.split(',') if item.strip()]


def str_to_bool(value):
    """Convert string to boolean."""
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', '1', 'on'):
        return True
    return False


def generate_config():
    """Generate WBM config from environment variables."""
    
    config = {
        # Personal Information
        "first_name": get_env_var("WBM_FIRST_NAME", required=True),
        "last_name": get_env_var("WBM_LAST_NAME", required=True),
        "sex": get_env_var("WBM_SEX", "m"),  # m or f
        "emails": parse_emails(get_env_var("WBM_EMAILS", required=True)),
        
        # Contact Information
        "street": get_env_var("WBM_STREET", required=True),
        "zip_code": get_env_var("WBM_ZIP_CODE", required=True),
        "city": get_env_var("WBM_CITY", required=True),
        "phone": get_env_var("WBM_PHONE", required=True),
        
        # WBS Information
        "wbs": get_env_var("WBM_WBS", "no"),  # yes or no
        "wbs_date": get_env_var("WBM_WBS_DATE", None),  # DD/MM/YYYY
        "wbs_num": get_env_var("WBM_WBS_NUM", None),
        "wbs_rooms": get_env_var("WBM_WBS_ROOMS", "1"),
        "wbs_special_housing_needs": get_env_var("WBM_WBS_SPECIAL_HOUSING_NEEDS", "no"),
        
        # Filtering Preferences
        "exclude": parse_exclude_list(get_env_var("WBM_EXCLUDE", "")),
        "flat_rent_below": get_env_var("WBM_FLAT_RENT_BELOW", "800"),
        "flat_size_above": get_env_var("WBM_FLAT_SIZE_ABOVE", "0"),
        "flat_rooms_above": get_env_var("WBM_FLAT_ROOMS_ABOVE", "0"),
        
        # Notification Settings
        "discord_notifications": str_to_bool(get_env_var("WBM_DISCORD_NOTIFICATIONS", "false")),
    }
    
    # Optional notification email (separate from application emails)
    notifications_email = get_env_var("WBM_NOTIFICATIONS_EMAIL")
    if notifications_email:
        config["notifications_email"] = notifications_email
    
    return config


def initialize_log_file():
    """Initialize the successful_applications.json log file from environment variable."""
    # Get the initial log data from environment variable
    initial_log_data = get_env_var("WBM_INITIAL_LOG_DATA", "{}")
    
    # Ensure logging directory exists
    log_dir = Path(os.getcwd()) / "logging"
    log_dir.mkdir(exist_ok=True)
    
    # Write the log file
    log_file = log_dir / "successful_applications.json"
    try:
        # Try to parse the initial log data as JSON
        log_data = json.loads(initial_log_data)
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=4, ensure_ascii=False)
        print(f"✅ Application log file initialized: {log_file}")
    except json.JSONDecodeError:
        print(f"⚠️  Invalid JSON in WBM_INITIAL_LOG_DATA, using empty object")
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)
        print(f"✅ Application log file initialized with empty data: {log_file}")


def main():
    """Main function to generate and save config."""
    try:
        print("Generating WBM config from Coolify environment variables...")
        
        # Generate config from environment variables
        config = generate_config()
        
        # Use the same path structure as constants.py: {os.getcwd()}/configs/wbm_config.json
        # In Docker, working directory is /home, so this will be /home/configs/wbm_config.json
        config_dir = Path(os.getcwd()) / "configs"
        config_dir.mkdir(exist_ok=True)
        
        # Write config file to the exact same location that load_wbm_config expects
        config_file = config_dir / "wbm_config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Config file created successfully: {config_file}")
        print(f"📧 Using emails: {', '.join(config['emails'])}")
        print(f"🏠 WBS: {config['wbs']} ({config['wbs_num']} - {config['wbs_rooms']} rooms)")
        print(f"💰 Max rent: {config['flat_rent_below']}€")
        print(f"📏 Min size: {config['flat_size_above']}m²")
        print(f"🏠 Min rooms: {config['flat_rooms_above']}")
        if config['exclude']:
            print(f"🚫 Excluding: {', '.join(config['exclude'])}")
        print(f"🔔 Discord notifications: {'enabled' if config['discord_notifications'] else 'disabled'}")
        
        # Initialize the application log file
        print("\nInitializing application log file...")
        initialize_log_file()
        
    except KeyboardInterrupt:
        print("\n❌ Configuration generation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error generating config: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()