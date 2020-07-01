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
    try:
        f = open("dict.pkl","rb")
        global guilds_dictionary
        guilds_dictionary = pickle.load(f)
        f.close()
    except:
        print("file does not exist")
        pass
    if not isinstance(guilds_dictionary,dict):
        guilds_dictionary = {}
    for guild in client.guilds:
        if not get(guild.roles, name="StratBotMod"):
            await guild.create_role(name="StratBotMod", colour=discord.Colour(0x0062ff))
        if guild.id not in guilds_dictionary.keys():
            guilds_dictionary[guild.id] = {}

@client.event
async def on_guild_join(guild):
    if guild.id not in guilds_dictionary.keys():
        guilds_dictionary[guild.id] = {}
        f = open("dict.pkl","wb")
        pickle.dump(guilds_dictionary,f)
        f.close()
    if not get(guild.roles, name="StratBotMod"):
            await guild.create_role(name="StratBotMod", colour=discord.Colour(0x0062ff))

@client.event
async def on_guild_remove(guild):
    if guild.id in guilds_dictionary.keys():
        del guilds_dictionary[guild.id]
        f = open("dict.pkl","wb")
        pickle.dump(guilds_dictionary,f)
        f.close()

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
        if message.channel.category.id in guilds_dictionary[message.guild.id].keys():
            for (channel,tags) in guilds_dictionary[message.guild.id][message.channel.category.id].items():
                for tag in tags:
                    if tag in message.content and message.author.bot == False and channel != message.channel.id:
                        chan = client.get_channel(channel)
                        await chan.send(message.content+"\n"+"Original post by " + message.author.mention +":\nhttps://discordapp.com/channels/"+str(message.guild.id)+"/"+str(message.channel.id)+"/"+str(message.id))

@client.command()
@commands.has_role("StratBotMod")
async def addTag(ctx,tag):
    if ctx.message.channel.category.id not in guilds_dictionary[ctx.guild.id].keys():
        guilds_dictionary[ctx.guild.id][ctx.message.channel.category.id] = {}
    if ctx.message.channel.id not in guilds_dictionary[ctx.guild.id][ctx.message.channel.category.id].keys():
        guilds_dictionary[ctx.guild.id][ctx.message.channel.category.id][ctx.message.channel.id] = []
    if tag not in guilds_dictionary[ctx.guild.id][ctx.message.channel.category.id][ctx.message.channel.id]:
        guilds_dictionary[ctx.guild.id][ctx.message.channel.category.id][ctx.message.channel.id].append(tag)
        f = open("dict.pkl","wb")
        pickle.dump(guilds_dictionary,f)
        f.close()
        await ctx.send("Messages containing \"" +tag + "\" will now be reposted in this channel")
    else:
        await ctx.send("This tag is already set for this channel")

@addTag.error
async def addTag_error(ctx,error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Only StratBotMods can use this command")

@client.command()
async def showTags(ctx):
    if ctx.message.channel.category.id in guilds_dictionary[ctx.guild.id].keys() and ctx.message.channel.id in guilds_dictionary[ctx.guild.id][ctx.message.channel.category.id].keys():
        await ctx.send("Auto detection tags for this channel: " + str(guilds_dictionary[ctx.guild.id][ctx.message.channel.category.id][ctx.message.channel.id])[1:-1])
    else:
        await ctx.send("No tag set for this channel")

@client.command()
async def removeAllTags(ctx):
    if ctx.message.channel.id in guilds_dictionary[ctx.guild.id][ctx.message.channel.category.id].keys():
        del guilds_dictionary[ctx.guild.id][ctx.message.channel.category.id][ctx.message.channel.id]
        f = open("dict.pkl","wb")
        pickle.dump(guilds_dictionary,f)
        f.close()
        await ctx.send("all auto detection tags deleted")
    else:
        await ctx.send("No tag set for this channel")

@client.command()
async def removeTag(ctx,tag):
    if ctx.message.channel.id in guilds_dictionary[ctx.guild.id][ctx.message.channel.category.id].keys():
        if tag in guilds_dictionary[ctx.guild.id][ctx.message.channel.category.id][ctx.message.channel.id]:
            guilds_dictionary[ctx.guild.id][ctx.message.channel.category.id][ctx.message.channel.id].remove(tag)
            f = open("dict.pkl","wb")
            pickle.dump(guilds_dictionary,f)
            f.close()
            await ctx.send("Auto detection tag deleted")
        else:
            await ctx.send("This tag doesn't exist")
    else:
        await ctx.send("No tag set for this channel")

@client.command()
async def help(ctx):
    await ctx.send("```\nGeneral Use:\n\tThis bot is made to organise your strats channels. By setting auto detection tags in a channel, the bot will repost any message containing the tag to this channel with a link to the original post. Tags and detection are defined within channel categories \n\nCommands: \n\taddTag [tag]: Add a tag to the current channel's tags list if it isn't already defined\n\tshowTags: Show the auto detection tags list for the current channel\n\tremoveTag [tag]: Remove the specified tag set from the current channel's tags list if it exists\n\tremoveAllTags: Remove all tags defined for the current channel\n```")

client.run(token)
