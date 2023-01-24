"""
Copyright 2019 Kaeo-19, Nasanian


Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

"""
#TODO:
- Gambling Games
* Blackjack
* Poker
* Roulette
* slots
- Economy Shit
Optional participation: One time command can be run, ECO on, once this command is ran by the player, they are forced to partake in the economy.
1x loan per week, if not paid back by end of week, loan + random interest rate gets added to ur debt.
debt reset options can be purchased, reset all money to 0.
Random daily tax amount. 
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

#Local libraries
import utils.users as users
#import utils.eco as eco


intents = discord.Intents.all()
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='>', description="This is a Helper Bot", intents=intents)
token = "" #Please make a bot instance and add your own token here.

@bot.event
async def on_ready():
    print("Loading configuration file")
    with open('./bot_settings.json', 'r+') as config:
        config = json.loads(config.read())

    print("Welcome to {} | Version {}".format(str(config['general']['name']), str(config['general']['version'])))
    print("Starting console logger...")
    logging.basicConfig(format=str(config['general']['name']) + '[' + '%(asctime)s' + ']' + ' %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    
    
@bot.event
async def on_member_join(member):
    """
    This is where the action happens when a user joins
    """
    
    print("Recognised that a member called " + member.name + " joined")
    if config['general']['Create_Profile_On_Join'] is True:
        logging.info("Created profile for new member: [{}]({}}".format(str(member.id), member.Name))
    else:
        logging.warn("Profile creation on first join is disabled! Users will have to manually create their profile if they wish to partake in the bot activities!")
        
        users.profile_create(member.id, member.name, member.roles)
        
    await bot.get_channel(789561208130895898).send(f"{member.name} has joined")
  
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
@bot.event
async def on_reaction_add(reaction, user):
    #if reaction.message.id == 789580051246743602:
    if reaction.emoji is '🙃':
        if reaction.count > 0:
            print("YESSS")
            channel = ctx.get_channel(789624745200582677)
            await ctx.send(reaction.message)
#
# Bot Chat Embeds Section
#
 
class chat_embeds:
    """Figured a dedicated class would be the neatest way to organize these and cut down on useless code."""
    def perm_embed(acceptable_rank: str = None, description: str = None) -> str:
        embed = discord.Embed(title="Permissions Error!", description="It appears you do not have the neccesary permissions/role to submit this command!", color=discord.Color.red())
        embed.add_field(name="Roles that can complete this command", value=str(acceptable_rank))
        if description != None:
            mbed.add_field(value=description)
        
        return embed1



################################################
# Bot command sections
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
        embed.add_field(name="disclaimer", value = "These should not be used as the formal evaluation tests These are simply online reveiw material at best,")
        await ctx.send(embed=embed)


@bot.command(aliases=["cf"])
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
            
@bot.command(aliases=["dmsgs"])
async def delete(ctx, amount: int = None):
    """
    Usage: delete [amount (int)]
    Permissions Group: Moderator or higher.
    Deletes messages in a channel. If "all" is submitted, it will purge the entire channel. If nothing is submitted, only ten messages are deleted.
    """
    role_admin = discord.utils.get(ctx.guild.roles, id=int(config['roles']['admin'])); role_mod = discord.utils.get(ctx.guild.roles, id=int(config['roles']['mod']))
    if role_admin or role_mod in ctx.author.roles:
        if amount is None:
            await ctx.channel.purge(limit=10)
        elif amount == "all":
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=int(amount))
    else:
        await ctx.send(embed=chat_embeds.perm_embed("Moderator+")) #Send a permissions error if a regular user without mod/admin role attempts to use this command.
                       
@bot.command()
async def announce(ctx, message):
    """
    Usage: announce (message)
    Permission Group: Moderator or higher.
    """
    role_admin = discord.utils.get(ctx.guild.roles, id=int(config['roles']['admin'])); role_mod = discord.utils.get(ctx.guild.roles, id=int(config['roles']['mod']))
    if role_admin or role_mod in ctx.author.roles:
        text_channel_list = []
        for server in Client.servers:
            for channel in server.channels:
                if channel.type == 'Text':
                    text_channel_list.append(channel)
                    channel = client.get_channel(channel)
                    await channel.send(message, delete_after=5)
                    
    else:
        await ctx.send(embed=chat_embeds.perm_embed("Moderator+"))
                 
