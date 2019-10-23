import discord, re, requests, time
from discord.ext import commands
from os import environ
from util import globals # pylint: disable=no-name-in-module
from util.functions import randomDiscordColor, formatTime, modOnly # pylint: disable=no-name-in-module

FUNCTIONS_URL = environ['FUNCTIONS_URL']

def attachmentsToString(attachments: list):
    out = ''
    index = 1
    for attachment in attachments:
        out += f'[Attachment {index}]({attachment})\n'
    
    return out

class Ticket(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    async def ticket(self, ctx: commands.Context):
        """
        Tickets
        """
        pass

    @ticket.command()
    async def create(self, ctx: commands.Context, *, content: str):
        if ctx.guild != None:
            await ctx.send('You can only run this command in DMs. This is to keep the tickets confidential')
            return

        print(content)

        ticket = {
            'messageId': str(ctx.message.id),
            'madeBy': str(ctx.author.id),
            'content': content,
            'createdAt': int(time.time()),
            'attachments': [],

        }

        embed = discord.Embed(title="A ticket was submitted", color = randomDiscordColor())
        embed.add_field(name = 'Content', value = ticket['content'], inline=False)
        embed.add_field(name = 'Created at', value = formatTime(ticket['createdAt']), inline=False)

        attachments = []
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                attachments.append(attachment.url)

            ticket['attachments'] = attachments
            print(attachments)
            embed.add_field(name = 'Atatchments', value = attachmentsToString(ticket['attachments']), inline=False)

        await self.bot.get_guild(globals.server).get_channel(globals.modmailChannel).send(f'ID: {ctx.message.id}', embed = embed)

        requests.post(f'{FUNCTIONS_URL}/createTicket', json=ticket)
        embed.title = "Ticket submitted"
        await ctx.channel.send(f'ID: {ctx.message.id}', embed = embed)

    @ticket.command()
    @modOnly()
    async def modreply(self, ctx: commands.Context, originalId, *, content: str):
        
        req = requests.get(f'{FUNCTIONS_URL}/getTicket?messageId={originalId}')
        original = req.json()

        ticket = {
            'originalId': str(originalId),
            'messageId': str(ctx.message.id),
            'sentBy': str(ctx.author.id),
            'content': content,
            'createdAt': int(time.time()),
            'attachments': [],
        }

        embed = discord.Embed(title="Your ticket was replied to", color = randomDiscordColor())
        embed.add_field(name = 'Content', value = ticket['content'], inline=False)
        embed.add_field(name = 'Original content', value = original['content'], inline=False)
        embed.add_field(name = 'Replied at', value = formatTime(ticket['createdAt']), inline=True)
        embed.add_field(name = 'Replied by', value = ctx.author.name, inline=True)

        attachments = []
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                attachments.append(attachment.url)

            ticket['attachments'] = attachments
            print(attachments)
            embed.add_field(name = 'Atatchments', value = attachmentsToString(ticket['attachments']), inline=False)


        req = requests.post(f'{FUNCTIONS_URL}/replyToTicket', json=ticket)
        madeBy = ctx.guild.get_member(int(original['madeBy']))
        print(madeBy.name)

        await madeBy.send(f'ID: {ctx.message.id}', embed = embed)
        
        embed.title = "You replied to a ticket"
        await self.bot.get_guild(globals.server).get_channel(globals.modmailChannel).send(f'ID: {ctx.message.id}', embed = embed)

        print(originalId)
        print(original)


    @ticket.command()
    async def reply(self, ctx: commands.Context, originalId, *, content: str):
        if ctx.guild != None:
            await ctx.send('You can only run this command in DMs. This is to keep the tickets confidential')
            return

        guild = self.bot.get_guild(globals.server)

        req = requests.get(f'{FUNCTIONS_URL}/getTicket?messageId={originalId}')
        original = req.json()

        ticket = {
            'originalId': str(originalId),
            'messageId': str(ctx.message.id),
            'sentBy': str(ctx.author.id),
            'content': content,
            'createdAt': int(time.time()),
            'attachments': [],
        }

        embed = discord.Embed(title="You responded to the reply", color = randomDiscordColor())
        embed.add_field(name = 'Content', value = ticket['content'], inline=False)
        embed.add_field(name = 'Previous reply', value = original['content'], inline=False)
        embed.add_field(name = 'Replied at', value = formatTime(ticket['createdAt']), inline=True)

        attachments = []
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                attachments.append(attachment.url)

            ticket['attachments'] = attachments
            print(attachments)
            embed.add_field(name = 'Atatchments', value = attachmentsToString(ticket['attachments']), inline=False)


        req = requests.post(f'{FUNCTIONS_URL}/replyToTicket', json=ticket)
        madeBy = guild.get_member(int(original['madeBy']))
        print(madeBy.name)

        await ctx.send(f'ID: {ctx.message.id}', embed = embed)
        print(originalId)
        print(original)
        embed.title = 'The reply was responded to'
        await guild.get_channel(globals.modmailChannel).send(f'ID: {ctx.message.id}', embed = embed)
    
    @commands.command()
    async def purge(self, ctx, amount):
        msgs = await ctx.channel.history(limit=20).flatten()
        mine = [msg for msg in msgs if msg.author.id == 535750344857354241]
        for i in mine:
            await i.delete()


def setup(bot: commands.Bot):
    bot.add_cog(Ticket(bot))
