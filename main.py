import subprocess
import threading
import discord
import random
import pickle
import os
from discord.ext import commands, tasks

link_role_id = 821096795013775361
pending_codes = {}

try:
    infile = open("link_data.txt", "rb")
except FileNotFoundError:
    print("WARNING: No data found! Creating new data file...")
    infile = open("link_data.txt", "x")
    infile.close()
    users = {}
try:
    infile = open("link_data.txt", "rb")
    users = pickle.load(infile)
    infile.close()
except EOFError:
    print("WARNING: No data found in file! Using empty...")
    users = {}

def syncwithfile():
    outfile = open("link_data.txt", "wb")
    pickle.dump(users, outfile)
    outfile.close()

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=False)
client = commands.Bot(command_prefix=['!'], intents=intents)
client.remove_command("help")

@tasks.loop(minutes=1)
async def count_down_pending():
    for code in pending_codes:
        code["expiration_time"] = code["expiration_time"] - 1
        if code["expiration_time"] == 0:
            pending_codes.pop(code["code"])

@client.event
async def on_ready():
    print("[MCBE-link] running!")

@client.command()
async def linkaccount(ctx, username=None):
    if username is not None:
        code = random.randint(1, 9999)
        print(f"[MCBE-link] Link account command recieved from MC: {username} Discord: {ctx.message.author} Code: {code}")
        bds.stdin.write(f"msg {username} {ctx.message.author} wants to link their Discord account to this Minecraft account, and they can do so using this code: {code}. If this wasn't you, ignore it.\n".encode())
        bds.stdin.flush()
        await ctx.send("A message has been sent to you in-game that contains a code. Please use !code <code here>. If you aren't online, join and type !linkaccount again.")
        pending_codes[str(code)] = {
            "discord_user": ctx.message.author.id,
            "minecraft_user": username,
            "expiration_time": 5,
            "code": code
        }
    else:
        await ctx.send("Usage: !linkaccount <Minecraft username>")

@client.command()
async def code(ctx, code=None):
    if code is not None:
        try:
            if pending_codes[code]["discord_user"] == ctx.message.author.id:
                users[str(ctx.message.author.id)] = {
                    "discord_user": ctx.message.author.id,
                    "minecraft_user": pending_codes[code]["minecraft_user"]
                }
                await ctx.send("Linked!")
                bds.stdin.write(f"tag {users[str(ctx.message.author.id)]['minecraft_user']} add linked\n".encode())
                bds.stdin.flush()
                await ctx.message.author.add_roles(ctx.message.guild.get_role(link_role_id))
                try:
                    await ctx.message.author.edit(nick=pending_codes[code]["minecraft_user"])
                except:
                    pass
                dict.pop(pending_codes, code)
                syncwithfile()
        except KeyError:
            await ctx.send("Invalid code. Please try again.")

@client.command()
async def unlinkaccount(ctx):
    dict.pop(users, str(ctx.message.author.id))
    syncwithfile()
    await ctx.send("Unlinked account!")

@client.command()
async def check(ctx, member: discord.Member):
    await ctx.send(f"{member.mention}'s Minecraft account is {users[member.name]['minecraft_user']}")

def bds_thread_function(name):
    global bds
    if os.name != 'nt':
    	bds = subprocess.Popen([r"./bedrock_server"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd="bds/")
    else:
        bds = subprocess.Popen([r"bds/bedrock_server.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in bds.stdout:
        print(line.decode("utf-8").replace("\n", ""))

def input_thread_function(name):
    while True:
        user_input = input() + "\n"
        user_input = user_input.encode()
        bds.stdin.write(user_input)
        bds.stdin.flush()
        log(f'Command "{user_input.decode("utf-8")}" was sent successfully')

def modding_thread_function(name):
    pass

def log(message: str, message_type: str = "INFO"):
    print(f"[{message_type}] {message}")


bds_thread = threading.Thread(target=bds_thread_function, args=(1,))
input_thread = threading.Thread(target=input_thread_function, args=(2,))
modding_thread = threading.Thread(target=modding_thread_function, args=(3,))
input_thread.start()
modding_thread.start()
bds_thread.start()
client.run("token here")
