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

async def paginator (ctx , entries , limit=5 ):
    
    pages = []
    my_list = []
    for i in entries :
        my_list.append(i)
    for i in range(0 , (len(my_list)) , int(limit)):
          pages.append(tuple(my_list[i:i+int(limit)]))
    c = pages

    content = ""
    for i in c[0]:
       content += str(i) + "\n"
    k = await ctx.send(f"{content}")
    def check (reaction , user) :
          return user == ctx.author and reaction.message.id == k.id
    reactions = [ "<:backward:740246720142901262>","<:shut:744345896912945214>", "<:forward:740246668229869579>" ]
    prev ,stop ,  next = reactions
    for i in reactions :
         await k.add_reaction(i)
    pages = 0
    while True :
       try : 
            a = await  ctx.bot.wait_for("reaction_add" , timeout = 45 , check = check)
            if str(a[0]) == next:
                   pages += 1 
                   content = ""
                   for i in c[pages]:
                         content += str(i) + "\n"
                   await k.edit(content = f"{content}")
                   continue
            if str(a[0]) == prev :
                  pages -= 1 
                  content = ""
                  for i in c[pages]:
                         content += str(i) + "\n"
                  await k.edit(content = f"{content}")
            if str(a[0]) == stop :
               await k.delete()
               break
       except(asyncio.TimeoutError):
            break
       except (IndexError):
            pass 
