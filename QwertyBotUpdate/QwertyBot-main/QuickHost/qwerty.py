#imports
from ast import Return
from importlib.resources import contents
import discord
import os
from discord.ext import commands
import random
import numpy
import time
import re
import string
import asyncio
import json
import aiohttp

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
#still does not work
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
#does not work
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
#need to figure out how to get heroku error details in discord via the heroku api
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

#nicknames
@bot.command()
@commands.has_permissions(administrator = True)
async def nickname(ctx, m: discord.Member, *, newnick):
    """A nickname command for admins!"""
    await m.edit(nick=newnick)
    await ctx.send('Nickname changed.')

#licence
@bot.command(aliases=['terms'])
async def licence(ctx):
    """Licence!"""
    embed = discord.Embed(
            title=('Info'),
            description =(f'This bot is distributed under the GPL 3.0 licence. Read the terms and conditions before using the code.'),
            
            color= discord.Colour.dark_blue()
        )
    embed.set_footer(text='QWERTY')
    embed.set_thumbnail(url='')
    await ctx.send(embed=embed)
    
#github
@bot.command(aliases=['source'])
async def github(ctx):
    """The GitHub page!"""
    await ctx.channel.send('https://github.com/QwertyIsCoding/QwertyBot')

# When a member joins, the bot DM's them a message
@client.event
async def on_member_join(member):
    await client.send_message(member, 'Welcome to the server {}, Enjoy your stay! Also, Check out the rules and feel free to take prt in server events!'.format(member.name))



@bot.command(help = "Prints details of Server")
async def details(ctx):
    owner=str(ctx.guild.owner)
    region = str(ctx.guild.region)
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    desc=ctx.guild.description
    
    embed = discord.Embed(
        title=ctx.guild.name + " Server Information",
        description=desc,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)

    members=[]
    async for member in ctx.guild.fetch_members(limit=150) :
        await ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name,str(member.status),str(member.joined_at)))

    

#this is buggy
@bot.event
async def on_member_join(member):
     for channel in member.guild.text_channels :
         if str(channel) == "general" :
             on_mobile=False
             if member.is_on_mobile() == True :
                 on_mobile = True
             await channel.send("Welcome to the Server {}!!\n On Mobile : {}".format(member.name,on_mobile))             


#make a command to check  user's roles
#this is not working yet
@bot.command()
async def roles(ctx, member: discord.Member):
    """Check user's roles!"""
    roles = [role for role in member.roles]
    embed = discord.Embed(
        title=f"{member}'s roles",
        description="\n".join(roles),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

#make a command for a calculator in discord and round off the answer
@bot.command()
async def calc(ctx, *, equation):
    """Calculate anything!"""
    try:
        answer = eval(equation)
    except Exception:
        await ctx.send("Invalid equation!")
        return
    embed = discord.Embed(
        title="Calculator",
        description=f"{equation} = {answer}",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)
    

#make a command to search for gifs
@client.command(pass_context=True)
async def giphy(ctx, *, search):
    embed = discord.Embed(colour=discord.Colour.blue())
    session = aiohttp.ClientSession()

    if search == '':
        response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=API_KEY_GOES_HERE')
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
    else:
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=API_KEY_GOES_HERE&limit=10')
        data = json.loads(await response.text())
        gif_choice = random.randint(0, 9)
        embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

    await session.close()

    await client.send_message(embed=embed)

#number guessing game 
@commands.command()
async def guess(self, ctx):
    number = random.randint(0, 100)
    for i in range(0, 5):
        await ctx.send('guess')
        response = await self.bot.wait_for('message')
        guess = int(response.content)
        if guess > number:
            await ctx.send('bigger')
        elif guess < number:
            await ctx.send('smaller')
        else:
            await ctx.send('true')
    
bot.run(TOKEN)
client.run(TOKEN)