################### Admin/Moderator Commands ################
@bot.command() #Work on making the mutes have timers that run in the background.
async def mute(ctx, member: discord.Member, reason = None):
    """
    Usage: mute [member name] (reason) 
    Permissions Group: Moderator or higher.
    Mutes a user. Generally it's good practice to add a reason, just so if a user complains later about being muted to another moderator there can be an explanation why.
    """
    role_admin = discord.utils.get(ctx.guild.roles, id=int(config['roles']['admin'])); role_mod = discord.utils.get(ctx.guild.roles, id=int(config['roles']['mod']))
    role = discord.utils.get(ctx.guild.roles, id=int(config['roles']['muted'])) #Ad4d the muted role, which basically sets the chat perms to 0
    if role_admin or role_mod in ctx.author.roles:  
        if reason != None:
            reason = "{} is muted for {}".format(str(member.name), reason)
        else:
            reason = "{} is muted for non-compliance.".format(str(member.name))

        await member.add_roles(role)
        embed=discord.Embed(title="User Muted!", description=reason, color=0x5c000e)
        await ctx.send("User muted!", delete_after=5)
    else:
        await ctx.send(embed=chat_embeds.perm_embed("Moderator+"))
@bot.command()
async def tempmute(ctx, member: discord.Member, time: int = 5, d: str = "m"):
    """
    Usage: tempmute tmute/tempm/ [Member Name] (Time:Five minutes if None)
    Permissions Group: Moderator or higher.
    Temporarily mutes a user
    """
    role_admin = discord.utils.get(ctx.guild.roles, id=int(config['roles']['admin'])); role_mod = discord.utils.get(ctx.guild.roles, id=int(config['roles']['mod']))
    
    mute_roll = discord.utils.get(ctx.guild.roles, name="Muted")
    member_id = int(member.id)
    if "/" not in users_dir:
        users_dir = str(users_dir) + "/"
    else:
        logging.info("Users directory parsed correctly")

    if config['general']['toxic_user_role'] is 'true':
        with open(str(users_dir) + str(member_id)) as user_file:
            user_file = json.loads(user_file.read())
            if user_file['mute_count'] >= 3:
                #Make an algorithm that trains off of toxic user data and determines which users are toxic and not
                member.add_roles(toxic_user)
    else:
        logging.info("Toxic User Role is turned off! (For more information, run binfo tur in the bot terminal")


    if role_admin or role_mod in ctx.author.roles:
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

    else:
        await ctx.send(embed=chat_embeds.perm_embed("Moderator+"))

    await member.remove_roles(mute_roll)
    
    
@bot.command()
async def unmute(ctx, member: discord.Member, reason: str = None):
    """
    Usage: unmute [Member Name]
    Permissions Group: Moderator or higher.
    Unmutes a user
    """
    
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    role_admin = discord.utils.get(ctx.guild.roles, id=int(config['roles']['admin'])); role_mod = discord.utils.get(ctx.guild.roles, id=int(config['roles']['mod']))
    if reason != None:
        embed = discord.Embed(title="User Unmuted!", description="**{}** was unmuted.", color=discord.Color.blue())
        embed.add_field(name="Reason", value=str(reason)) #Force type conversion to avoid command injection

    if role_admin or role_mod in ctx.author.roles:
        await member.remove_roles(role)     
        await ctx.send(embed=embed, delete_after=5)

@bot.command()
async def kick(ctx, member: discord.Member, reason: str = None):
    """
    Usage: kick [Member name] [Reason (None)]
    Permissions Group: Moderator or higher
    Kicks a user. You can add a reason, but the default is None
    """

    role_admin = discord.utils.get(ctx.guild.roles, name="Admin"); role_mod = discord.utils.get(ctx.guild.roles, name="Mod")
    if role_admin or role_mod in ctx.author.roles:
         await member.kick()
    else:
        embed=chat_embeds.perms(str(discord.utils.get(ctx.guild.roles, id=int(config['roles']['admin']))))
        await ctx.send(embed=embed)

@bot.command()
async def av(ctx, member: discord.Member):
    """
    Usage: av [Member name]
    Permissions group: any
    Returns a users avatar
    """

    embed = discord.Embed(title="{}'s Avatar".format(str(member.name)))
    await ctx.send(str(member.avatar_url))


@bot.command()
async def profile_create(ctx, member: discord.Member = None):
    """
    Usage: profile_create [Member name (admins only)]
    Permissions Group: any
    Planning on making this something that happens automatically on join, but creates a user profile that is stored on the server
    """
    
    if member is None:
        member = str(ctx.author.id) #use the authors ID if no member name is passed
    else:
        users.create_profile(member.id, member.name, member.roles)
        
    embed = discord.Embed(title="Profile Created!", description="Created a new profile for {}".format(member), color=discord.Color.blue())
    await ctx.send(embed=embed)
    
