import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from nextcord import Member
from nextcord.ext.commands import has_permissions, MissingPermissions
from googlesearch import search
from datetime import datetime
import asyncio
import pytz
import requests

intents = nextcord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

client = commands.Bot(command_prefix='?', intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.idle, activity=nextcord.Game("Gooning Simulator"))
    print("The goon is gooning.")
    print("--------------------")

testServerId = 1265959030283698207

@client.slash_command(name="test", description="Testing rn", guild_ids=[testServerId])
async def test(interaction: Interaction):
    await interaction.response.send_message("gooning rn")

@client.event
async def on_member_join(member):
    message = "Welcome to the server!"
    embed = nextcord.Embed(title=message)
    await member.send(embed=embed)

@client.slash_command(name="kick", description="Kick a member", guild_ids=[testServerId])
@has_permissions(kick_members=True)
async def kick(
    interaction: Interaction,
    member: Member = SlashOption(name="member", description="The member to kick", required=True),
    reason: str = SlashOption(name="reason", description="The reason for kicking the member", required=False)
):
    if interaction.guild.me.guild_permissions.kick_members:
        reason = reason if reason else "No reason provided"
        await member.kick(reason=reason)
        await interaction.response.send_message(f'User {member} has been kicked for reason: {reason}')
    else:
        await interaction.response.send_message("I do not have permission to kick members.")

