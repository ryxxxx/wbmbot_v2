import datetime as dt
import os

# Bot version (MAJOR.MINOR.PATCH)
bot_version = "1.1.5"

# Today
today = dt.date.today()
# Now
now = dt.datetime.now()
now = now.strftime("%Y-%m-%d_%H-%M")

# Retrieve email and password from environment variables
email_password = os.environ.get("EMAIL_PASSWORD")

# Retrieve Discord webhook URL from environment variables
discord_webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

# WBM Config File Name
wbm_config_name = f"{os.getcwd()}/configs/wbm_config.json"
wbm_test_config_name = f"{os.getcwd()}/test-data/wbm_test_config.json"

# Applications Logger that we applied for
log_file_path = f"{os.getcwd()}/logging/successful_applications.json"

# Script Logging
script_log_path = f"{os.getcwd()}/logging/wbmbot-v2_{today}.log"

# Offline viewing paths
offline_angebote_path = f"{os.getcwd()}/offline_viewings/angebote_pages/"
offline_apartment_path = f"{os.getcwd()}/offline_viewings/apartments_expose_pdfs/"

# URLs
wbm_url = "https://www.wbm.de/wohnungen-berlin/angebote/"
test_wbm_url = f"file://{os.getcwd()}/test-data/angebote.html"

# Intro Banner

intro_banner = r"""
 __      _____ __  __   ___      _         ____
 \ \    / / _ )  \/  | | _ ) ___| |_  __ _|__ /
  \ \/\/ /| _ \ |\/| | | _ \/ _ \  _| \ V /|_ \ 
   \_/\_/ |___/_|  |_| |___/\___/\__|  \_/|___/
"""
