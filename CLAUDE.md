# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WBMBOT_v2 is a Python-based Selenium automation bot designed to automatically apply for apartment listings on the WBM (Wohnungsbaugesellschaft Berlin-Mitte) website. The bot scrapes apartment listings, filters them based on user preferences, and submits applications automatically.

## Common Development Commands

### Running the Bot
```bash
# Basic run
python3 wbmbot_v2/main.py

# With custom interval (default is 3 minutes)
python3 wbmbot_v2/main.py -i 5

# Headless mode (no browser window)
python3 wbmbot_v2/main.py -H

# Test mode (uses local test data)
python3 wbmbot_v2/main.py -t
```

### Dependencies
```bash
# Install requirements
pip install -r wbmbot_v2/requirements.txt
```

### Environment Variables
```bash
# Email notifications (optional)
export EMAIL_PASSWORD="your_outlook_app_password"

# Discord notifications (optional) 
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
```

### Docker Operations
```bash
# Build image
docker build -f ci/docker/Dockerfile -t wbmbot_v2 .

# Pull from registry
docker pull vel7an/wbmbot_v2:latest

# Run with volumes (interactive for first-time setup)
docker run -it \
    -v /PATH_HERE/offline_viewings:/home/offline_viewings \
    -v /PATH_HERE/logging:/home/logging \
    -v /PATH_HERE/configs:/home/configs \
    vel7an/wbmbot_v2:latest

# Run with email and Discord notifications
docker run -it \
    -e "EMAIL_PASSWORD=your_password" \
    -e "DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_URL" \
    -v /PATH_HERE/offline_viewings:/home/offline_viewings \
    -v /PATH_HERE/logging:/home/logging \
    -v /PATH_HERE/configs:/home/configs \
    vel7an/wbmbot_v2:latest
```

## Code Architecture

### Core Structure
- **`main.py`**: Entry point and main orchestration loop with crash recovery
- **`handlers/`**: Core business logic classes
  - `flat.py`: Flat listing data model with filtering logic
  - `user.py`: User profile and configuration management
- **`helpers/`**: Utility modules
  - `webDriverOperations.py`: Selenium automation logic for web scraping and form filling
  - `notifications.py`: Email notification system
  - `discord_notifications.py`: Discord webhook notification system with rich embeds
  - `constants.py`: Application constants and configuration
- **`chromeDriver/`**: Chrome WebDriver configuration and management
- **`utility/`**: Common utilities for I/O, user interaction, and miscellaneous operations
- **`logger/`**: Custom colored logging system
- **`httpsWrapper/`**: HTTP page downloading functionality

### Key Data Flow
1. User configuration loaded from `configs/wbm_config.json`
2. Chrome WebDriver initialized with appropriate settings
3. Main loop in `webDriverOperations.process_flats()` handles:
   - Page navigation and scraping
   - Flat listing extraction and filtering
   - Application form submission
   - Success/failure logging to `logging/successful_applications.json`

### Configuration System
- User config stored in `configs/wbm_config.json` with personal details, filtering preferences, WBS information, and notification settings
- Test configuration available in `test-data/wbm_test_config.json`
- Email notifications require `EMAIL_PASSWORD` environment variable (Outlook only)
- Discord notifications require `DISCORD_WEBHOOK_URL` environment variable and `discord_notifications: true` in config
- Application history tracked in `logging/successful_applications.json` to prevent duplicate applications

### Output Management
- Offline apartment pages saved to `offline_viewings/angebote_pages/`
- PDF exposés downloaded to `offline_viewings/apartments_expose_pdfs/`
- Structured logging with timestamps and color coding
- Application success/failure tracking with detailed reasoning

### Testing Strategy
- Test mode (`-t` flag) uses local HTML files from `test-data/` directory
- No actual network requests made in test mode
- Allows development and debugging without hitting live website