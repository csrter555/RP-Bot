import discord
from discord import app_commands
from discord.ext import commands


class Layout(discord.ui.Container):
  # Set accent color as a keyword or pass children positionally
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
    await interaction.response.send_message(
        f"You selected: {select.values[0]}", ephemeral=True
    )


class TestView(discord.ui.LayoutView):

  def __init__(self):
    super().__init__()
    self.add_item(Layout())


# Inside your Cog or setup:
@app_commands.command(
    name="test2", description="Testing Components V2 Layout"
)
async def test_command(interaction: discord.Interaction):
  view = TestView()
  await interaction.response.send_message(view=view)