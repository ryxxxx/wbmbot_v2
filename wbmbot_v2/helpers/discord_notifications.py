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
    flat_details: dict, 
    user_email: str, 
    application_status: str = "success"
):
    """Send Discord notification for apartment application.

    Args:
        webhook_url (str): Discord webhook URL.
        flat_details (dict): Dictionary containing flat information.
        user_email (str): Email address used for the application.
        application_status (str): Status of the application ('success' or 'failed').
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
        embed.add_embed_field(name="🏠 Title", value=flat_details.get('title', 'N/A'), inline=False)
        embed.add_embed_field(name="📍 Location", value=f"{flat_details.get('district', 'N/A')}, {flat_details.get('street', 'N/A')}", inline=True)
        embed.add_embed_field(name="🏙️ Address", value=f"{flat_details.get('zip_code', 'N/A')} {flat_details.get('city', 'N/A')}", inline=True)
        embed.add_embed_field(name="💰 Total Rent", value=flat_details.get('total_rent', 'N/A'), inline=True)
        embed.add_embed_field(name="📏 Size", value=flat_details.get('size', 'N/A'), inline=True)
        embed.add_embed_field(name="🚪 Rooms", value=flat_details.get('rooms', 'N/A'), inline=True)
        
        # Add WBS status
        wbs_status = "Yes" if flat_details.get('wbs', False) else "No"
        embed.add_embed_field(name="🎫 WBS Required", value=wbs_status, inline=True)
        
        # Add timestamp
        embed.set_timestamp()
        
        # Set footer
        embed.set_footer(text=f"WBMBOT v{constants.bot_version}")

        # Add embed to webhook
        webhook.add_embed(embed)
        
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