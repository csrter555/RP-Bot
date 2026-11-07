import discord
from discord.ext import commands

class Layout(discord.ui.Container):
    def __init__(self):
        self.button_row = discord.ui.ActionRow()
        self.select_row = discord.ui.ActionRow()
        
        super().__init__(
            discord.ui.TextDisplay("Test.... (You CAN SEE THIS??? the bot may be coming soon?!)"),
            self.button_row,
            self.select_row,
            accent_color=discord.Color.blue()
        )

        @self.button_row.button(label="Test Button", style=discord.ButtonStyle.primary)
        async def aaa(interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("You clicked the button!", ephemeral=True)

        @self.select_row.select(placeholder="Test", options=[
            discord.SelectOption(label="Option 1", value="option1"),
            discord.SelectOption(label="Option 2", value="option2"),
            discord.SelectOption(label="Option 3", value="option3"),
        ])
        async def bbb(interaction: discord.Interaction, select: discord.ui.Select):
            await interaction.response.send_message(f"You selected: {select.values}", ephemeral=True)

class TestView(discord.ui.LayoutView):
    def __init__(self):
        super().__init__()
        self.add_item(Layout())

class Test2_aCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="test2-a", description="Testing Components V2 inside a Cog")
    async def test2_a_command(self, ctx: commands.Context):
        view = TestView()
        await ctx.send(view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Test2_aCog(bot))