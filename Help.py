import discord
from discord.ext import commands

class MyHelpCommand(commands.HelpCommand):
	# This function triggers when somone type `<prefix>help`
        async def send_bot_help(self, mapping):
                ctx = self.context
                Member = ctx.author
                file = discord.File("text.gif", filename= "text.gif")
                embed = discord.Embed(title="<a:__verified4:719472520486453280> Some usefull commands", description = "To use the feature type `.o{command}` <a:Thumbsup:719935159427924019> " )
                embed.color= 0xE9335B
                embed.add_field(name= "moderation <:moderator:719621742993342550> ", value= "> `kick,ban,purge,lock,softlock,unlock,purge,chnick,addrole,removerole,mute,unmute`")
                embed.add_field(name="fun <a:fun:719621895569539095> " , value="> `roullete,toss,dogfact,catfact,pandafact,foxfact,birdfact,wtp(which pokemon is that),gtb(guess the brand)`")
                embed.add_field(name="Anime <a:anime:719623172982439968> ", value = "> `kanna,naruto,ryuk,giyu,ishigami,kaguya,chika,eugeo,garaa,yumeko,albedo,zoro`")
                embed.add_field(name="Actions <a:action:719624959537840239> " , value="> `cry,angry,happy,smile,smug,hug,pat,wink,cuddle,kiss,slap,tickle,stare`")
                embed.add_field(name="Support <a:support:719625052634480670> " , value = """> [invite me!!](https://top.gg/bot/714733360521674800)\n> use command `.osuggest (suggestion)` for suggestions
                [Support server](https://discord.gg/UuQeNec)""")
                embed.add_field (name = "pings" , value = "•To get started register yourself by typing `.ocreate`, now you have been registered into the Database.\n•You can use the command `.opings` to see your recent mentions.\n(by default they are set to <@invalid-user> and 1234, you need to get yourself mentioned and it will update it) ")
  
                embed.set_thumbnail(url="attachment://text.gif")
                embed.set_footer(text=f"{ctx.author}", icon_url=f"{Member.avatar_url}")
                embed.set_footer(text=f"{ctx.author}", icon_url=f"{Member.avatar_url}")
                await ctx.send (file=file , embed=embed)
    

	
	# This function triggers when someone type `<prefix>help <cog>`
        async def send_cog_help(self, cog):
                ctx = self.context
		
		# Do what you want to do here
	
	# This function triggers when someone type `<prefix>help <command>`
        async def send_command_help(self, command):
                ctx = self.context
                embed = discord.Embed (title = f"{command.name}" , description = f"{command.help}")
                embed.color = 0xfff000
                embed.add_field(name = "usage" , value = f"```{command.usage}```" )
                embed.add_field(name = "Aliases" , value = f"```{command.aliases}```")
                await ctx.send(embed=embed)
		
	
	# This function triggers when someone type `<prefix>help <group>`
        async def send_group_help(self, group):
                ctx = self.context
		
		# Do what you want to do here
		
class Help(commands.Cog):
         def __init__(self, client):
                self.client = client
		
		# Storing main help command in a variable
                self.client._original_help_command = client.help_command
		
		# Assiginig new help command to bot help command
                client.help_command = MyHelpCommand()
		
		# Setting this cog as help command cog
                client.help_command.cog = self
	
	# Event triggers when this cog unloads
         def cog_unload(self):
		
		# Setting help command to the previous help command so if this cog unloads the help command restores to previous
                self.client.help_command = self.client._original_help_command

def setup(client):
        client.add_cog(Help(client))
