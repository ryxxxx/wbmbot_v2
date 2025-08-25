import time
from discord_webhook import DiscordWebhook, DiscordEmbed
from helpers import constants
from logger import wbm_logger
import os

__appname__ = os.path.splitext(os.path.basename(__file__))[0]
color_me = wbm_logger.ColoredLogger(__appname__)
LOG = color_me.create_logger()


def send_discord_notification(
    webhook_url: str, 
    flat_details: set, 
    user_email: str, 
    application_status: str = "success",
    pdf_path: str = None
):
    """Send Discord notification for apartment application.

    Args:
        webhook_url (str): Discord webhook URL.
        flat_details (set): Set containing flat information strings.
        user_email (str): Email address used for the application.
        application_status (str): Status of the application ('success' or 'failed').
        pdf_path (str): Path to the PDF file (optional).
    """

    if not webhook_url:
        LOG.warning(
            color_me.yellow(
                "Discord webhook URL not found. Discord notifications disabled 🚧"
            )
        )
        return

    try:
        # Initialize Discord webhook
        webhook = DiscordWebhook(url=webhook_url)
        
        # Create embed based on application status
        if application_status == "success":
            embed = DiscordEmbed(
                title="🎉 Successfully Applied to Apartment!",
                description=f"Applied with email: {user_email}",
                color='00ff00'  # Green
            )
            embed.add_embed_field(name="✅ Status", value="Application Submitted", inline=False)
        else:
            embed = DiscordEmbed(
                title="❌ Failed to Apply to Apartment",
                description=f"Attempted with email: {user_email}",
                color='ff0000'  # Red
            )
            embed.add_embed_field(name="❌ Status", value="Application Failed", inline=False)

        # Add apartment details to embed
        # Convert set to list and extract information
        flat_info_list = list(flat_details)
        
        # Parse the flat details from the set
        title_info = ""
        link_info = ""
        
        for detail in flat_info_list:
            if detail.startswith("[Applied]"):
                title_info = detail.replace("[Applied] ", "")
            elif detail.startswith("Apartment Link:"):
                link_info = detail.replace("Apartment Link: ", "")
        
        embed.add_embed_field(name="🏠 Title", value=title_info if title_info else "N/A", inline=False)
        embed.add_embed_field(name="🔗 Link", value=link_info if link_info else "N/A", inline=False)
        
        # Add timestamp
        embed.set_timestamp()
        
        # Set footer
        embed.set_footer(text=f"WBMBOT v{constants.bot_version}")

        # Add embed to webhook
        webhook.add_embed(embed)
        
        # Add PDF file as attachment if provided
        if pdf_path and os.path.exists(pdf_path):
            try:
                with open(pdf_path, "rb") as f:
                    webhook.add_file(file=f.read(), filename=os.path.basename(pdf_path))
                LOG.info(color_me.blue(f"Added PDF attachment: {os.path.basename(pdf_path)}"))
            except Exception as e:
                LOG.warning(color_me.yellow(f"Failed to attach PDF file: {str(e)}"))
                # Add PDF path as field if file attachment fails
                embed.add_embed_field(name="📄 PDF Path", value=pdf_path, inline=False)
        elif pdf_path:
            LOG.warning(color_me.yellow(f"PDF file not found: {pdf_path}"))
            embed.add_embed_field(name="📄 PDF Path", value=f"{pdf_path} (file not found)", inline=False)
        
        # Send webhook with rate limiting
        response = webhook.execute()
        
        if response.status_code == 200 or response.status_code == 204:
            LOG.info(
                color_me.green("Discord notification sent successfully ✅")
            )
        else:
            LOG.error(
                color_me.red(f"Discord notification failed with status {response.status_code} ❌")
            )
            
        # Add rate limiting delay to prevent Discord API blocks
        time.sleep(1)
        
    except Exception as e:
        LOG.error(color_me.red(f"Failed to send Discord notification: {str(e)} ❌"))


def send_discord_status_update(webhook_url: str, message: str, status_type: str = "info"):
    """Send a general status update to Discord.

    Args:
        webhook_url (str): Discord webhook URL.
        message (str): Status message to send.
        status_type (str): Type of status ('info', 'warning', 'error', 'success').
    """
    
    if not webhook_url:
        return

    try:
        webhook = DiscordWebhook(url=webhook_url)
        
        # Set color and emoji based on status type
        colors = {
            'info': '0099ff',      # Blue
            'warning': 'ffaa00',   # Orange
            'error': 'ff0000',     # Red
            'success': '00ff00'    # Green
        }
        
        emojis = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌',
            'success': '✅'
        }
        
        embed = DiscordEmbed(
            title=f"{emojis.get(status_type, 'ℹ️')} Bot Status Update",
            description=message,
            color=colors.get(status_type, '0099ff')
        )
        
        embed.set_timestamp()
        embed.set_footer(text=f"WBMBOT v{constants.bot_version}")
        
        webhook.add_embed(embed)
        response = webhook.execute()
        
        if response.status_code not in [200, 204]:
            LOG.error(
                color_me.red(f"Discord status update failed with status {response.status_code} ❌")
            )
            
        # Rate limiting
        time.sleep(1)
        
    except Exception as e:
        LOG.error(color_me.red(f"Failed to send Discord status update: {str(e)} ❌"))