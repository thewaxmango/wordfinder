import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import Ret

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
client = commands.Bot(command_prefix='%', intents=intents)

retr = Ret.Retriever("database.db")
listen = False


@client.event
async def on_ready():
    print('{0.user} online'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)
    if ":boom:" in message.content:
        if retr.history:
            retr.missed.append(retr.history[-1])
        if retr.listen:
            await message.channel.send(retr(1))
    if "containing:" in message.content:
        loc = message.content.index("containing:")
        substr = message.content[loc + 12:].split()[0].upper()
        retr.store(substr)


@client.command(name='review', aliases=['re', 'rv', 'r'])
async def _review(ctx, arg=None):
    await ctx.send(retr(arg))


@client.command(name='reviewmiss', aliases=['rm'])
async def _reviewmiss(ctx, arg=None):
    await ctx.send(retr(1))


@client.command(name='misslist', aliases=['ml'])
async def _misslist(ctx):
    await ctx.send(retr.get_misses())


@client.command(name='listen', aliases=['li'])
async def _listen(ctx, arg=''):
    if arg.lower() in ('on', 'i', '1', 'yes', 'y'):
        retr.listen = True
        await ctx.send("listening")
    elif arg.lower() in ('off', 'o', '0', 'no', 'n'):
        retr.listen = False
        retr.history = []
        await ctx.send("not listening")
    else:
        await ctx.send(
            "```missing or invalid argument:\non: <on/i/yes/y/1>\noff: <off/o/no/n/0>```"
        )


@client.command(name='numresponses', aliases=['numr', 'nr'])
async def _numresponses(ctx, arg=''):
    await ctx.send(retr.set_numresp(arg))

try:
    client.run(os.getenv("TOKEN"))
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
