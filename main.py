import os
import asyncio
import random
import sqlite3
import json
import requests
import logging
import traceback
import math
import io
import datetime

import logging
import time
from pathlib import Path
from typing import Optional

import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv 
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix=">", intents=intents)

START_TIME = time.time()

async def load_commands():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await client.load_extension(f"commands.{filename[:-3]}")
                print(f"Loaded: {filename}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

async def load_utils():
    for filename in os.listdir("./utils"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await client.load_extension(f"utils.{filename[:-3]}")
                print(f"Loaded: {filename}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")

    # Sync commands
    try:
        synced = await client.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"Synced {len(synced)} commands to guild.")
    except Exception as e:
        print(f"Command sync failed: {e}")


class Layout(discord.ui.Container):

  accent_color = discord.Color.blue()

  first = discord.ui.TextDisplay("Test.... (You CAN SEE THIS??? the bot may be coming soon?!)")

  button_row = discord.ui.ActionRow()
  select_row = discord.ui.ActionRow()

  @button_row.button(label="Test Button", style=discord.ButtonStyle.primary)
  async def aaa(self, interaction, button):
    await interaction.response.send_message("You clicked the button!")

  @select_row.select(placeholder="Test", options=[
    discord.SelectOption(label="Option 1", value="option1"),
    discord.SelectOption(label="Option 2", value="option2"),
    discord.SelectOption(label="Option 3", value="option3"),
  ])
  async def bbb(self, interaction, select):
    await interaction.response.send_message(f"You selected: {select.values[0]}")

view = discord.ui.LayoutView()

container = Layout()
view.add_item(container)

@client.tree.command(name="test", description="...", guild=discord.Object(id=GUILD_ID))
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message(view=view)

async def main():
    async with client:
        await load_commands()
        await client.start(TOKEN)

asyncio.run(main())