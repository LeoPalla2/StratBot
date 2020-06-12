import discord
from discord.ext.commands import Bot
from discord.ext import commands



Client = discord.Client()
bot_prefix = "!"
client = commands.Bot(command_prefix=bot_prefix)
bot_id= 382588984355717122
channels_dictionary = {}
tag = "[strat]"
@client.event
async def on_ready():
    print("Bot Online")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))

@client.event
async def on_message(message):
    await client.process_commands(message)
    if tag in message.content and message.author.bot == False:
        if message.channel.id in channels_dictionary.keys():
            channel = client.get_channel(channels_dictionary[message.channel.id])
            await channel.send(message.content+"\n"+"Original post: https://discordapp.com/channels/"+str(message.guild.id)+"/"+str(message.channel.id)+"/"+str(message.id))
        else:
            channel = message.channel
            await channel.send("This channel isn't bound yet. use the bindChannel command to bind it")
        

@client.command()
async def bindChannel(ctx,channel: discord.TextChannel):
    channels_dictionary[ctx.message.channel.id] = channel.id
    await ctx.send("This channel is now bound to " + channel.mention)


@client.command()
async def setTag(ctx,newtag):
    global tag
    await ctx.send("Autodetection tag changed from " +tag + " to: " + newtag)
    tag = newtag

@client.command()
async def showTag(ctx):
    global tag
    await ctx.send("Autodetection tag is: " +tag)

@setTag.error
async def setTag_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Please specify a new autodetection tag")

@bindChannel.error
async def bindChannel_error(ctx,error):
    if isinstance(error,commands.BadArgument):
        await ctx.send("This is not a valid channel on this server")
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Please specify the channel you want to link with")
        
client.run("MzgyNTg4OTg0MzU1NzE3MTIy.Xs_X4Q.kosXCT_6qABSG80IwEWrKvkR5VI")
