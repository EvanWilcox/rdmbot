"""
RDM Discord Bot
"""

import os
import time
import random
import asyncio

from dateutil import parser
from requests_oauthlib import OAuth1Session

import discord


BUILD = os.getenv("BUILD", "dev")
print(f"In {BUILD} mode.")

if BUILD != "prod":
    from dotenv import load_dotenv

    load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
DISCORD_BOT_KEY = os.getenv("DISCORD_BOT_KEY")
TWITTER_ID = os.getenv("TWITTER_ID")

BACKLOG_FILE = "backlog.txt"


# Make the request
oauth = OAuth1Session(
    CONSUMER_KEY,
    client_secret=CONSUMER_SECRET,
    resource_owner_key=ACCESS_TOKEN,
    resource_owner_secret=ACCESS_TOKEN_SECRET,
)


client = discord.Client()

MIN_TWEET_DELAY = 60 * 60 * 12
DISCORD_POST_DELAY = 60 * 5


def post_tweet(message: str) -> None:
    """Post a tweet."""
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json={"text": message.replace('"', "")},
    )
    print(response.status_code, response.text)


def time_since_last_tweet() -> int:
    """Get the time in seconds since the last tweet was posted."""
    response = oauth.get(
        f"https://api.twitter.com/2/users/{TWITTER_ID}/tweets",
        params={"tweet.fields": "created_at"},
    )
    if response.status_code == 200:
        return time.time() - parser.parse(response.json()["data"][0]["created_at"]).timestamp()


async def process_backlog() -> None:
    """Process the backlog of messages to be posted."""
    while True:
        time_since = time_since_last_tweet()
        print(f"Time since last tweet: {time_since / 60 / 60:.1f} hours.")

        if time_since is None:
            print("Error getting time since last tweet")
            return

        if time_since > MIN_TWEET_DELAY:
            print(
                f"No tweets in last {MIN_TWEET_DELAY / 60 / 60:.1f} hour(s),"
                f"posting a random one from the backlog."
            )
            file = open(BACKLOG_FILE, "r", encoding="UTF-8")
            backlog = file.readlines()
            rand_line = random.randint(0, len(backlog) - 1)
            file.close()

            print("Posting from backlog: ", end="")

            if BUILD == "prod":
                post_tweet(backlog[rand_line])
                del backlog[rand_line]
            else:
                print(backlog[rand_line])

            file = open(BACKLOG_FILE, "w", encoding="UTF-8")
            for line in backlog:
                file.write(line)
            file.close()

            await asyncio.sleep(MIN_TWEET_DELAY)

        else:
            print(f"Not posting a tweet, last tweet was {time_since / 60 / 60:.1f} hours ago.")
            print(f"Checking in {(MIN_TWEET_DELAY - time_since) / 60 / 60:.1f} hours.")
            await asyncio.sleep(MIN_TWEET_DELAY - time_since)


@client.event
async def on_ready() -> None:
    """Called when the bot is ready to start."""
    print(f"We have logged in as {client.user}")

    if os.path.exists(BACKLOG_FILE):
        print("Found backlog file, starting backlog processor.")
        await process_backlog()
    else:
        print("No backlog file found.")


@client.event
async def on_message(message) -> None:
    """Handles messages."""
    if message.channel.name == "overheard":
        message_id = message.id
        await asyncio.sleep(DISCORD_POST_DELAY)

        try:
            message = await message.channel.fetch_message(message_id)
            print("Posting from Discord: ", end="")
            if BUILD == "prod":
                post_tweet(message.content)
            else:
                print(message.content)

        except discord.errors.NotFound:
            pass

    elif message.channel.name == "bot-test":
        print(message.content)
        message_id = message.id
        await asyncio.sleep(60)

        try:
            message = await message.channel.fetch_message(message_id)
            print("Posting from Discord: ", end="")
            print(message.content)
        except discord.errors.NotFound:
            print("Message Deleted")


# Start Discord bot
client.run(DISCORD_BOT_KEY)
