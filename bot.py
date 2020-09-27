import discord
from discord.ext import commands
import random
import asyncio
import os 
import ast
import requests
import datetime
import time
import aiohttp 
import dbl
import asyncpg
import async_cleverbot as ac
try:
  import jishaku
except Exception as e:
  print(e)
  print("Jishaku not found")
from paginate import paginator 

client  = commands.Bot(command_prefix = ".o")
#client.remove_command("help")
#restathereF
@client.event 
async def on_ready():
    print("ready ! no error maybe")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".ohelp "))
    st = client.get_channel(715214406967099492)
    await st.send("```i am back online```")


@client.command(name="info", help = "shows you information about the bot.", usage = ".oinfo")
@commands.is_owner()
async def _info(ctx):
   #embed = discord.Embed(title = "Nocturnal" , description = "Nocturnal is a simple made Just for fun")
   #embed.add_field(name = "server count " , value = len(client.guilds) )
   #embed.add_field(name = "total users" , value 
   print("eh")
#what

@client.command(name = "Guess The Brand " , help = "A simple brand guessing game which lets you guess the brand by thier logo", usage = ".ogtb" , aliases = ["gtb","wtb",])
async def gtb (ctx):
    def check (msg):      
        return msg.author == ctx.author and ctx.channel == msg.channel
    number = random.randint(1, 22)
    db = await client.pg_con.fetch("""SELECT * FROM gtb WHERE id = $1""",number)
    image = db[0]["link"]
    sol = db[0]["answer"]
    embed = discord.Embed(title = "which brand is that?")
    embed.set_image(url = image) 
    await ctx.send(embed=embed)
    answer = await client.wait_for("message" , timeout = 15 , check=check)
    if answer.content.lower() == sol.lower() :
       embed = discord.Embed(title = "right answers")
       embed.color = 0xE9335B
       await ctx.send(embed = embed)
    else:
       await ctx.send("WRONG")



@client.event
async def on_message_edit(before, after):

   await client.process_commands(after)





#lmao not removing this to show how dumb i was 
@client.event
async def on_dbl_vote(data):
    print(data)
    a = data["user"]
    d = await client.get_user(a)
    await d.send("THANKS FOR VOTING")

@client.command()
async def votes (ctx):
    id = ctx.author.id
    a = dbl.get_user_vote(id)
    await ctx.send(a)


@client.command()
@commands.is_owner()
async def servers(ctx):
   guild = client.guilds
   await ctx.send(f"""**Hello, I am in these guilds:**""")   
   for server in guild:

      await ctx.send(f"** {server.name}, ID**: `{server.id}`")
   await ctx.send(f"**--- END ---**")   



#BAN AND ERROR HANDLER FOR BAN 

@client.command(name = "ban" , help = "Ban the mentioned user from the guild with a optional reason " , usage = ".oban <member/id> [reason]")

@commands.has_permissions(ban_members=True, kick_members=True)
async def ban (ctx, member :discord.Member , *, reason=None ):
    await member.ban(reason=reason)
    await ctx.send (f"banned {member}")



#error handlers

@ban.error
async def ban_error(ctx, error):
    error = getattr(error, "original", error)
    
    if isinstance(error,commands.CommandInvokeError):  
        embed= discord.Embed(title= "Mission Permission " , description = "Missing permission, You do not has permission to ban the mentioned user.")
        embed.color = 0xE9335B

        await ctx.send(embed=embed , delete_after=9)
    elif isinstance(error,commands.MissingRequiredArgument):  
        embed= discord.Embed(title= "Missing Argument " , description = "Usage :` .oban (user) (reason)`")
        embed.color = 0xE9335B
        await ctx.send(embed=embed, delete_after = 9)

    elif isinstance(error,commands.BadArgument):  
        embed= discord.Embed(title= "Bad Argument " , description = "Invalid User, Please tag a valid user.\nUsage: `.oban (user) (reason)`")
        embed.color = 0xE9335B
        await ctx.send(embed=embed , delete_after = 9)

    

    
    elif isinstance(error,commands.MissingPermissions):  
        embed= discord.Embed(title= "Mission Permission " , description = "Missing permission,The bot does not has the role to ban members make sure that the bot has `ban_members` Permission .")
        embed.color = 0xE9335B
        await ctx.send(embed=embed , delete_after=13)
     
    else:
        raise error




