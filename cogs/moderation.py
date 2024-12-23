import discord
from discord import app_commands
from discord.ext import commands
from dotenv import dotenv_values

config = dotenv_values(".env")

MODERATION_ROLE = config["DISCORD_MODERATION_ROLE"]
DIRECTIVE_ROLE = config["DIRECTIVE_ROLE"]
IA_ROLE = config["IA_ROLE"]
MGMT_ROLE = config["MGMT_ROLE"]
LOGGING_CHANNEL_ID = config["LOGGING_CHANNEL_ID"]

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")

    @app_commands.command(name="role", description="Adds a role to a user.")
    @app_commands.checks.has_any_role(DIRECTIVE_ROLE, MGMT_ROLE, IA_ROLE)
    async def role(self, interaction : discord.Interaction, member : discord.Member, role : discord.Role):
        if interaction.user.top_role.position > role.position:
            await member.add_roles(role)
            await interaction.response.send_message(f"Successfuly roled user {member.mention}")
        else:
            await interaction.response.send_message(f"Cannot add role to user {member.mention}.")

    @app_commands.command(name="purge", description="Purges above messages.")
    @app_commands.checks.has_any_role(MODERATION_ROLE, DIRECTIVE_ROLE)
    async def purge(self, interaction : discord.Interaction, count : int):
        await interaction.channel.purge(limit=count)
        conf_embed = discord.Embed(title = "Message Purged", color=discord.Color.blue())
        conf_embed.add_field(name="Moderator: ",value=interaction.user.mention, inline=False)
        conf_embed.add_field(name="Messages: ", value=count, inline=False)
        conf_embed.add_field(name="Channel: ", value=interaction.channel)
        conf_embed.set_footer(text="Powered by NYCRP", icon_url="https://cdn.discordapp.com/attachments/1305269939162320946/1308544269128044614/NYCRP_SERVER_LOGO.png?ex=673e5451&is=673d02d1&hm=b2b82704abc59ce686f730da31cee671b61d68d9386f8412fd38d26f5e9be2f9&")
        
        channel = self.client.get_channel(int(LOGGING_CHANNEL_ID))
        
        await channel.send(embed=conf_embed)

        await interaction.response.send_message(f"Purged {count} message(s).", ephemeral=True)

    @app_commands.command(name="kick", description="Kicks the given user")
    @app_commands.checks.has_any_role(MODERATION_ROLE, DIRECTIVE_ROLE)
    async def kick(self, interaction : discord.Interaction, member: discord.Member, *, reason : str):
        if interaction.user.top_role.position > member.top_role.position:
            await interaction.guild.kick(user=member, reason=reason)

            conf_embed = discord.Embed(title = "Member Kicked", color=discord.Color.blue())
            conf_embed.add_field(name="Moderator: ",value=interaction.user.mention, inline=False)
            conf_embed.add_field(name="Kicked: ", value=member.mention, inline=False)
            conf_embed.add_field(name="Reason: ", value=reason, inline=False)
            conf_embed.set_footer(text="Powered by NYCRP", icon_url="https://cdn.discordapp.com/attachments/1305269939162320946/1308544269128044614/NYCRP_SERVER_LOGO.png?ex=673e5451&is=673d02d1&hm=b2b82704abc59ce686f730da31cee671b61d68d9386f8412fd38d26f5e9be2f9&")

            channel = self.client.get_channel(LOGGING_CHANNEL_ID)
            await channel.send(embed=conf_embed)

            await interaction.response.send_message(f"Kicked user: {member.mention}.")
        else:
            await interaction.response.send_message(f"Cannot kick user {member.mention}.")

    @app_commands.command(name="ban", description="Bans the given user")
    @app_commands.checks.has_role(MODERATION_ROLE)
    async def ban(self, interaction : discord.Interaction, member: discord.Member, *, reason : str):
        if interaction.user.top_role.position > member.top_role.position:
            await interaction.guild.ban(user=member, reason=reason)

            conf_embed = discord.Embed(title = "Member Banned", color=discord.Color.blue())
            conf_embed.add_field(name="Moderator: ",value=interaction.user.mention, inline=False)
            conf_embed.add_field(name="Banned: ", value=member.mention, inline=False)
            conf_embed.add_field(name="Reason: ", value=reason, inline=False)
            conf_embed.set_footer(text="Powered by NYCRP", icon_url="https://cdn.discordapp.com/attachments/1305269939162320946/1308544269128044614/NYCRP_SERVER_LOGO.png?ex=673e5451&is=673d02d1&hm=b2b82704abc59ce686f730da31cee671b61d68d9386f8412fd38d26f5e9be2f9&")

            channel = self.client.get_channel(LOGGING_CHANNEL_ID)
            await channel.send(embed=conf_embed)

            await interaction.response.send_message(f"Banned user: {member.mention}.")
        else:
            await interaction.response.send_message(f"Cannot ban user {member.mention}.")

async def setup(client):
    await client.add_cog(moderation(client))