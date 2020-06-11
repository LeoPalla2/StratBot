import discord
from discord.ext.commands import Bot
from discord.ext import commands



Client = discord.Client()
bot_prefix = "!"
client = commands.Bot(command_prefix=bot_prefix)
channels_list=[715868081594826783,715868097365540876,715868124104228974]

@client.event
async def on_ready():
    print("Bot Online")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))

@client.event
async def on_message(message):
    await client.process_commands(message)
    if "[strat]" in message.content and message.channel.id not in channels_list:
        if "d1" in message.channel.name:
            channel = client.get_channel(channels_list[0])
        elif "d2" in message.channel.name:
            channel = client.get_channel(channels_list[1])
        else:
            channel = client.get_channel(channels_list[2])
        await channel.send(message.content)
        await channel.send("Original post: https://discordapp.com/channels/"+str(message.guild.id)+"/"+str(message.channel.id)+"/"+str(message.id))

        
client.run("MzgyNTg4OTg0MzU1NzE3MTIy.Xs_X4Q.kosXCT_6qABSG80IwEWrKvkR5VI")
