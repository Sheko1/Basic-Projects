import re
from twitchio.ext import commands

CHANNELS = ["#channel_name"]  # channels that the bot will connect [must be list or tuple]
NICK = "bot username"  # your bot channel username

bot = commands.Bot(
    irc_token="",  # your oauth code
    client_id="",  # your app id
    nick=NICK,
    prefix="!",  # command prefix
    initial_channels=CHANNELS
)

permit_users = []


@bot.event
async def event_ready():
    print("Bot is ready")
    ws = bot._ws
    for channel in CHANNELS:
        await ws.send_privmsg(channel, "/me is online")   # bot sends a message that he is online


@bot.event
async def event_message(ctx):
    if ctx.author.name.lower() == NICK:
        return

    await bot.handle_commands(ctx)

    # check if there is a link in the message
    match = re.search(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]"
                      r"+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>"
                      r"]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<"
                      r">]+|(\([^\s()<>]+\)))*\)|[^\s`!()"
                      r"\[\]{};:'\".,<>?«»“”‘’]))", ctx.content)

    if match and "https://osu.ppy.sh/beatmapsets/" not in match.group(1) and ctx.author.name\
            not in permit_users and not ctx.author.is_mod:

        await ctx.channel.timeout(ctx.author.name, 60, "link post")
        await ctx.channel.send(f"Don't post links {ctx.author.name}")
        # if there is a link in the user message and its not a osu! map request, he receive a timeout for 60 seconds


@bot.command(name="req")
async def request(ctx, link=None):
    if link:
        if "https://osu.ppy.sh/beatmapsets/" in str(link):
            await ctx.send(f"Request has been sent {ctx.author.name}")
            print(f"{link} - request from {ctx.author.name}")
            # prints the osu beat map link and who requested it if the link is correct

    else:
        await ctx.send(f'!req "osu! map link" - to request a map')


@bot.command(name="clear")
async def clear(ctx):
    if ctx.author.is_mod:
        await ctx.channel.clear()
        # clears the entire chat if the command is used by a moderator


@bot.command(name="ban")
async def ban(ctx, user=None, *args):
    if ctx.author.is_mod:
        if user and args:
            await ctx.channel.ban(user, " ".join(args))
            await ctx.send(f"{user} has been banned for {' '.join(args)}")

        else:
            await ctx.send(f'{ctx.author.name} -> !ban "user" "reason"')
            # ban a user if command is used by mod


@bot.command(name="unban")
async def unban(ctx, user):
    if ctx.author.is_mod:
        await ctx.channel.unban(user)
        # unban user if command is used by mod


@bot.command(name="permit")
async def permit(ctx, user):
    if ctx.author.is_mod:
        permit_users.append(user)
        await ctx.send(f"{user} is permitted to post links")
        # you can permit a user to post links if command is used by mod


@bot.command(name="unpermit")
async def permit(ctx, user):
    if ctx.author.is_mod:
        permit_users.remove(user)
        await ctx.send(f"{user} is no longer permitted to post links")
        # you can remove the permission from the user if command is used by mod

bot.run()
