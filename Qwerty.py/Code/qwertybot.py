""" 
_____
___  ___       __   _______   ________  _________    ___    ___ ________  ________  _________   
|\   __  \|\  \     |\  \|\  ___ \ |\   __  \|\___   ___\ |\  \  /  /|\   __  \|\   __  \|\___   ___\ 
\ \  \|\  \ \  \    \ \  \ \   __/|\ \  \|\  \|___ \  \_| \ \  \/  / | \  \|\ /\ \  \|\  \|___ \  \_| 
 \ \  \\\  \ \  \  __\ \  \ \  \_|/_\ \   _  _\   \ \  \   \ \    / / \ \   __  \ \  \\\  \   \ \  \  
  \ \  \\\  \ \  \|\__\_\  \ \  \_|\ \ \  \\  \|   \ \  \   \/  /  /   \ \  \|\  \ \  \\\  \   \ \  \ 
   \ \_____  \ \____________\ \_______\ \__\\ _\    \ \__\__/  / /      \ \_______\ \_______\   \ \__\
    \|___| \__\|____________|\|_______|\|__|\|__|    \|__|\___/ /        \|_______|\|_______|    \|__|
          \|__|                                          \|___|/                                      

"""

#imports
from importlib.resources import contents
import discord
import os
from discord.ext import commands
import random
import time
import asyncio

client = discord.Client()

#discord bot token
TOKEN = 'X'

#Prefix 
bot = commands.Bot(command_prefix="#")


#bot status in discord client and server ready message
@bot.event
async def on_ready():
    activity = discord.Game(name="#help", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot is ready!")

#coinflip
@bot.command(pass_context=True)
async def coinflip(ctx):
    """Flip a virtual coin!"""
    variable = [
        "```Heads!```",
        "```Tails!```",]
    await ctx.channel.send("{}".format(random.choice(variable)))

#dice
@bot.command(pass_context=True)
async def dice(ctx):
    """Throws a virtual 6 sided die."""
    variable = [
        "```1```",
        "```2```",
        "```3```",
        "```4```",
        "```5```",
        "```6```",
               ]
    await ctx.channel.send("{}".format(random.choice(variable)))

#ping
@bot.command()
async def ping(ctx):
    """Check the bot ping!"""
    await ctx.send(f"{client.latency}")
    if round(client.latency * 1000) <= 50:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(client.latency *1000)}** milliseconds!", color=0x44ff44)
    elif round(client.latency * 1000) <= 100:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(client.latency *1000)}** milliseconds!", color=0xffd000)
    elif round(client.latency * 1000) <= 200:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(client.latency *1000)}** milliseconds!", color=0xff6600)
    else:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(client.latency *1000)}** milliseconds!", color=0x990000)
    await ctx.send(embed=embed)


#weclome message dm
@client.event
async def on_member_join(member, ctx):
    await ctx.author.send("```Hello there!```")
    

#membercount
@bot.command()
async def membercount(ctx):
    """Check the server membercount!"""
    embed = discord.Embed(
            title=('Membercount'),
            description =(f'There are currently **{ctx.guild.member_count}** members in the server!'),
            
            color= discord.Colour.dark_blue()
        )
    embed.set_footer(text='QWERTY')
    embed.set_thumbnail(url='')
    await ctx.send(embed=embed)
    

#bot-commands
@bot.command(aliases=['about'])
async def info(ctx):
    """About the bot!"""
    embed = discord.Embed(
            title=('Info'),
            description =(f'A Discord bot made by QwertyIsThinking#1587 for moderation and for fun! It is self hosted and is made with Discord.py!'),
            
            color= discord.Colour.dark_blue()
        )
    embed.set_footer(text='QWERTY')
    embed.set_thumbnail(url='')
    await ctx.send(embed=embed)
    

#bot invite
@bot.command(pass_context=True)
async def invite(ctx):
    """Invite this bot to your server!"""
    
    embed = discord.Embed(
            title=('Invite'),
            description =(f'Here is the invitation link: https://discord.com/api/oauth2/authorize?client_id=927841410319781908&permissions=449160039488&scope=bot'),
            
            color= discord.Colour.dark_blue()
        )
    embed.set_footer(text='QWERTY')
    embed.set_thumbnail(url='')
    await ctx.send(embed=embed)

#test the bot to see if it is online
@bot.command(aliases=['test'])
async def status(ctx):
    """Is the bot okay?"""
    embed = discord.Embed(
            title=('Status'),
            description =(f'The bot is online and everything SEEMS to be fine!'),
            
            color= discord.Colour.dark_blue()
        )
    embed.set_footer(text='QWERTY')
    embed.set_thumbnail(url='')
    await ctx.send(embed=embed)

#your discord server invite, in this case, it is my discord server invite
@bot.command(pass_context=True)
async def server(ctx):
    """The creator's main server!"""
    await ctx.channel.send('Here is the server invite for main server: https://discord.gg/JE2AfPm2Yu')

#the discord bot support server, you can make your own support server if you are the one hosting it
@bot.command(pass_context=True)
async def support(ctx):
    """Support server!"""
    await ctx.channel.send('Here is the support server link: https://discord.gg/7RSxKSaN68')
@bot.command(pass_context = True)

#owner
@commands.is_owner()
async def owner(ctx):
    """Shows if you are the true owner of the bot or not."""
    await ctx.channel.send('```If you executed this command, then you are the owner of this bot!```')

#badwords filter 
with open('badwords.txt') as file:
    file = file.read().split()

@bot.event
async def on_message(message):
    mybot = bot.get_user('X')

    if message.author is mybot:
        return

    flag = False
    for badword in file:
        if badword in message.content.lower():
            await message.delete()
            await message.channel.send(f'{message.author.mention}! Foul language.')
            flag = True

    if not flag:
        await bot.process_commands(message)

#repeat
@bot.command()
async def  repeat(ctx, *, message):
        """Repeats what you type in."""
        
        await ctx.channel.send(message)
       
#dms
@bot.command(pass_context = True)
@commands.is_owner()
async def setprefix(ctx, prefix):
       
    bot.command_prefix = prefix
    await ctx.send(f"Prefix changed to ``{prefix}``")
    await ctx.author.send("Alert! Prefix changed to ``{prefix}``!")

#timer
@bot.command()
async def timer(ctx, time: int):
    """Timer(seconds) after the prefix(no.)-May be laggy."""
    await ctx.send("Timer started")
    def check(message):
        return message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == "cancel"
    try:
        m = await bot.wait_for("message", check=check, timeout=time)
        await ctx.send("Timer cancelled")
    except asyncio.TimeoutError:
        await ctx.channel.send('Timer is ringing {}!'.format(ctx.author.mention))



    
bot.run(TOKEN)
client.run(TOKEN)