#pokemon 
@client.command(name = "who's that pokemon" , help = "Generates a random pokemon image for guessing" , usage = ".owtp", aliases = ["gtp" , "wtp"])
async def wtp (ctx):
    
    token = "domk"
    def check (message):
      return ctx.author.id == message.author.id and ctx.channel == message.channel
    async with aiohttp.ClientSession() as cs:
         async with cs.get('https://dagpi.tk/api/wtp' ,headers = { "token" : f"""{token}"""}) as r:
            res = await r.json()  # returns dict
            embed1 = discord.Embed(title = "which pokemon is that , you got 3 tries")
            embed1.set_image(url = res["question_image"])
            oki = await ctx.send(embed = embed1)
            answer = res["pokemon"]["name"]
            embed2 = discord.Embed(title = f"""the pokemon was {res["pokemon"]["name"]}""")
            embed2.set_image(url = res["answer_image"])
 
            a = await client.wait_for ("message" , timeout = 15 , check = check)
            if answer.lower() == a.content.lower():
               await ctx.send(embed = embed2)
            if not answer.lower() == a.content.lower():
               b = await client.wait_for ("message" , timeout = 22 , check = check )
               if answer.lower() == b.content.lower():
                 await ctx.send(embed = embed2)
            
            if not answer.lower() == b.content.lower() or answer.lower() == a.content.lower():
              c = await client.wait_for ("message" , timeout = 30 , check = check )
              if answer.lower() == c.content.lower():
                 await ctx.send(embed = embed2)
           
              else:
                 await ctx.send(embed = embed2)
                 asyncio.sleep(1)
                 await oki.edit(content = "this message is inactive now, try `.owtp`")


cb = ac.Cleverbot("NONK")

#cleberbot 
@client.command(name = "cleverbot" , help = "A ai chatbot that lets you talk with it", aliases= ["cb" , "ask"] , usage = ".ocb <query>")     
async def cleverbot (ctx , *, query):
    await ctx.trigger_typing()
    response = await cb.ask(query , ctx.author.id)
    await ctx.send(f"{ctx.author.mention}{response}")   

             
import async_cse
g_cl = async_cse.Search("ONK") # create the Search client (uses Google by default!)

#GOOOGLE COMMAD 
@client.command()
@commands.cooldown(1,3 , commands.BucketType.user)
async def google (ctx , * , query ):
    if query.startswith("how to make")  : 
        return await ctx.send(f"~~make your own {query[11:] }~~" ) 
    results = await g_cl.search(query, safesearch=False) # returns a list of async_cse.Result objects
    result_list = []
    for i in results[:8]:
        result_list.append(i.url)
    await paginator (ctx , result_list , limit = 1) 





#PINGS 
async def create_db_pool():
    client.pg_con = await asyncpg.create_pool("ONK")

client.loop.run_until_complete(create_db_pool())


    



@client.command(name = "create" , help = "create a ping tracker who tracks your pings" , usage = ".ocreate")
async def create (ctx):
    id1 = str(ctx.author.id) + str(ctx.guild.id)
    
    await client.pg_con.execute("""INSERT INTO pings (id , fpings , fcont , spings , scont , tpings , tcont , epings , econt )
    VALUES ($1 , $2 ,$3 , $4 , $5 , $6 , $7 ,$8 , $9 );""", id1 , "mention yourself" , "1234" , "1234567890" , "1234" , "12345" , "1234" , "1234" , "1234")  
    embed = discord.Embed(title = "Success <a:done:725733143558094979>" , description = "You have been registered ,try running `.opings` after someone tags you ") 
    await ctx.send(embed = embed )



@client.command(name = "pings" , help = "Shows you your last 4 Pings with the a jump url to the message" , usage = ".opings")
@commands.cooldown(1,3 , commands.BucketType.user)
async def pings (ctx):
    id3 = str(ctx.author.id) + str(ctx.guild.id)
    results = await client.pg_con.fetch("""SELECT fpings , fcont , spings , scont , tpings , tcont , epings , econt FROM pings WHERE id = $1;""" , id3 )
    r = results [0]
    cont1  = r["fcont"]
    auth1 = r["fpings"]
    cont2  = r["scont"]
    auth2 = r["spings"]
    auth3 = r["tpings"]
    cont3 = r["tcont"]
    auth4 = r["epings"]
    cont4 = r["econt"]
    format =f"""1){auth1}| [Click Here]({cont1})\n2){auth2} | [Click Here]({cont2})\n3){auth3}|[Click Here]({cont3})\n4){auth4}|[Click Here]({cont4})"""
    embed = discord.Embed(title = "Pings:-" ,  description = f"{format}" )
    await ctx.send(embed = embed)

