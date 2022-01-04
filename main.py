from __future__ import annotations

import datetime
import discord
import coc
import aiohttp
import asyncio
import traceback
import settings
from credentials import *

COC_CLIENT = coc.login(COC_API_EMAIL, COC_API_PASSWORD)


async def get_clan_players(client: coc.Client) -> list[coc.ClanMember]:
    players: list[coc.ClanMember] = []
    for tag in settings.CLAN_TAGS:
        clan = None
        try:
            clan = await client.get_clan(tag)
        except coc.NotFound:
            print(f"I can't find a clan with this [{tag}] tag.")
        except coc.Maintenance:
            print("The coc API is in maintenance, I can't get data right now.")
        if clan:
            for member in clan.members:
                players.append(member)
    return players


def sort_players(players: list[coc.Player | coc.ClanMember | coc.RankedPlayer]):
    if settings.VERSUS:
        return sorted(players, key=lambda player: player.versus_trophies, reverse=True)
    else:
        return sorted(players, key=lambda player: player.trophies, reverse=True)


async def get_leaderboard_str(leaderboard: list[coc.ClanMember]) -> str:
    text = settings.PLAYER_SEPARATOR.join([settings.PLAYER_FORMAT_STRING.format(rank=rank, player=player)
                                           for rank, player in enumerate(leaderboard, 1)])
    return text


async def send_leaderboard(webhook: discord.Webhook, client: coc.Client):
    l_board = await get_clan_players(client)
    l_board_str = await get_leaderboard_str(l_board[:settings.PLAYER_LIMIT])
    embed = discord.Embed(colour=settings.COLOUR, title=settings.LEADERBOARD_TITLE, description=l_board_str)
    if settings.TIMESTAMP:
        embed.timestamp = datetime.datetime.utcnow()
    await webhook.send(embed=embed)


def calculate_remaining_time() -> datetime.timedelta:
    if not settings.DAILY:  # this indicates that leaderboards shall only be send at the end of each season
        return coc.utils.get_season_end() - datetime.datetime.utcnow()

    # now for the daily scheduling:
    if datetime.datetime.utcnow().time() > settings.INVOKE_TIME:
        next_invoke_date = datetime.date.today() + datetime.timedelta(days=1)
    else:
        next_invoke_date = datetime.date.today()
    next_invoke_time = datetime.datetime(next_invoke_date.year, next_invoke_date.month,
                                         next_invoke_date.day, settings.INVOKE_TIME.hour, settings.INVOKE_TIME.minute)
    return next_invoke_time - datetime.datetime.utcnow()


async def main():
    async with aiohttp.ClientSession() as session:
        adapter = discord.AsyncWebhookAdapter(session)
        webhook = discord.Webhook.from_url(DISCORD_WEBHOOK_URL, adapter=adapter)
        running = True
        first_run = True

        while running:
            try:
                sleep_time = calculate_remaining_time()
                if TEST_MODE and first_run:
                    first_run = False
                    print(sleep_time)
                else:
                    first_run = False
                    await asyncio.sleep(sleep_time.total_seconds())
                await send_leaderboard(webhook, COC_CLIENT)
            except BaseException:
                traceback.print_exc()
    COC_CLIENT.close()


if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        print("Interrupt detected. Closing the process.")
    except BaseException:
        traceback.print_exc()