@kick.error
async def kick_error(interaction: Interaction, error):
    if isinstance(error, MissingPermissions):
        await interaction.response.send_message("You do not have permission to kick members.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await interaction.response.send_message("Please mention a user to kick.")
    elif isinstance(error, commands.BadArgument):
        await interaction.response.send_message("Please provide a valid user to kick.")
    else:
        await interaction.response.send_message(f"An error occurred: {error}")

@client.slash_command(name="ban", description="Ban a member", guild_ids=[testServerId])
@has_permissions(ban_members=True)
async def ban(
    interaction: Interaction,
    member: Member = SlashOption(name="member", description="The member to ban", required=True),
    reason: str = SlashOption(name="reason", description="The reason for banning the member", required=False)
):
    if interaction.guild.me.guild_permissions.ban_members:
        reason = reason if reason else "No reason provided"
        await member.ban(reason=reason)
        await interaction.response.send_message(f'User {member} has been banned for reason: {reason}')
    else:
        await interaction.response.send_message("I do not have permission to ban members.")

@ban.error
async def ban_error(interaction: Interaction, error):
    if isinstance(error, MissingPermissions):
        await interaction.response.send_message("You do not have permission to ban members.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await interaction.response.send_message("Please mention a user to ban.")
    elif isinstance(error, commands.BadArgument):
        await interaction.response.send_message("Please provide a valid user to ban.")
    else:
        await interaction.response.send_message(f"An error occurred: {error}")

@client.slash_command(name="unban", description="Unban a member", guild_ids=[testServerId])
@has_permissions(ban_members=True)
async def unban(
    interaction: Interaction,
    user_id: int = SlashOption(name="user_id", description="The ID of the user to unban", required=True),
    reason: str = SlashOption(name="reason", description="The reason for unbanning the user", required=False)
):
    if interaction.guild.me.guild_permissions.ban_members:
        reason = reason if reason else "No reason provided"
        user = await client.fetch_user(user_id)
        await interaction.guild.unban(user, reason=reason)
        await interaction.response.send_message(f'User {user} has been unbanned for reason: {reason}')
    else:
        await interaction.response.send_message("I do not have permission to unban members.")

@unban.error
async def unban_error(interaction: Interaction, error):
    if isinstance(error, MissingPermissions):
        await interaction.response.send_message("You do not have permission to unban members.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await interaction.response.send_message("Please provide the user ID to unban.")
    elif isinstance(error, commands.BadArgument):
        await interaction.response.send_message("Please provide a valid user ID to unban.")
    else:
        await interaction.response.send_message(f"An error occurred: {error}")

@client.slash_command(name="mute", description="Mute a member", guild_ids=[testServerId])
@has_permissions(manage_roles=True)
async def mute(
    interaction: Interaction,
    member: Member = SlashOption(name="member", description="The member to mute", required=True),
    reason: str = SlashOption(name="reason", description="The reason for muting the member", required=False)
):
    if interaction.guild.me.guild_permissions.manage_roles:
        reason = reason if reason else "No reason provided"
        mute_role = nextcord.utils.get(interaction.guild.roles, name="Muted")

        if not mute_role:
            
            if not interaction.guild.me.guild_permissions.manage_roles:
                await interaction.response.send_message("I do not have permission to create roles.")
                return
            
            mute_role = await interaction.guild.create_role(name="Muted")

            
            for channel in interaction.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

       
        if not interaction.guild.me.guild_permissions.manage_roles:
            await interaction.response.send_message("I do not have permission to manage roles.")
            return
        
        await member.add_roles(mute_role, reason=reason)
        await interaction.response.send_message(f'User {member} has been muted for reason: {reason}')
    else:
        await interaction.response.send_message("I do not have permission to manage roles.")

@client.slash_command(name="unmute", description="Unmute a member", guild_ids=[testServerId])
@has_permissions(manage_roles=True)
async def unmute(
    interaction: Interaction,
    member: Member = SlashOption(name="member", description="The member to unmute", required=True)
):
    if interaction.guild.me.guild_permissions.manage_roles:
        mute_role = nextcord.utils.get(interaction.guild.roles, name="Muted")

        if mute_role in member.roles:
            if not interaction.guild.me.guild_permissions.manage_roles:
                await interaction.response.send_message("I do not have permission to manage roles.")
                return
            
            await member.remove_roles(mute_role)
            await interaction.response.send_message(f'User {member} has been unmuted.')
        else:
            await interaction.response.send_message(f'User {member} is not muted.')
    else:
        await interaction.response.send_message("I do not have permission to manage roles.")


@client.command(name="google")
async def google_command(ctx, *, query: str):
    search_results = list(search(query, num_results=1))
    if search_results:
        result = search_results[0]
        await ctx.send(f'First result for "{query}": {result}')
    else:
        await ctx.send(f'No results found for "{query}".')

@client.slash_command(name="timeout", description="Mute a member for a specified duration", guild_ids=[testServerId])
@has_permissions(manage_roles=True)
async def timeout(
    interaction: Interaction,
    member: Member = SlashOption(name="member", description="The member to mute", required=True),
    duration: int = SlashOption(name="duration", description="Duration in minutes", required=True),
    reason: str = SlashOption(name="reason", description="The reason for muting the member", required=False)
):
    if interaction.guild.me.guild_permissions.manage_roles:
        reason = reason if reason else "No reason provided"
        mute_role = nextcord.utils.get(interaction.guild.roles, name="Muted")

        if not mute_role:
            mute_role = await interaction.guild.create_role(name="Muted")

            for channel in interaction.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        await member.add_roles(mute_role, reason=reason)
        await interaction.response.send_message(f'User {member} has been muted for {duration} minutes for reason: {reason}')
        
        await asyncio.sleep(duration * 60)
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await interaction.channel.send(f'User {member} has been unmuted after {duration} minutes.')

    else:
        await interaction.response.send_message("I do not have permission to manage roles.")

@client.slash_command(name="untimeout", description="Unmute a member", guild_ids=[testServerId])
@has_permissions(manage_roles=True)
async def untimeout(
    interaction: Interaction,
    member: Member = SlashOption(name="member", description="The member to unmute", required=True)
):
    if interaction.guild.me.guild_permissions.manage_roles:
        mute_role = nextcord.utils.get(interaction.guild.roles, name="Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await interaction.response.send_message(f'User {member} has been unmuted.')
        else:
            await interaction.response.send_message(f'User {member} is not muted.')

    else:
        await interaction.response.send_message("I do not have permission to manage roles.")






@client.slash_command(name="purge", description="Purge messages from the channel", guild_ids=[testServerId])
@commands.has_permissions(manage_messages=True)
async def purge(
    interaction: Interaction,
    amount: int = SlashOption(name="amount", description="Number of messages to delete", required=False),
    user: nextcord.Member = SlashOption(name="user", description="User whose messages to delete", required=False),
    start_time: str = SlashOption(name="start_time", description="Start time in YYYY-MM-DD HH:MM:SS format", required=False),
    end_time: str = SlashOption(name="end_time", description="End time in YYYY-MM-DD HH:MM:SS format", required=False)
):
    if amount is None and not (start_time and end_time):
        await interaction.response.send_message("Please provide either an amount or a time range.", ephemeral=True)
        return

    if start_time:
        try:
            start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            await interaction.response.send_message("Start time is in an invalid format. Use YYYY-MM-DD HH:MM:SS.", ephemeral=True)
            return
    else:
        start_dt = None

    if end_time:
        try:
            end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            await interaction.response.send_message("End time is in an invalid format. Use YYYY-MM-DD HH:MM:SS.", ephemeral=True)
            return
    else:
        end_dt = None

    if start_dt:
        start_dt = pytz.utc.localize(start_dt)
    if end_dt:
        end_dt = pytz.utc.localize(end_dt)

    channel = interaction.channel
    messages = await channel.history(limit=100).flatten()

    if amount:
        messages = messages[:amount]

    
    filtered_messages = []
    for msg in messages:
        if start_dt and end_dt:
            if start_dt <= msg.created_at <= end_dt:
                filtered_messages.append(msg)
        elif start_dt:
            if start_dt <= msg.created_at:
                filtered_messages.append(msg)
        elif end_dt:
            if msg.created_at <= end_dt:
                filtered_messages.append(msg)
        else:
            filtered_messages.append(msg)

    if user:
        filtered_messages = [msg for msg in filtered_messages if msg.author == user]

    for msg in filtered_messages:
        await msg.delete()

    try:
        await interaction.response.send_message(f"Deleted {len(filtered_messages)} messages.", ephemeral=True)
    except nextcord.errors.NotFound:
        print("Failed to send message: interaction not found.")




@client.command(name='define')
async def define(ctx, *, word: str):
    """Fetches definition from Urban Dictionary"""
    url = f"https://api.urbandictionary.com/v0/define?term={word}"
    response = requests.get(url)
    data = response.json()

    if data['list']:
        definition = data['list'][0]['definition']
        await ctx.send(f"**{word}**: {definition}")
    else:
        await ctx.send(f"No definitions found for **{word}**.")



client.run('yourtoken')
    