#pings error HANDLER
@create.error
async def on_command_error(ctx ,error):
    error = getattr(error , "original" , error)
    if isinstance (error , asyncpg.exceptions.UniqueViolationError ):
       embed = discord.Embed( title = "Error <:error:725658157573079101>" , description = " You are already registered. Try running `.opings` to see your pings.")
       await ctx.send(embed=embed)
    else:
        raise error

@pings.error

async def on_command_error(ctx ,error):
    Oerror = getattr(error , "original" , error)
    if isinstance (error , commands.CommandInvokeError ):
       embed = discord.Embed( title = "Error <:error:725658157573079101>" , description = " You are not registered.Type `.ocreate` to create your account")
       await ctx.send(embed=embed)
    elif isinstance (error , commands.CommandOnCooldown ):
         embed = discord.Embed( title = "Cooldown " , description = " You are using commands too fast , retry after {:.2f}s".format(error.retry_after))
         await ctx.send(embed=embed)
    else:
         raise error


#KICK AND ERROR HANDLER 

@client.command(name = "kick" , help = "kicks the mention user from the guild with a optional reason " , usage = ".okick <member/id> [reason]")
@commands.has_permissions(ban_members=True, kick_members=True)
async def kick (ctx, member :discord.Member , *, reason=None ):
    await member.kick(reason=reason)
    await ctx.send (f"kicked {member}")


@kick.error
async def kick_error(ctx, error):

    if isinstance(error,commands.CommandInvokeError):  
        embed= discord.Embed(title= "Mission Permission " , description = "Missing permission, You do not have permission to kick the mentioned user.")
        embed.color = 0xE9335B
        await ctx.send(embed=embed ,delete_after =9)

    elif isinstance(error,commands.MissingRequiredArgument):  
        embed= discord.Embed(title= "Missing Argument " , description = "Usage :` .okick (user) (reason)`")
        embed.color = 0xE9335B
        await ctx.send(embed=embed , delete_after = 9)

    elif isinstance(error,commands.BadArgument):  
        embed= discord.Embed(title= "Bad Argument " , description = "Invalid User, Please tag a valid user.\nUsage :.okick (user) (reason)`")
        embed.color = 0xE9335B
        await ctx.send(embed=embed , delete_after = 9)

    
    
    elif isinstance(error,commands.MissingPermissions):  
        embed= discord.Embed(title= "Mission Permission " , description = "Missing permission,The bot does not has the role to kick members make sure that the bot has `kick_members` Permission .")
        embed.color = 0xE9335B
        await ctx.send(embed=embed , delete_after=13)

    else:
        raise error






#PURGE AND ERROR HANDLER

@client.command(name = "purge" , help = "Deletes the messages of current channel" , usage = ".opurge <limit> ")
@commands.has_permissions(manage_messages=True)
async def purge (ctx , amount : int):
    await ctx.channel.purge(limit=amount)




@purge.error
async def purge_error(ctx, error):

    if isinstance(error,commands.CommandInvokeError):  
        embed= discord.Embed(title= "Mission Permission " , description = "Missing permission, You do not have permission to use this command.")
        embed.color = 0xE9335B
        await ctx.send(embed=embed ,delete_after =9)

    elif isinstance(error,commands.MissingRequiredArgument):  
        embed= discord.Embed(title= "Missing Argument " , description = "Usage :` .opurge (amount) `")
        embed.color = 0xE9335B
        await ctx.send(embed=embed , delete_after = 9)

    elif isinstance(error,commands.BadArgument):  
        embed= discord.Embed(title= "Bad Argument " , description = "Invalid amount, Please specify a integer .")
        embed.color = 0xE9335B
        await ctx.send(embed=embed , delete_after = 9)

    
    
    elif isinstance(error,commands.MissingPermissions):  
        embed= discord.Embed(title= "Mission Permission " , description = "Missing permission,The bot does not has the role to kick perform the following task .Make sure that the bot has `manage_messages` Permission .")
        embed.color = 0xE9335B
        await ctx.send(embed=embed , delete_after=13)

    else:
        raise error









