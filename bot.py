import discord
import os
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from dotenv import find_dotenv
import pickle

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
guilds_dictionary = {}
Client = discord.Client()
bot_prefix = "!"
client = commands.Bot(command_prefix=bot_prefix)
client.remove_command('help')
@client.event
async def on_ready():
    print("Bot Online")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    f = open("dict.pkl","rb")
    global guilds_dictionary
    guilds_dictionary = pickle.load(f)
    f.close()
    for guild in client.guilds:
        if not get(guild.roles, name="StratBotMod"):
            await guild.create_role(name="StratBotMod", colour=discord.Colour(0x0062ff))
        if guild.id not in guilds_dictionary.keys():
            guilds_dictionary[guild.id] = {}

@client.event
async def on_guild_join(guild):
    if guild.id not in guilds_dictionary.keys():
        guilds_dictionary[id] = {}
    if not get(guild.roles, name="StratBotMod"):
            await guild.create_role(name="StratBotMod", colour=discord.Colour(0x0062ff))

@client.event
async def on_guild_remove(guild):
    if guild.id in guilds_dictionary.keys():
        del guilds_dictionary[id]

@client.event
async def on_disconnect():
    f = open("dict.pkl","wb")
    pickle.dump(guilds_dictionary,f)
    f.close()

@client.event
async def on_message(message):
    ctx = await client.get_context(message)
    if ctx.valid:
        await client.process_commands(message)
    else:
        for (tag,channel) in guilds_dictionary[message.guild.id].items():
            if tag in message.content and message.author.bot == False and guilds_dictionary[message.guild.id][tag] != message.channel.id:
                chan = client.get_channel(channel)
                await chan.send(message.content+"\n"+"Original post by " + message.author.mention +":\nhttps://discordapp.com/channels/"+str(message.guild.id)+"/"+str(message.channel.id)+"/"+str(message.id))

@client.command()
@commands.has_role("StratBotMod")
async def setTag(ctx,tag):
    guilds_dictionary[ctx.guild.id][tag] = ctx.message.channel.id
    f = open("dict.pkl","wb")
    pickle.dump(guilds_dictionary,f)
    f.close()
    await ctx.send("Messages containing \"" +tag + "\" will now be reposted in this channel")

@setTag.error
async def setTag_error(ctx,error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Only StratBotMods can use this command")

@client.command()
async def showTag(ctx):
    for (key,value) in guilds_dictionary[ctx.guild.id].items():
        if value == ctx.message.channel.id:
            await ctx.send("Auto detection tag for this channel is: " + key)
            return
    await ctx.send("No tag set for this channel")

@client.command()
async def help(ctx):
    await ctx.send("```\nGeneral Use:\n\tThis bot is made to organise your strat channels. By setting an autodetection tag in a channel, the bot will repost any message containing the tag to this channel with a link to the original post. \n\nCommands: \n\tsetTag [tag]: Set the auto detection tag redirecting to the channel where the command is called\n\tshowTag: Show the auto detection tag currently set for the channel where the command is called\n```")

client.run(token)
