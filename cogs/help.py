from nextcord.ext import commands
from nextcord.ext.commands import command as Command
from nextcord.ext.commands import Context

class CustomHelpCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Custom Help Command

    @Command(name='help', help='Displays the help command', description='Displays this message', usage='<command>')
    async def help_cmd(self, ctx: Context, cmd=None, tertiary=None):

        bot_cmds = self.bot.commands
        cmds = self.get_cmds()
        maxlen = self.get_max_len(cmds)
        cmd_dict = self.create_dict(bot_cmds, maxlen)
        cmd_list = '\n'.join('{} {}'.format(*i) for i in sorted(cmd_dict.items()))
        if cmd == None:
            await ctx.send(f'{ctx.author.mention}\n```Here is a list of available commands.\nPlease insure you prefix the command with a "--"\n\nCommands:\n{cmd_list}\n\nFor additional help, you use --help <command>```')
        else:

            requested_cmd = self.bot.get_command(cmd)
            if tertiary:

                if isinstance(requested_cmd, commands.Group):
                    cmd_help = ''
                    for subcmd in requested_cmd.walk_commands():
                        if tertiary in subcmd.name:
                            cmd_help = f'Usage: --{cmd} {subcmd.name} {subcmd.usage}\n\nCommand Details:\n{subcmd.help}'
                    await ctx.send(f"{ctx.author.mention}```{cmd_help}```")
                else:
                    if requested_cmd:
                        await ctx.send(f"{ctx.author.mention}\n```Usage: --{requested_cmd.name} {requested_cmd.usage}\n\nCommand Details:\n\n{requested_cmd.help}```")
                    else:
                        await ctx.send(f"{ctx.author.mention} -> Sorry, I don't recognize that command. Please double check the spelling, or use `--help` for more information.")
            else:
                await ctx.send(f"{ctx.author.mention}\n```Usage: --{requested_cmd.name} {requested_cmd.usage}\n\nCommand Details:\n\n{requested_cmd.help}```")

    # Getting command name

    def get_cmds(self):
        return [command.name for command in self.bot.commands if not command.hidden]

    # Finding command name with longest length

    def get_max_len(self, cmdlist):
        return len(max(cmdlist, key=len))

    # Creating a dictionary concatenating the command and help info

    def create_dict(self, cmds, maxlen):
        return {command.name.ljust(maxlen): command.description for command in cmds if not command.hidden}

def setup(bot):
    bot.add_cog(CustomHelpCommand(bot))