@client.command(name = "suggestion" , help = "Suggest or request a particular feature in the bot. " ,  usage = ".osuggest <suggestion> ")
async def suggest(ctx, *,sugg):
    id = ctx.author.id
    #author = ctx.author
    channel = client.get_channel(715187567661940746)
    await ctx.send("thanks for suggestion")
    await channel.send(f"`{id}` suggested ```{sugg}```")


@client.event

async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed= discord.Embed(title= "CoolDown" , description = "u are using commands too fast while u wait u can [vote for me](https://top.gg/bot/714733360521674800/vote).")
        embed.color = 0xE9335B
        await ctx.send(embed=embed)   
    
    elif isinstance(error,commands.CommandInvokeError):  
        embed= discord.Embed(title= "Error " , description = "Try running a command `.ocreate` and try it again")
        embed.color = 0xE9335B
        #await ctx.send(embed=embed ,delete_after =9)
    else :
       raise error
    

@client.event

async def on_error(error) :

    if isinstance(error , IndexError ):
       pass 
    elif isinstance (error , TypeError) :
       pass 
    else :
       raise error 

          
        

  
@client.command(name = "audit" , help = "Let's you know the last 5 audit log actions" , usage = ".oaudit ")
async def audit (ctx):
    Em = discord.Embed(title = f"Audit Log Actions for {ctx.guild.name}\u200b")
    Em.color = 0x00ffa2
    async for entry in ctx.guild.audit_logs(limit=10):
	 
         ee = str(entry.action)[15:]
         Em.add_field(name = f"{entry.target}" , value =  f"{entry.user} did __{ee}__ to {entry.target} for reason `{entry.reason}`")
	
    await ctx.send(embed=Em)
  
      
       
 #JUST DONT VOTE    
@client.command(name = "vote" , help = "Gives you the link for DBL , so that you can upvote the bot" , usage = ".ovote")
@commands.cooldown(1, 1.5, commands.BucketType.user)
async def vote(ctx):
   em=discord.Embed(title="thanks for voting buddy", description ="[click here](https://top.gg/bot/714733360521674800/vote)")
   em.color = 0xff69b4
   await ctx.send(embed=em)




@client.event
async def on_message(message):
   
   await client.process_commands(message)
   if message.author.id == 673362753489993749:
       title=message.embeds[0].title
       des = message.embeds[0].description
       role4 = discord.utils.get(message.guild.roles,name="T4")
       role5 = discord.utils.get(message.guild.roles,name="T5")
       role6 = discord.utils.get(message.guild.roles,name="T6")
       if "Tier: 4" in title:
          if role4: 
             return await message.channel.send(f"A wild card appeared! **{title}** {role4.mention}")

       elif "Tier: 5" in title:
          if role5:
            return await message.channel.send(f"A wild card appeared! **{title}** {role5.mention}")

       elif "Tier: 6" in title:
          if role6:
            return await message.channel.send(f"A wild card appeared! **{title}** {role6.mention}")
   else :
   
      if not message.author.id == 721945269033500672:
          if message.mentions:
             
             authorid = str(message.author.display_name)        
             mention = str(message.mentions[0].id )
             id2  = str(mention) + str(message.guild.id)
             content = message.jump_url
             results = await client.pg_con.fetch("""SELECT * FROM pings
             WHERE id = $1;""" , id2 )
             ping1 = results[0]["fpings"]
             cont1 = results[0]["fcont"]
             ping2 = results [0]["spings"]
             cont2 = results [0]["scont"]
             ping3 = results [0]["tpings"]
             cont3 = results [0]["tcont"]
      

      
      
      
      
             await client.pg_con.execute(f"""UPDATE pings SET fpings = $1 , 
             fcont = $2 , spings = $3 , scont = $4 ,tpings = $5 , tcont = $6 , epings = $7 , econt = $8 WHERE id = $9 """, authorid , content ,ping1 , cont1 ,ping2 , cont2, ping3 , cont3 ,id2) 
      





   

@client.command()
async def time(ctx):
  n = datetime.datetime.now()
  await ctx.channel.send(n)
#ADDROLE AND REMOVEROLE WITH ERROR HANDLERS

@client.command(pass_context=True , name = "addrole" , help = "Adds a particular role to the mentioned person" , usage = ".oaddrole <member/id> <role>" , aliases = ["arole","ar"])

