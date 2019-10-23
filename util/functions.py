from discord import Color, Member
from discord.ext import commands
from random import randint
from datetime import datetime
from util.globals import mods # pylint: disable=no-name-in-module

def randomDiscordColor() -> Color:
    return Color(value=randint(0, 16777215))

def formatTime(time: int) -> str:
    return datetime.fromtimestamp(time).strftime("%d-%m-%Y, %H:%M:%S")

def modOnly():
    def predicate(ctx):
        if isinstance(ctx, Member):
            author = ctx
        else:
            author = ctx.author

        roleIds = [x.id for x in author.roles]
        for roleId in set(roleIds):
            if roleId in mods:
                return True

        return False
        
    return commands.check(predicate)