import discord
from discord import app_commands
from discord.ext import commands

# 1. Define your Layout container
class Layout(discord.ui.Container):
    accent_color = discord.Color.blue()
    first = discord.ui.TextDisplay("Test.... (You CAN SEE THIS??? the bot may be coming soon?!)")
    
    button_row = discord.ui.ActionRow()
    select_row = discord.ui.ActionRow()

    @button_row.button(label="Test Button", style=discord.ButtonStyle.primary)
    async def aaa(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked the button!", ephemeral=True)

    @select_row.select(placeholder="Test", options=[
        discord.SelectOption(label="Option 1", value="option1"),
        discord.SelectOption(label="Option 2", value="option2"),
        discord.SelectOption(label="Option 3", value="option3"),
    ])
    async def bbb(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_message(f"You selected: {select.values}", ephemeral=True)

# 2. Define the isolated LayoutView
class TestView(discord.ui.LayoutView):
    def __init__(self):
        super().__init__()
        self.add_item(Layout())

# 3. Create the Cog class to hold your application command
class Test2Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="test2.a", description="Testing Components V2 inside a Cog")
    async def test2_command(self, interaction: discord.Interaction):
     view = TestView()
     await interaction.response.defer(ephemeral=True)
     await interaction.channel.send(view=view)
     await interaction.delete_original_response()

# 4. The critical missing setup function
async def setup(bot: commands.Bot):
    await bot.add_cog(Test2Cog(bot))