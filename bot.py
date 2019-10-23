import discord
from discord.ext import commands
from util.functions import randomDiscordColor # pylint: disable=no-name-in-module


class Bot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, module: str):
        """
        Reloads a cog
        """
        if module == 'bot':
            self.bot.reload_extension('bot')
        else:
            self.bot.reload_extension(f'cogs.{module}')
        await ctx.send("🔄")

    @commands.command()
    async def help(self, ctx: commands.Context, command: str = None):
        """
        Displays help message
        """

        embed = discord.Embed(title='**You wanted help? Help is provided**', color = randomDiscordColor())
        embed.set_footer(text=f'Do {self.bot.command_prefix}help commndName to get help for a specific command')

        if command is None:

            for name, cog in self.bot.cogs.items():
                out = ''
                # cmds = [x for x in  if x.name in publicCommands or (await self.bot.is_owner(ctx.author)) or (isMod(ctx) and 'is_owner' not in str(x.checks))]
                for cmd in cog.get_commands():
                    helpStr = str(cmd.help).split('\n')[0]
                    out += f"**{cmd.name}**:\t{helpStr}\n"

                if out:
                    embed.add_field(name=f'**{name}**', value=out, inline=False)
        else:
            
            cmd = self.bot.get_command(command)
            try:
                canRun = await cmd.can_run(ctx)
            except commands.errors.CommandError:
                canRun = False
            print(canRun)
            if cmd is None:
                await ctx.send(f"Command {command} doesn't exist")
                return
            elif not canRun and not await self.bot.is_owner(ctx.author):
                await ctx.send(f"You can't run {command} command")
                return

            embed.add_field(name = f'{cmd.name}', value = cmd.help, inline=False)

            cmdAliases = cmd.aliases
            if (cmdAliases):
                aliases = ''
                for i in range(0, len(cmdAliases)):
                    aliases += f'{i + 1}. {cmdAliases[i]}\n'

                embed.add_field(name='Aliases:', value=aliases, inline=False)
            
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Bot(bot))