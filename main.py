import discord
from discord.ext import commands
from discord import Intents
import pymongo
import json
import os
from discord.utils import get

intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)
prefix = bot.command_prefix

mongoclient = pymongo.MongoClient('mongodb+srv://offset:QwK0eDxOnUcNQJ8h@cluster0.vle2thu.mongodb.net/?')
db = mongoclient['Cluster0']  # Make sure the case matches your actual database name
collection = db['user_data']

def clear_screen():
    # windows
    if os.name == 'nt':
        os.system('cls')
    # unix / mac
    else:
        os.system('clear')


@bot.event
async def on_ready():
    clear_screen()
    print("Ready")
    # await bot.change_presence(activity=discord.Streaming(name="luhrokkowt", url='https://www.twitch.tv/r3zk1_91'))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Offset"))    # await bot.change_presence(activity=discord.Game(name="in Offset", type=1))


@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    # await ctx.send(f'Latency: {latency}ms')
    embed = discord.Embed(
        description=f'Latency: {latency}ms',
        color=0xff1100
    )

    await ctx.send(embed=embed)

# Moderation cmd
# ban cmd 
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)

# kick cmd
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)

# unban cmd
@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

# avatar stalking (Put in Embed to hide url)
    
@bot.command(name='pfp', aliases=['avatar', 'av'])
async def pfp(ctx, user: discord.User = None):
    # if no user is given it defaults to the sender
    user = user or ctx.author

    # avatar url
    avatar_url = user.avatar_url if user.avatar else user.default_avatar_url

    # color and users name
    embed = discord.Embed(
        title=f"{user.display_name}'s Avatar",
        color=0xff1100
    )

    # set the avatar as the image in the embed
    embed.set_image(url=avatar_url)

    # send the embed
    await ctx.send(embed=embed)

# Banner stalking

@bot.command()
async def banner(ctx, user: discord.Member = None):
    user = user or ctx.author

    req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = req["banner"]

    # If statement because the user may not have a banner
    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
        embed = discord.Embed(
            title=f'{user.display_name}\'s Banner',
            color=0xff1100
        )

        # send embed
        embed.set_image(url=banner_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
        title=f"{user.display_name} does not have a banner / does not have nitro and has a default banner",
        color=0xff1100
    )
        await ctx.send(embed=embed)


@bot.command(aliases= ['mc', 'memcount', 'mcount'])
async def membercount(ctx):
    guild = ctx.guild
    member_count = guild.member_count
    embed = discord.Embed(
        description=f'*This server currently has {member_count} members.*',
        color=0xff1100
    )

    # send embed
    await ctx.send(embed=embed)

@bot.command(aliases=['il', 'inv', 'link'])
async def invitelink(ctx):
    link = await ctx.channel.create_invite(max_age = 300)
    await ctx.send(f'{link}')
    # embed = discord.Embed(
    #     title=f'Here is a invite link to {ctx.message.guild.name}',
    #     description=f'{link}',
    #     color=0x2b2d31
    # )

    # # send embed
    # await ctx.send(embed=embed)

# AFK CMD

# afk_users = {}

# @bot.event
# async def on_message(message):
#     if not message.author.bot:
#         user_id = str(message.author.id)

#         if user_id in afk_users:
#             # Calculate duration
#             duration = datetime.now() - afk_users[user_id]['timestamp']
#             duration_str = format_timedelta(duration)
#             embed = discord.Embed(
#                 description=f"*{message.author.mention}, you are no longer AFK.\nYou were away for {duration_str}.*",
#                 color=0xff1100
#             )
#             await message.channel.send(embed=embed)
#             del afk_users[user_id]  # Remove user from AFK list
#         else:
#             user_data = economy_collection.find_one({"user_id": user_id})
#             if user_data:
#                 embed = discord.Embed(
#                     description=f"*{message.author.mention}, you are currently AFK.\nReason: {user_data['reason']}*",
#                     color=0xff1100
#                 )
#                 await message.channel.send(embed=embed)

#     await bot.process_commands(message)

# def format_timedelta(delta):
#     days, seconds = delta.days, delta.seconds
#     hours, remainder = divmod(seconds, 3600)
#     minutes, seconds = divmod(remainder, 60)

