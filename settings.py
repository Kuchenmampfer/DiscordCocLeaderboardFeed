import datetime
from discord import Colour

# Do you want a builder base leaderboard? If so, set this to True
VERSUS = False

# enter the tags of the clans of the players you want to include in the leaderboards as shown into the following list
CLAN_TAGS = ["#2VJLGYC2", "#UPYYY8PC", "#LQJGRC9Y", "#288CVY8P8", "#QL89RUV2", "#RPJ8RPLP"]

# For daily leaderboards, select True. For leaderboards only at the end of season, select False and ignore INVOKE_TIME
DAILY = True

# adjust the daily time you want the leaderboard to be posted. Note that this is UTC time
INVOKE_TIME = datetime.time(hour=4, minute=58)

# What title shall the leaderboard have?
LEADERBOARD_TITLE = "Legendary Leaderboard"

# customize the appearance of your leaderboard by changing the following strings that are used to construct it
# the player separator stands between the players and can be something like "\n----------\n"
PLAYER_SEPARATOR = "\n\n"

# The player format string lets you adjust how each player appears. Note that the player object has various
# attributes that can be shown. These attributes change depending on the type of leaderboard you chose. You can find
# them in the coc.py documentation: https://cocpy.readthedocs.io/en/latest/code_overview/models.html#players For clan
# leaderboards, the ClanMember model is used. For location leaderboards, look into RankedPlayer. Note that you can
# use Discord formatting.
PLAYER_FORMAT_STRING = "`Rank    ` **{rank}**\n" \
                       "`Trophies` {player.trophies}\n" \
                       "`Name    ` {player.name}\n" \
                       "`Tag     ` {player.tag}\n"\
                       "`Clan    ` {player.clan}"

# the player limit lets you control how many players the leaderboard shall hold
PLAYER_LIMIT = 5

# Do you want to add a timestamp to your leaderboard? Choose True or False
TIMESTAMP = True

# Which colour shall the bar of the embed have? For a list of available colours visit
# https://discordpy.readthedocs.io/en/latest/api.html#colour
COLOUR = Colour.red()
