import os

# Bot token from @botfather
BOT_TOKEN = os.environ.get("BOT_TOKEN","7533212360:AAEBnSox6BEU4Mw4gsl8ulMdJOx6U20sAwU")
# From my.telegram.org/
API_ID = int(os.environ.get("API_ID", "5360874"))
API_HASH = os.environ.get("API_HASH","4631f40a1b26c2759bf1be4aff1df710")
# For /log cmd
OWNER_ID = [int(i) for i in os.environ.get("OWNER_ID", "6103947285").split(" ")]
# No time limit for this users
AUTH_USERS = [int(i) for i in os.environ.get("AUTH_USERS", "6103947285").split(" ")]
# Time gap after each request (in seconds)
TIME_GAP = int(os.environ.get("TIME_GAP", "360"))
# Bot channel ID for ForceSub, don't forget to add bot in Bot Channel
UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", False)