#     if days:
#         return f"{days} days, {hours} hours, {minutes} minutes"
#     elif hours:
#         return f"{hours} hours, {minutes} minutes"
#     elif minutes:
#         return f"{minutes} minutes"
#     else:
#         return f"{seconds} seconds"

# @bot.command(name='afk', aliases=['set_afk'])
# async def set_afk(ctx, *, reason=""):
#     user_id = str(ctx.author.id)

#     if user_id in afk_users:
#         # User is already AFK, update the reason
#         afk_users[user_id]['reason'] = reason
#     else:
#         # User is not in the AFK list, add them
#         afk_users[user_id] = {'reason': reason, 'timestamp': datetime.now()}

#     embed = discord.Embed(
#         description=f"*{ctx.author.mention} is now AFK.\nReason: {reason}*",
#         color=0xff1100
#     )
#     await ctx.send(embed=embed)

# Snipe cmd 

# snipe_data = {}

# @bot.event
# async def on_message_delete(message):
#     channel_id = message.channel.id
#     snipe_data[channel_id] = [(message.content, message.author.id, message.created_at)]


# @bot.command(aliases=['s', 'sni'])
# async def snipe(ctx, index: int = 1):
#     channel_id = ctx.channel.id

#     if channel_id not in snipe_data or not snipe_data[channel_id]:
#         embed = discord.Embed(description="*There's nothing to snipe.*", color=0xff1100)
#         await ctx.send(embed=embed)
#         return

#     sniped_messages = snipe_data[channel_id]

#     if index > len(sniped_messages):
#         embed = discord.Embed(description="*Invalid snipe index.*", color=0xff1100)
#         await ctx.send(embed=embed)
#         return

#     content, author_id, created_at = sniped_messages[index - 1]

#     user = await bot.fetch_user(author_id)

#     embed = discord.Embed(color=0xff1100)
#     member = ctx.message.author
#     userAvatar = member.avatar.url
#     embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=userAvatar)
#     embed.add_field(name="Sniped Message", value=content)
#     embed.set_footer(text=f"{created_at.strftime('%Y-%m-%d %H:%M:%S')}")

#     await ctx.send(embed=embed)

@bot.command(aliases=['h5', '5', 'gj'])
async def highfive(ctx):
    await ctx.send("https://tenor.com/view/high-five-patrick-star-spongebob-squarepants-the-patrick-star-show-yes-gif-22559195")

# clear cmd
@bot.command(aliases=['purge', 'delete'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = -1):
    if amount == -1:
        embed = discord.Embed(
            description=f'**Make sure to add the number of messages to purge!**',
            color=0xff1100
        )
        await ctx.send(embed=embed)
    else:
        await ctx.channel.purge(limit=amount)


# API_KEY = 'aRVzDOvBcZd4h1mvhUyoxyANH'
# API_SECRET_KEY = 'eL7V0vaW4eTH581U74wGPtyXAssWojyXrrB0yKrhKnfIBQXDgZ'

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore messages from bots

    await bot.process_commands(message)  # Process commands

    # Increment message count for the user
    user_id = str(message.author.id)
    user_data = collection.find_one({'_id': user_id})

    if not user_data:
        user_data = {'_id': user_id, 'messages': 0, 'level': 1, 'messages_to_level_up': 25}
        collection.insert_one(user_data)

    user_data['messages'] += 1

    # Check if the user should level up
    if user_data['messages'] >= user_data['messages_to_level_up']:
        user_data['level'] += 1
        user_data['messages_to_level_up'] *= 2  # Double the required messages for the next level
        await message.channel.send(f'Congratulations, {message.author.mention}! You leveled up to level {user_data["level"]}.')

        # Update user data in MongoDB
        collection.update_one({'_id': user_id}, {'$set': user_data})

@bot.command(name='level')
async def display_level(ctx):
    user_id = str(ctx.author.id)
    user_data = collection.find_one({'_id': user_id})
    level = user_data['level']
    # await ctx.send(f'{ctx.author.mention}, your current level is {level}.')
    
    embed = discord.Embed(
        description=f'*{ctx.author.mention}, your current level is {level}.*',
        color=0xff1100
    )
    
    await ctx.send(embed=embed)


# securing the token in another file
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

TOKEN = config_data.get('TOKEN', '')
bot.run(TOKEN)