@commands.has_permissions(manage_roles=True)
async def addrole(ctx, user: discord.Member, role: discord.Role):
  
    await user.add_roles(role)
    
    await ctx.send(f"hey {ctx.author.name}, {user.name} has been given a role called: {role.name}")



@addrole.error
async def addrole_error(ctx, error):


    if isinstance(error,commands.CommandInvokeError):  
        embed= discord.Embed(title= "Mission Permission " , description = "Missing permission, You do not have permission to perform the following task .")
        embed.color = 0xE9335B
        await ctx.send(embed=embed ,delete_after =9)

    elif isinstance(error,commands.MissingRequiredArgument):  
        embed= discord.Embed(title= "Missing Argument " , description = "Usage :` .oaddrole (user) (role)`")
        embed.color = 0xE9335B
        await ctx.send(embed=embed , delete_after = 9)

    elif isinstance(error,commands.BadArgument):  
        embed= discord.Embed(title= "Bad Argument " , description = "Invalid user , Please tag a valid user\n Usage:`.oaddrole (user) (role)`.")
        embed.color = 0xE9335B
        await ctx.send(embed=embed , delete_after = 9)

    
   
    elif isinstance(error,commands.MissingPermissions):  
        embed= discord.Embed(title= "Mission Permission " , description = "Missing permission,The bot does not has the permission to perform the following task ,  make sure that the bot has `manage_role` Permission .")
        embed.color = 0xE9335B
        await ctx.send(embed=embed , delete_after=13)

    else:
        raise error




@client.command(pass_context=True , name = "remove role" , help = "removes a particular role from the mentioned user", usage = ".oremoverole", aliases = ["rm","rrole"])

@commands.has_permissions(manage_roles=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"hey {ctx.author.name}, {user.name} has been removed  a role called: {role.name}")



@removerole.error
async def addrole_error(ctx, error):

    if isinstance(error,commands.CommandInvokeError):  
        embed= discord.Embed(title= "Mission Permission " , description = "Missing permission, You do not have permission to perform the following task .")
        embed.color = 0xE9335B
        await ctx.send(embed=embed ,delete_after =9)

    
    elif isinstance(error,commands.MissingRequiredArgument):  
        embed= discord.Embed(title= "Missing Argument " , description = "Usage :` .oremoverole (user) (role)`")
        embed.color = 0xE9335B
        await ctx.send(embed=embed , delete_after = 9)

    elif isinstance(error,commands.BadArgument):  
        embed= discord.Embed(title= "Bad Argument " , description = "Invalid user , Please tag a valid user\n Usage:`.oremoverole (user) (role)`.")
        embed.color = 0xE9335B
        await ctx.send(embed=embed , delete_after = 9)

    
    elif isinstance(error,commands.MissingPermissions):  
        embed= discord.Embed(title= "Mission Permission " , description = "Missing permission,The bot does not has the permission to perform the following task ,  make sure that the bot has `manage_role` Permission .")
        embed.color = 0xE9335B
        await ctx.send(embed=embed , delete_after=13)

    else:
        raise error



@client.command(aliases = ["g"])
async def lmgify (ctx , * , arg):
   search_term = arg.replace(" " , "+")
   link = f"""https://lmgtfy.com/?q={search_term}"""
   await ctx.send(link)




@client.command()
async def perms (ctx ):
    
   a = lambda x : "<:online:700252359015530506>" if x else  "<:outage:700251782412238889>"
   list = [f"{a(perm)} ==> {v}".replace("_" , " ") for v, perm  in ctx.author.guild_permissions]
   final =  "\n".join(list)
   await ctx.send(embed = discord.Embed(title = ctx.author.display_name , description = final))




@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def hug (ctx , member:discord.Member = None):
  if not member :
    await ctx.channel.send("mention a user you want to hug")
  r = requests.get("https://some-random-api.ml/animu/hug")
  hug = r.json()
  embed = discord.Embed(title= f"{ctx.author.display_name} hugs {member.display_name}")
  embed.color= 0xE9335B
  embed.set_image(url=hug['link'])
  await ctx.channel.send(embed=embed)



