import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from dotenv import load_dotenv
import os

class Client(commands.Bot):
    async def on_ready(self):
        print(f"I, {self.user}, is logged on!!")
        try:
            synced = await self.tree.sync(guild=GUILD_ID)  # <-- Registration happens here
            print(f"Synced {len(synced)} slash commands.")
        except Exception as e:
            print(e)

intents = discord.Intents.default()
#intents.message_content = True
client = Client(command_prefix="!",intents=intents)

load_dotenv()
guildid = int(os.getenv("GUILD_ID"))
GUILD_ID = discord.Object(guildid)

@client.tree.command(name="hello", description="says hello", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("hiiii \nthere!!")

#replace with database
gameboard = None
white = None
black = None

@client.tree.command(name="newgame", description="Open fresh connect 5 game board", guild=GUILD_ID)
async def game(interaction: discord.Interaction, opponent: discord.User):
    global white
    white = interaction.user
    global black
    black = opponent
    await interaction.response.send_message(f"white: {interaction.user.mention}! black: {opponent.mention}", view=buttonView())
    global gameboard 
    gameboard = await interaction.followup.send(printGame(gameData), wait=True)

class buttonView(View):
    @discord.ui.button(label="place a piece", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(placePieceModal())

class placePieceModal(discord.ui.Modal, title="place a piece"):
    row = discord.ui.TextInput(
        label="Enter a number between 1 and 15",
        placeholder="1",
        required=True,
        max_length=2,
    )
    column = discord.ui.TextInput(
        label="Enter a number between 1 and 15",
        placeholder="1",
        required=True,
        max_length=2,
    )

    async def on_submit(self, interaction: discord.Interaction):
        piece = -1
        if interaction.user.id == white.id:
            piece = 0
        elif interaction.user.id == black.id:
            piece = 1
            
        gameData[int(self.row.value)-1][int(self.column.value)-1] = piece
        await gameboard.edit(content=printGame(gameData))
        await interaction.response.send_message("placed!", ephemeral=True)

gameData = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1, 1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1, 0,-1, 0,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1, 1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]

def printGame(data):
    board = ""
    num = 1
    for row in data:
        if num < 10:
            board += "0" + str(num) + "  "
        else:
            board += str(num) + "  "
        num += 1
        for spot in row:
            if spot == -1:
                board += " 十 "
            elif spot == 0:
                board += "⚪ "
            elif spot == 1:
                board += "⚫ "
        board += '\n'
    board += ".     1     2     3     4     5    6    7    8    9   10   11   12   13   14   15"
    return board

TOKEN = os.getenv('TOKEN')
client.run(TOKEN)