@bot.command()
async def profile_delete(ctx, member: discord.Member):
    """
    Usage: profile_delete [Member name]
    Permissions group: Moderator and above
    Deletes a profile from the server database
    """
    
    if member is None:
        role_admin = discord.utils.get(ctx.guild.roles, id=int(config['roles']['admin'])) #Obviously only administrators or higher should be able to delete profiles. (Deleting profiles also erases their debt.)
        if ctx.author.roles != role_admin:
            
            embed=chat_embeds.perms(str(discord.utils.get(ctx.guild.roles, id=int(config['roles']['admin']))), "Only administrators can delete their profiles!")

        else:
            users.profiles.delete()

@bot.command()
async def profile_view(ctx, member: discord.Member):
    """
    Usage: profile_view [Member name (none)]
    Permissions group: any
    Shows a users profile
    """
    
    if member is None:
        users.profile.view(ctx.author.id)
    else:
        #Returns the users profile saved as a json in /users
        
        profile = users.view(member.id)
        description = ["Discord Username: {}\n".format(profile[str(member.id)]["name"]),
                       "Profile Created: {}\n".format(profile[str(member.id)]["profile_created_at"]),
                       "Server Rank: {}\n".format(profile[str(member.id)]["rank"]),
                       "Messages: {}\n".format(profile[str(member.id)]["dm_status"]),
                       "Pronouns: {}\n".format(profile[str(member.id)]["gender"]),
                       "Bio: {}".format(profile[str(member.id)]["bio"]),
                       "Balance: {}".format(profile[str(member.id)]["wallet"]) #Make this an optional thing to display.
        ]

        for i in range(len(description)):
            fdescription = ""
            new_description = fdescription + description[i]
            
        embed=discord.Embed(title="{}'s profile".format(str(member.name)), description=new_description)
        await ctx.send(embed=embed)

@bot.command()
async def wallet_send(ctx, member: discord.Member, amount: int = None):
    """
    Usage: wallet_send [Member name] [Amount]
    Permissions group: any
    Sends money to a user.
    """
    if amount is None:
        logging.info("User [{}]({}) attempted to send money, but failed to specify amount!".format(str(member.id),member.Name))
        
    eco.wallet.transfer_coin(member.id, amount)

@bot.command()
async def wallet_view(ctx, member: discord.Member):
    eco.wallet.check_wallet(member.id)

@bot.command()
async def itemprice(ctx, item: str = None):
    """
    Checks an items price in the server shop
    """
    logging.info("User [{}]({}) checked the price of item {}".format(discord.Member.id, discord.Member.name, item))
    eco.check_item_price(item)

@bot.command()
async def itemstat(ctx, item: str = None):
    """
    returns an items price, ID, and available shops
    """
    logging.info("User [{}]({}) checked the stats on item {}".format(discord.Member.id, discord.Member.name, item))
    eco.check_item_stats(item)

@bot.command()
async def openshop(ctx, member: discord.Member):
    """
    Opens a user shop. Note that config has to have AllowUserShops set to true
    """
    if config['AllowUserShops'] is False:
        logging.critical("Attempted to open a user shop for user {} but was denied because it is set to false in the config".format(member.Name))
        
    else:
        with open('./users/{}_shop'.format(str(member.id)), "w") as user_shop_file:
            print("TESTING BREAK")
            exit
            
"""


##########
#Bot events
##########

#Prints discord messages to console and logs them.
"""
@bot.event <-- Doesn't work with bot.command() for some reason.
async def on_message():

    Logs/displays messages from discord to the termninal

"""
"""
@bot.event
async def on_message(ctx):
    #Log server messages to both terminal
    logging.info(str(ctx))
"""
"""
@bot.event
async def on_member_join(self, member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)
@bot.event
async def on_ready():
    channel = bot.get_channel(789561208130895898)
    global msg
    msg = await bot.send_message(channel, "React to me!")
    await bot.add_reaction(msg, tennis)

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.user == client.user:
        return
    if reaction.message == msg and reaction.emoji == tennis:
        verified = discord.utils.get(user.server.roles, name="verified")
        await client.add_roles(user, verified)

@bot.event
async def on_reaction_remove(reaction, user):
    if reaction.message == msg and reaction.emoji == tennis:
        verified = discord.utils.get(user.server.roles, name="verified")
        await client.remove_roles(user, verified)
"""
bot.run(token)
  