@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def pat (ctx , member:discord.Member = None):
  if not member :
    await ctx.channel.send("mention a user you want to pat")
  r = requests.get("https://some-random-api.ml/animu/pat")
  pat = r.json()
  embed = discord.Embed(title= f"{ctx.author.display_name} pats {member.display_name}")
  embed.color= 0xffb6c1
  embed.set_image(url=pat['link'])
  await ctx.channel.send(embed=embed)


@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def wink (ctx , member:discord.Member = None):
  if not member :
    await ctx.channel.send("mention a user you want to wink")
  r = requests.get("https://some-random-api.ml/animu/wink")
  wink = r.json()
  embed = discord.Embed(title= f"{ctx.author.display_name} winks {member.display_name}")
  embed.color= 0xffb6c1
  embed.set_image(url=wink['link'])
  await ctx.channel.send(embed=embed)
  









@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def cuddle (ctx , member:discord.Member = None):
   if not member :
      await ctx.channel.send("mention a user you want to cuddle")
   async with aiohttp.ClientSession() as session:
       resp = await session.get(f'https://rra.ram.moe/i/r?type=cuddle')
       resp = await resp.json()
       gif = f"https://rra.ram.moe{resp['path']}"
       em=discord.Embed(title = f"{ctx.author.display_name} cuddles {member.display_name}")
       em.color=0xcc00ff
       em.set_image(url=gif)         
       await ctx.send(embed=em)





@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def kiss (ctx , member:discord.Member = None):
   if not member :
      await ctx.channel.send("mention a user you want to kiss")
   async with aiohttp.ClientSession() as session:
       resp = await session.get(f'https://rra.ram.moe/i/r?type=kiss')
       resp = await resp.json()
       gif = f"https://rra.ram.moe{resp['path']}"
       em=discord.Embed(title = f"{ctx.author.display_name} kisses {member.display_name}")
       em.color=0xcc00ff
       em.set_image(url=gif)         
       await ctx.send(embed=em)

       



@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def slap (ctx , member:discord.Member = None):
   if not member :
      await ctx.channel.send("mention a user you want to slap")
   async with aiohttp.ClientSession() as session:
       resp = await session.get(f'https://rra.ram.moe/i/r?type=slap')
       resp = await resp.json()
       gif = f"https://rra.ram.moe{resp['path']}"
       em=discord.Embed(title = f"{ctx.author.display_name} slapes {member.display_name}")
       em.color=0xcc00ff
       em.set_image(url=gif)         
       await ctx.send(embed=em)







@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def tickle (ctx , member:discord.Member = None):
   if not member :
      await ctx.channel.send("mention a user you want to tickle")
   async with aiohttp.ClientSession() as session:
       resp = await session.get(f'https://rra.ram.moe/i/r?type=tickle')
       resp = await resp.json()
       gif = f"https://rra.ram.moe{resp['path']}"
       em=discord.Embed(title = f"{ctx.author.display_name} tickles {member.display_name}")
       em.color=0xcc00ff
       em.set_image(url=gif)         
       await ctx.send(embed=em)






@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def stare (ctx , member:discord.Member = None):
   if not member :
      await ctx.channel.send("mention a user you want to stare")
   async with aiohttp.ClientSession() as session:
       resp = await session.get(f'https://rra.ram.moe/i/r?type=stare')
       resp = await resp.json()
       gif = f"https://rra.ram.moe{resp['path']}"
       em=discord.Embed(title = f"{ctx.author.display_name} stares {member.display_name}")
       em.color=0xcc00ff
       em.set_image(url=gif)         
       await ctx.send(embed=em)














@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def kanna(ctx):
  
  apikey = "onk"
  lmt = 50
  search_term = "kanna"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None 
 



@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def albedo(ctx):
  
  apikey = "onk"
  lmt = 40
  search_term = "albedo"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None



@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def zoro(ctx):
  
  apikey = "onk"
  lmt = 50
  search_term = "zoro anime"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None


   




@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def naruto(ctx):
  
  apikey = "onk"
  lmt = 50
  search_term = "naruto"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None 






@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def yumeko(ctx):
  
  apikey = "onk"
  lmt = 40
  search_term = "yumeko"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None





    
@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def ryuk(ctx):
    giphykey="onk"
    search_term="ryuk"
    try:
        async with aiohttp.ClientSession() as session:
           resp = await session.get(f'https://api.giphy.com/v1/gifs/search?api_key={giphykey}&q={search_term}') 
           resp = await resp.json()
           gif=f"https://media.giphy.com/media/{resp['data'][random.randint(0, len(resp['data']) - 2)]['id']}/giphy.gif "
           em=discord.Embed(color=0xcc00ff)
           em.set_image(url=gif)         
           await ctx.send(embed=em)
    except Exception as e:
        await ctx.send(e)



