import discord
from discord.ext import commands
import json
from requests import get
token = "ODc1NDk4NDcyOTk5MTI0OTky.YRWZfQ.sHaLiEwaLD0stW70uo4txEutCFQ"

client = commands.Bot(command_prefix=".",intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Logged in! Fuck me daddy.")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=".h | Made by: Paper#7042"))

@client.command()
async def h(ctx):
    helpmenu=discord.Embed(title="**Help Menu - -**", description=".h ‣ This message. \n .clear ‣ Clears messages \n .meme ‣ Meme command", color=0x341a4a)
    await ctx.send(embed=helpmenu)

@client.command()
async def rules(ctx):
    embed=discord.Embed(title="**RULES - -**", description="The rules of the server!", color=0x341a4a)
    embed.set_author(name="Paper | 🌴 Chilling 🌴")
    embed.add_field(name="No Racism", value="Any kind of racism is not allowed!", inline=True)
    embed.add_field(name="Swearing", value="In this server we allow swearing!", inline=True)
    embed.add_field(name="Intro", value="After you read the rules, please make an introduction about yourself!", inline=False)
    embed.add_field(name="Discord ToS", value="Please follow Discord's Terms of Service!", inline=False)
    embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)

@client.command()
async def meme(ctx):
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content)
    meme = discord.Embed(title=f"{data['title']}", Color = discord.Color.red()).set_image(url=f"{data['url']}")
    await ctx.send(embed=meme)

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send("Messages has been removed!", delete_after=3)

@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:

        with open('reactrole.json') as react_file:

            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):

        with open('reactrole.json') as react_file:

            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

                    await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

@client.command()
async def reactrole(ctx, emoji, role: discord.Role,*,message):
    emb = discord.Embed(description=message, color=0x341a4a)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role= {
            'role_name':role.name,
            'role_id':role.id,
            'emoji':emoji,
            'message_id':msg.id
        }

        data.append(new_react_role)


    with open('reactrole.json', 'w') as j:
        json.dump(data,j,indent=4)

client.run(token)