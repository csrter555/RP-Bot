import asyncio
import datetime
import io
import json
import logging
import math
import os
import random
import sqlite3
import time
from pathlib import Path
from typing import Optional

import aiohttp
import discord
from discord import app_commands
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
  # Crucial Fix: ensure the folder path matches the extension dot-path
  if os.path.exists("./cogs"):
    for filename in os.listdir("./cogs"):
      if filename.endswith(".py") and filename != "__init__.py":
        try:
          await client.load_extension(f"cogs.{filename[:-3]}")
          print(f"Loaded Cog: {filename}")
        except Exception as e:
          print(f"Failed to load cog {filename}: {e}")


async def load_utils():
  if os.path.exists("./utils"):
    for filename in os.listdir("./utils"):
      if filename.endswith(".py") and filename != "__init__.py":
        try:
          await client.load_extension(f"utils.{filename[:-3]}")
          print(f"Loaded Util: {filename}")
        except Exception as e:
          print(f"Failed to load util {filename}: {e}")


@client.event
async def on_ready():
  print(f"Logged in as {client.user} (ID: {client.user.id})")

  # Sync commands
  if GUILD_ID:
    try:
      synced = await client.tree.sync(guild=discord.Object(id=int(GUILD_ID)))
      print(f"Synced {len(synced)} commands to guild.")
    except Exception as e:
      print(f"Command sync failed: {e}")


# --- Components V2 Layout System ---


class Layout(discord.ui.Container):

  accent_color = discord.Color.blue()

  first = discord.ui.TextDisplay(
      "Test.... (You CAN SEE THIS??? the bot may be coming soon?!)"
  )

  button_row = discord.ui.ActionRow()
  select_row = discord.ui.ActionRow()

  @button_row.button(label="Test Button", style=discord.ButtonStyle.primary)
  async def aaa(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.response.send_message(
        "You clicked the button!", ephemeral=True
    )

  @select_row.select(
      placeholder="Test",
      options=[
          discord.SelectOption(label="Option 1", value="option1"),
          discord.SelectOption(label="Option 2", value="option2"),
          discord.SelectOption(label="Option 3", value="option3"),
      ],
  )
  async def bbb(
      self, interaction: discord.Interaction, select: discord.ui.Select
  ):
    # Fixed select values parsing
    selected_value = select.values[0] if select.values else "None"
    await interaction.response.send_message(
        f"You selected: {selected_value}", ephemeral=True
    )


# Standardizing Layout View sub-class to avoid multi-execution state issues
class TestView(discord.ui.LayoutView):

  def __init__(self):
    super().__init__()
    self.add_item(Layout())


@client.tree.command(
    name="test", description="...", guild=discord.Object(id=int(GUILD_ID))
)
async def test_command(interaction: discord.Interaction):
  # Fresh view assigned per command interaction execution
  view = TestView()
  await interaction.response.send_message(view=view)


async def main():
  async with client:
    await load_commands()
    await load_utils()  # Remembered to invoke utility loaders
    await client.start(TOKEN)


if __name__ == "__main__":
  asyncio.run(main())