@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def giyu(ctx):
  
  apikey = "onk"
  lmt = 50
  search_term = "Giyu"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None




@client.command(name="ishigami")
@commands.cooldown(1, 2, commands.BucketType.user)
async def ishigami(ctx):
  
  apikey = "onk"
  lmt = 50
  search_term = "yu ishigami"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None 
 





@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def kaguya(ctx):
  
  apikey = "onk"
  lmt = 50
  search_term = "kaguya shinomiya"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None



@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def chika(ctx):
  
  apikey = "onk"
  lmt = 50
  search_term = "chika fujiwara"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None



@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def garaa(ctx):
  
  apikey = "onk"
  lmt = 50
  search_term = "garaa"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None



@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def eugeo(ctx):
  
  apikey = "onk"
  lmt = 50
  search_term = "eugeo"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None


















@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def miko(ctx):
    giphykey="onk"
    search_term="miko iino"
    try:
        async with aiohttp.ClientSession() as session:
           resp = await session.get(f'https://api.giphy.com/v1/gifs/search?api_key={giphykey}&q={search_term}') 
           resp = await resp.json()
           gif=f"https://media.giphy.com/media/{resp['data'][random.randint(0, len(resp['data']) - 2)]['id']}/giphy.gif "
           em=discord.Embed(color=0xcc00ff)
           em.set_image(url=gif)         
           await ctx.send(embed=em)
    except Exception as e:
        await ctx.send(e)









@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def cry(ctx):
  
  apikey = "onk"
  lmt = 50
  search_term = "anime crying"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None




@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def angry(ctx):
  
  apikey = "onk"
  lmt = 50
  search_term = "angry anime"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None






@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def smile(ctx):
  
  apikey = "onk"
  lmt = 50
  search_term = "smiling anime"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None





@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def smug(ctx):
  
  apikey = "onk"
  lmt = 50
  search_term = "anime smug"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None



@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def happy(ctx):
  
  apikey = "onk"
  lmt = 50
  search_term = "happy anime"

  r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

  if r.status_code == 200:
    top_8gifs = r.json()
    gif=top_8gifs["results"][random.randint(0, lmt) - 1]["media"][0]["gif"]["url"]
    embed=discord.Embed(color=discord.Color.green()).set_image(url=gif)
    await ctx.send(embed=embed)
    
  else:
    top_8gifs = None








@client.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def dogfact (ctx ):
  
  r = requests.get("https://some-random-api.ml/facts/dog")
  dogf = r.json()
  
  
  await ctx.channel.send(dogf["fact"])



@client.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def catfact (ctx ):
  
  r = requests.get("https://some-random-api.ml/facts/cat")
  catf = r.json()
  
  
  await ctx.channel.send(catf["fact"])



@client.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def pandafact (ctx ):
  
  r = requests.get("https://some-random-api.ml/facts/panda")
  pandaf = r.json()
  
  
  await ctx.channel.send(pandaf["fact"])



@client.command()
async def foxfact (ctx ):
  
  r = requests.get("https://some-random-api.ml/facts/fox")
  foxf = r.json()
  
  
  await ctx.channel.send(foxf["fact"])


@client.command()
async def birdfact (ctx ):
  
  r = requests.get("https://some-random-api.ml/facts/bird")
  birdf = r.json()
  
  
  await ctx.channel.send(birdf["fact"])




@client.command()
async def ping(ctx):
    await ctx.channel.send ("pong!! {0}ms ".format(round(client.latency *1000)))
    
    

@client.command(pass_context=True)
@commands.has_permissions(change_nickname=True)
async def chnick(ctx , member : discord.Member , nick):
    await member.edit(nick=nick)
    await ctx.channel.send (f"nickname has been changed for {member}")


@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx ):
    for role in ctx.guild.roles:
        if role.name == "@everyone":
            await ctx.channel.set_permissions(role , send_messages=False)
            
            embed = discord.Embed(title= "LOCKED" , description="``Channel has been successfully locked``")
            embed.color= 0xffb6c1

            await ctx.channel.send(embed=embed)


