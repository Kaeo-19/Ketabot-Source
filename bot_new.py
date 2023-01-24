"""
Copyright 2019 Kaeo-19, Nasanian


Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import discord
from discord.utils import get
from discord.ext import commands
import datetime
import logging
import json
from random import randint
import requests
from bs4 import BeautifulSoup
import asyncio

__version__ = '1.0.0r0'
#Bot Intents (used for things like welcoming new members and stuff.)
intents = discord.Intents.all()

#Init bot
bot = commands.Bot(command_prefix='>', description="This is a Helper Bot", intents=intents)

#Load the token file.
with open("token.txt" ,"r") as tokenfile:
    token = str(tokenfile.read())

@bot.event
async def on_ready():
    print("Bot started!")
    print("Version: {}".format(__version__))

@bot.event
async def on_member_join(member):
    print("Recognised that a member called " + member.name + " joined")
    await bot.get_channel(789561208130895898).send(f"{member.name} has joined")

@bot.event
async def on_member_leave(member):
    print("Recognised that a member called " + member.name + " left")
    await bot.get_channel(789561208130895898).send(f"{member.name} has left :c")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 789561208130895898:
        if payload.emoji.name == "⭐":
            channel = bot.get_channel(789561208130895898)
            message = await channel.fetch_message(payload.message_id)
            reaction = get(message.reactions, emoji=payload.emoji.name)
            if reaction and reaction.count > 3:
                channel = ctx.get_channel(789624745200582677)
                await ctx.send(message)

#
# Bot Chat Embeds Section
#
 
class chat_embeds:
    """Figured a dedicated class would be the neatest way to organize these and cut down on useless code."""
    def perm_embed(acceptable_rank: str = None) -> str:
        embed = discord.Embed(title="Permissions Error!", description="It appears you do not have the neccesary permissions/role to submit this command!", color=discord.Color.red())
        embed.add_field(name="Roles that can complete this command", value=str(acceptable_rank))

        return embed

#
# Bot command sections
#

################ Misc. Commands ################
@bot.command(aliases=["i"])
async def info(ctx):
    """
    Usage: info /i
    Permissions Group: everyone.
    Displays server information
    """
    logging.info("{} initiated info command".format(ctx.author.id))
    async with ctx.typing():

        #Generate the rich format response with server information
        embed = discord.Embed(title=f"{ctx.guild.name}", description="Hail satan", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
        embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
        embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
        embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
        embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
        embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")

    await ctx.send(embed=embed)

@bot.command(aliases=["wikisearch", "wikipedia"])
async def ws(ctx,query1):
    """
    Usage: ws /wikisearch/wikipedia [Query]
    Permissions Group: everyone.
    Searches wikipedia with the given query and returns the page.
    """
    
    async with ctx.typing():


        #Fetch the appropriate wikipedia page
        resp = requests.get("https://en.wikipedia.org/wiki/" + query1.capitalize())
        
        #Parse the html page using bs4's html parser
        html = BeautifulSoup(resp.text, 'html.parser')

        paragraphs = html.select('p')
        text = ''.join([para.text for para in paragraphs[0:4]])

        embed= discord.Embed(title="Query", description=str(text))
        embed.add_field(name="link", value = str(resp), inline=True)


        await ctx.send(embed=embed)

@bot.command(aliases=["pt","lsrp","mmpi2"])
async def tests(ctx):
    """
    Usage: tests /pt/lsrp/mmpi2
    Permissions Group: everybody.
    Gives you a list of online psyche tests
    """
    
    psyche_tests = {
    "https://openpsychometrics.org/tests/SD3/",
    "htps://openpsychometrics.org/tests/LSRP.php",
    "https://www.truity.com/test/big-five-personality-test",
    "https://www.16personalities.com/free-personality-test",
    "https://openpsychometrics.org/tests/SD3/"
    }

    #Convert the array to string, each link seperated on a newline
    outputb = '\n'.join(psyche_tests)
    async with ctx.typing():
        embed = discord.Embed(title="Psyche Tests", description="{}".format(outputb), timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
        embed.add_field(name="disclaimer", value = "These should not be used as the formal evaluation tests@ These are simply online reveiw material at best,")
        await ctx.send(embed=embed)


@bot.command()
async def coin_flip(ctx):
    """
    Usage: cf
    Permissions Group: everybody.
    Pseudorandom coin flip generator.
    """
    #Use pythons pseudorandom number generator to pick between -1 (tails) and 1 (heads)
    async with ctx.typing():
        coin = randint(0, 1)
        if coin == 0:
            await ctx.send(embed=discord.Embed(title="Coin Flipper", description="f{ctx.message.author} flipped tails", timestamp=datetime.datetime.utcnow(), color=discord.Color.red()))
        else:
            await ctx.send(embed=discord.Embed(title="Coin Flipper", description="f{ctx.message.author} flipped heads", timestamp=datetime.datetime.utcnow(), color=discord.Color.red()))
            

################ chat commands ################
@bot.command()
async def delete(ctx, amount: int = None):
    """
    Usage: delete [amount (int)]
    Permissions Group: Moderator or higher.
    Deletes messages in a channel. If "all" is submitted, it will purge the entire channel. If nothing is submitted, only ten messages are deleted.
    """
    role_admin = discord.utils.get(ctx.guild.roles, name="Admin"); role_mod = discord.utils.get(ctx.guild.roles, name="Mod")
    if role_admin or role_mod in ctx.author.roles:
        if amount is None:
            await ctx.channel.purge(limit=10)
        elif amount == "all":
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=int(amount))
    else:
        await ctx.send(embed=chat_embeds.perm_embed("Moderator+")) #Send a permissions error if a regular user without mod/admin role attempts to use this command.

################ Admin/Moderator Commands ################
@bot.command() #Work on making the mutes have timers that run in the background.
async def mute(ctx, member: discord.Member, reason = None):
    """
    Usage: mute [member name] (reason) 
    Permissions Group: Moderator or higher.
    Mutes a user. Generally it's good practice to add a reason, just so if a user complains later about being muted to another moderator there can be an explanation why.
    """
    role_admin = discord.utils.get(ctx.guild.roles, name="Admin"); role_mod = discord.utils.get(ctx.guild.roles, name="Mod")
    role = discord.utils.get(ctx.guild.roles, name='Muted') #Add the muted role, which basically sets the chat perms to 0
    if reason is None:
        reason = "You were muted for {} for Non-compliance.".format(f"{ctx.guild.name}")

    
    await member.add_roles(role)
    embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
    await ctx.send("User muted!")

@bot.command()
async def tempmute(ctx, member: discord.Member, time: int = 5, d: str = "m"):
    """
    Usage: tempmute tmute/tempm/ [Member Name] (Time:Five minutes if None)
    Permissions Group: Moderator or higher.
    Temporarily mutes a user
    """
    mute_roll = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(mute_roll)
    await ctx.send(embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6))

    if d is "s":
        await asyncio.sleep(time)
    if d is "m":
        await asyncio.sleep(time*60)
    if d is "h":
        await asyncio.sleep(time*60*60)
    if d is "d":
        await asyncio.sleep(time*60*60*24)

    await member.remove_roles(mute_roll)
    
@bot.command()
async def unmute(ctx, member: discord.Member, reason: str = None):

    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    embed=discord.Embed(title="User Unmuted!", color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command()
async def kick(ctx, member: discord.Member, reason: str = None):
    role_admin = discord.utils.get(ctx.guild.roles, name="Admin"); role_mod = discord.utils.get(ctx.guild.roles, name="Mod")
    if role_admin or role_mod in ctx.author.roles:
         await member.kick()

@bot.command()
async def av(ctx, member: discord.Member):
    await ctx.send(str(member.avatar_url))



bot.run(token)