@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx ):
    for role in ctx.guild.roles:
        if role.name == "@everyone":
            await ctx.channel.set_permissions(role , send_messages=True)
            embed = discord.Embed(title= "UNLOCKED" , description="``Channel has been successfully unlocked``")
            embed.color= 0xffb6c1
            asyncio.sleep(3)

            await ctx.channel.send(embed=embed)


@client.command()
@commands.has_permissions(manage_channels=True)
async def softlock(ctx ):
    for role in ctx.guild.roles:
        if role.name == "@everyone":
            await ctx.channel.set_permissions(role , send_messages=False)
            
            embed = discord.Embed(title= "LOCKED" , description="``Channel has been successfully locked``")
            embed.color= 0xffb6c1

            await ctx.channel.send(embed=embed)
            
            
            await asyncio.sleep(30)
            embed = discord.Embed(title= "UNLOCKED" , description="``Channel has been successfully unlocked``")
            embed.color= 0xffb6c1
            await ctx.channel.set_permissions(role , send_messages=True)
            await ctx.channel.send(embed=embed)














@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    if member.top_role < ctx.author.top_role:
        
        guild = ctx.guild

        for role in guild.roles:
            if role.name == "Muted":
                await member.add_roles(role)
                await ctx.channel.send(f"{member.mention} has been muted ")






@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
    if member.top_role < ctx.author.top_role:
        
        guild = ctx.guild

        for role in guild.roles:
            if role.name == "Muted":
                await member.remove_roles(role)
                await ctx.channel.send(f"{member.mention} has been unmuted ")



@client.command()
async def roullete (ctx , choice = "none"):
    X = random.randint(1 , 36)
    embed = discord.Embed (title=f"{ctx.author}" , description=f"you choosed : {choice} \nits :{X}" )
    embed.color= 0xffb6c1

    await ctx.send(embed=embed)




@client.command()
async def toss (ctx , choicet="none"):
    toss_resp =[ "heads" , "tails"]
    X = random.choice(toss_resp)
    embed = discord.Embed (title=f"{ctx.author}" , description=f"you choosed : {choicet} \nits :{X}" )
    embed.color= 0xffb6c1

    await ctx.send(embed=embed)

@client.command()
async def bhandara (ctx):
    puri = random.randint(1 , 100)
    Member = ctx.author
    embed = discord.Embed (title=f"{Member}" , description=f"you have eaten from a bhandara and earned yourself {puri} Puries ")
    embed.color= 0xffb6c1
    embed.set_footer(text="|Sponsored by Owl", icon_url=f"{Member.avatar_url}")
    await ctx.channel.send(embed=embed)


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


@client.command()


async def e (ctx, *, cmd):
    """Evaluates input.
    Input is interpreted as newline seperated statements.
    If the last statement is an expression, that is the return value.
    Usable globals:
      - `bot`: the bot instance
      - `discord`: the discord module
      - `commands`: the discord.ext.commands module
      - `ctx`: the invokation context
      - `__import__`: the builtin `__import__` function
    Such that `>eval 1 + 1` gives `2` as the result.
    The following invokation will cause the bot to send the text '9'
    to the channel of invokation and return '3' as the result of evaluating
    >eval ```
    a = 1 + 2
    b = a * 2
    await ctx.send(a + b)
    a
    ```
    """

    if not ctx.author.id in (461974777905545236,510096668633464843):
       return await ctx.send("Tere paas power na h, smjha")
 
    fn_name = "_eval_expr"

    cmd = cmd.strip("` ")

    # add a layer of indentation
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

    # wrap in async def body
    body = f"async def {fn_name}():\n{cmd}"

    parsed = ast.parse(body)
    body = parsed.body[0].body

    insert_returns(body)

    env = {
        'bot': ctx.bot,
        'discord': discord,
        'commands': commands,
        'ctx': ctx,
        '__import__': __import__
    }
    try : 
       exec(compile(parsed, filename="<ast>", mode="exec"), env)

       result = (await eval(f"{fn_name}()", env))
       await ctx.send(result)
       await ctx.message.add_reaction("<:chikardy:735520396387942430>")
    except Exception as e :
        await ctx.author.send(e)
        await ctx.message.add_reaction("<:error:725658157573079101>")
    

try:
  client.load_extension("jishaku")
  client.load_extension("help")
except Exception as e:
  print(e)
  print("Error Cogs")

client.run("aaaa")
