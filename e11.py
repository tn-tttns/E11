import discord, sqlite3, os, datetime, re
from discord.ext import commands


# os.chdir(r'E11')
query=["""CREATE TABLE IF NOT EXISTS "secret" (
       "user"    INTEGER NOT NULL, 
       "id"    INTEGER NOT NULL, 
       "status"    TEXT NOT NULL
)""", 
"""CREATE TABLE IF NOT EXISTS "warn" (
       "user"    INTEGER NOT NULL, 
       "id"    INTEGER NOT NULL, 
       "reason"    TEXT NOT NULL
)""", 
"""CREATE TABLE IF NOT EXISTS "id" (
       "ticket"    INTEGER NOT NULL, 
       "warn"    INTEGER NOT NULL
)""", 
"""CREATE TABLE IF NOT EXISTS "manywarn" (
       "user"    INTEGER NOT NULL, 
       "three"    INTEGER NOT NULL, 
       "five"    INTEGER NOT NULL
)""", 
# """INSERT INTO id VALUES (1, 1)""", 
]
conn=sqlite3.connect('database.db')
cur=conn.cursor()
for i in query:
    cur.execute(i)
conn.commit()
conn.close()

async def is_owner(ctx: commands.context.Context):
    return 1151455040851156992 in [i.id for i in ctx.author.roles]


class NoticeRole(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="공지알림", emoji='📢', style=discord.ButtonStyle.primary, custom_id='notice')
    async def on_click(self, interaction: discord.Interaction, button):
        role=1152160081052442704
        user=interaction.user
        if role in [i.id for i in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            embed=discord.Embed(description='공지알림 역할이 삭제되었습니다.', color=discord.Color.red())
        else:
            await user.add_roles(user.guild.get_role(role))
            embed=discord.Embed(description='공지알림 역할이 지급되었습니다.', color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)

class SecretChnBtn2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='채널 활성화', style=discord.ButtonStyle.green, custom_id='open')
    async def open(self, interaction: discord.Interaction, button):
        if interaction.user.id in [958657179064365099, 1148999177804718210, 1077929256232955974]:
            guild=interaction.guild
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute(f"SELECT * FROM secret WHERE id = (?)", (int(interaction.channel.name[5:]), ))
            user=c.fetchall()[0][0]
            c.execute(f"UPDATE secret SET status = ? WHERE id = ?", ('open', int(interaction.channel.name[5:])))
            conn.commit()
            conn.close()
            category=discord.utils.get(guild.categories, name='비밀문의')
            await interaction.channel.set_permissions(guild.get_member(user), send_messages=True, read_messages=True)
            await interaction.channel.edit(category=category)
            await interaction.channel.send(guild.get_member(user).mention)
            embed=discord.Embed(description='본 비밀 문의 채널이 활성화되었습니다.\n메시지를 보낼 수 있습니다.', color=discord.Color.green())
            message=await interaction.channel.send(embed=embed, view=SecretChnBtn())
            await message.pin()
            await interaction.message.delete()
        else:
            embed=discord.Embed(description='관리자만 사용 가능한 명령어입니다.', color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label='채널 삭제', style=discord.ButtonStyle.red, custom_id='delete')
    async def on_click(self, interaction: discord.Interaction, button):
        if interaction.user.id in [958657179064365099, 1148999177804718210, 1077929256232955974]:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute(f"DELETE FROM secret WHERE id = (?)", (int(interaction.channel.name[5:]), ))
            conn.commit()
            conn.close()
            await interaction.channel.delete()
        else:
            embed=discord.Embed(description='관리자만 사용 가능한 명령어입니다.', color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

class SecretChnBtn(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='채널 폐쇄', style=discord.ButtonStyle.red, custom_id='close')
    async def close(self, interaction: discord.Interaction, button):
        if interaction.user.id in [958657179064365099, 1148999177804718210, 1077929256232955974]:
            guild=interaction.guild
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute(f"SELECT * FROM secret WHERE id = (?)", (int(interaction.channel.name[5:]), ))
            user=c.fetchall()[0][0]
            c.execute(f"UPDATE secret SET status = ? WHERE id = ?", ('close', int(interaction.channel.name[5:])))
            conn.commit()
            conn.close()
            category=discord.utils.get(guild.categories, name='비밀문의 - 폐쇄')
            await interaction.channel.set_permissions(guild.get_member(user), read_messages=False)
            await interaction.channel.edit(category=category)
            embed=discord.Embed(description='본 비밀 문의 채널이 폐쇄되었습니다.\n관리자만 메시지를 보낼 수 있습니다.', color=discord.Color.red())
            message=await interaction.channel.send(embed=embed, view=SecretChnBtn2())
            await message.pin()
            await interaction.message.delete()
        else:
            embed=discord.Embed(description='관리자만 사용 가능한 명령어입니다.', color=discord.Color.red())
            await interaction.response.send_message(embed=embed,ephemeral=True)

    @discord.ui.button(label='채널 삭제', style=discord.ButtonStyle.red, custom_id='delete')
    async def delete(self, interaction: discord.Interaction, button):
        if interaction.user.id in [958657179064365099, 1148999177804718210, 1077929256232955974]:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute(f"DELETE FROM secret WHERE id = (?)", (int(interaction.channel.name[5:]), ))
            conn.commit()
            conn.close()
            await interaction.channel.delete()
        else:
            embed=discord.Embed(description='관리자만 사용 가능한 명령어입니다.', color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

class SecretChn(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='비밀 문의 채널 생성', emoji='📮', style=discord.ButtonStyle.green, custom_id='secret')
    async def on_click(self, interaction: discord.Interaction, button):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM secret WHERE user = ? AND status = ?", (interaction.user.id, 'open'))
        check=c.fetchall()
        conn.commit()
        conn.close()
        if len(check)==0:
            guild=interaction.guild
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            category=discord.utils.get(guild.categories, name='비밀문의')
            c.execute(f"SELECT * FROM id")
            num=c.fetchall()[0][0]
            c.execute(f"UPDATE id SET ticket = ? WHERE ticket = ?", (num+1, num))
            c.execute(f"INSERT INTO secret VALUES (?, ?, ?)", (interaction.user.id, num, 'open'))
            conn.commit()
            conn.close()
            secret_chn=await guild.create_text_channel(
                f'비밀문의-{num}', 
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(read_messages=False), 
                    guild.get_role(1151455040851156992): discord.PermissionOverwrite(read_messages=True), 
                    interaction.user: discord.PermissionOverwrite(read_messages=True)
                    }, 
                category=category)
            embed=discord.Embed(description=f'<#{secret_chn.id}> 채널이 생성되었습니다.', color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await secret_chn.send(interaction.user.mention)
            embed=discord.Embed(title=f'{interaction.user.name} 님의 비밀문의 채널', description='관리자는 아래 버튼으로 채널을 폐쇄하거나 삭제할 수 있습니다.', color=discord.Color.blue())
            message=await secret_chn.send(embed=embed, view=SecretChnBtn())
            await message.pin()
        else:
            embed=discord.Embed(description=f'문의 채널 생성은 한 유저당 하나만 가능합니다.', color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


class Bot(commands.Bot):
    def __init__(self):
        intents=discord.Intents.all()
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        self.add_view(NoticeRole())
        self.add_view(SecretChnBtn2())
        self.add_view(SecretChnBtn())
        self.add_view(SecretChn())
        
    async def on_ready(self):
        print(f'E11 Start.')

    async def on_member_join(self, member: discord.Member):
        if member.guild.id==1151169856394248232:
            chn=self.get_channel(1151453202764529696)
            embed=discord.Embed(title='새 멤버가 들어왔습니다!', description=f'{member.mention}님이 서버에 들어오셨습니다! 환영합니다!\n규칙을 잘 읽어주세요!', color=discord.Color.green())
            embed.set_thumbnail(url=member.avatar)
            await chn.send(embed=embed)

    async def on_member_remove(self, member):
        if member.guild.id==1151169856394248232:
            chn=self.get_channel(1151453202764529696)
            embed=discord.Embed(description=f'{member.mention}님이 서버를 나가셨습니다.', color=discord.Color.red())
            await chn.send(embed=embed)
        
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.reply(embed=discord.Embed(description='관리자만 사용 가능한 명령어입니다.', color=discord.Color.red()))

    async def on_guild_join(self, guild: discord.Guild):
        if guild.id!=1151169856394248232:
            await guild.leave()

bot=Bot()


@bot.command(name="notice_role")
@commands.check(is_owner)
async def notice(ctx):
    chn=bot.get_channel(1151452938217205760)
    embed=discord.Embed(title=':loudspeaker: 공지알림 역할', description='아래 버튼을 눌러 공지알림 역할을 받을 수 있습니다.\n버튼을 다시 누를 시 역할이 제거됩니다.', color=discord.Color.blue())
    await ctx.reply('<#1151452938217205760> 에 <@&1152160081052442704> 역할 부여 메시지를 보냈습니다.')
    await chn.send(embed=embed, view=NoticeRole())


@bot.command(name="secret_chn")
@commands.check(is_owner)
async def notice(ctx):
    chn=bot.get_channel(1151451302895820902)
    embed=discord.Embed(title=':mailbox: 비밀 문의 채널 생성', description='아래 버튼을 눌러 비밀 문의 채널을 생성할 수 있습니다.\n이유 없이 채널 생성 시 제재될 수 있습니다.', color=discord.Color.blue())
    await ctx.reply('<#1151451302895820902> 에 비밀 문의 채널 생성 메시지를 보냈습니다.')
    await chn.send(embed=embed, view=SecretChn())


@bot.command(name='clean', aliases=['delete', 'purge', '삭제', '청소'])
@commands.check(is_owner)
async def clean(ctx, message: int=1):
    await ctx.channel.purge(limit=message+1)

@clean.error
async def clean_error(ctx, error):
    if isinstance(error, commands.errors.BadArgument):
        await ctx.reply(embed=discord.Embed(description='삭제할 메시지 수는 자연수여야 합니다.', color=discord.Color.red()))


@bot.command(name='warn', aliases=['경고'])
@commands.check(is_owner)
async def warn(ctx: commands.context.Context, user: discord.Member, reason='Unspecific', amount: int=1):
    if amount<=0:
        ctx.reply(embed=discord.Embed(description='횟수는 자연수여야 합니다.'))
    chn=bot.get_channel(1152158163064340551)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM id")
    num=c.fetchall()[0][1]
    c.execute(f"UPDATE id SET warn = ? WHERE warn = ?", (num+amount, num))
    for i in range(amount):
        c.execute(f"INSERT INTO warn VALUES (?, ?, ?)", (user.id, num+i, reason))
    c.execute(f'SELECT * FROM manywarn WHERE user = ?', (user.id, ))
    if len(c.fetchall())==0:
        c.execute(f"INSERT INTO manywarn VALUES (?, ?, ?)", (user.id, 0, 0,))
    conn.commit()
    conn.close()
    if amount==1:
        embed=discord.Embed(title=f'경고', description=f'처리자: {ctx.author.mention}\n대상: {user.mention}\n횟수: {amount}회\n사유: {reason}\n경고 ID: {num}', color=discord.Color.red())
    else:
        embed=discord.Embed(title=f'경고', description=f'처리자: {ctx.author.mention}\n대상: {user.mention}\n횟수: {amount}회\n사유: {reason}\n경고 ID: {num}~{num+amount-1}', color=discord.Color.red())
    await ctx.reply(embed=embed)
    await chn.send(embed=embed)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM warn WHERE user = ?", (user.id, ))
    warn=len(c.fetchall())
    c.execute(f'SELECT * FROM manywarn WHERE user = ?', (user.id, ))
    manywarn=c.fetchall()[0]
    if warn>=7:
        try:
            dm=await user.create_dm()
            embed=discord.Embed(title=f'{user.name}님은 E10 Support 서버에서 차단되셨습니다.', description=f'처리자: {ctx.guild.get_role(1151473241865596988).mention}\n대상: {user.mention}\n사유: 경고 7회 누적', color=discord.Color.red())
            await dm.send(embed=embed)
        except:
            pass
        await user.ban()
        embed=discord.Embed(title=f'차단', description=f'처리자: {ctx.guild.get_role(1151473241865596988).mention}\n대상: {user.mention}\n사유: 경고 7회 누적', color=discord.Color.red())
        c.execute(f"UPDATE manywarn SET five = ? WHERE user = ?", (1, user.id))
        c.execute(f"UPDATE manywarn SET three = ? WHERE user = ?", (1, user.id))
        await chn.send(embed=embed)
    elif warn>=5 and manywarn[2]==0:
        await user.timeout(datetime.timedelta(days=5))
        embed=discord.Embed(title=f'타임아웃', description=f'처리자: {ctx.guild.get_role(1151473241865596988).mention}\n대상: {user.mention}\n기간: 5d\n사유: 경고 5회 누적', color=discord.Color.red())
        c.execute(f"UPDATE manywarn SET five = ? WHERE user = ?", (1, user.id))
        c.execute(f"UPDATE manywarn SET three = ? WHERE user = ?", (1, user.id))
        await chn.send(embed=embed)
    elif warn>=3 and manywarn[1]==0:
        await user.timeout(datetime.timedelta(days=3))
        embed=discord.Embed(title=f'타임아웃', description=f'처리자: {ctx.guild.get_role(1151473241865596988).mention}\n대상: {user.mention}\n기간: 3d\n사유: 경고 3회 누적', color=discord.Color.red())
        c.execute(f"UPDATE manywarn SET three = ? WHERE user = ?", (1, user.id))
        await chn.send(embed=embed)
    conn.commit()
    conn.close()

@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.reply(embed=discord.Embed(description='`!warn [멤버] (이유) (횟수)` 형식으로 입력해주세요!', color=discord.Color.red()))
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.reply(embed=discord.Embed(description='멤버나 횟수를 정확히 입력해주세요.', color=discord.Color.red()))


@bot.command(name='unwarn', aliases=['경고철회', '경고삭제'])
@commands.check(is_owner)
async def unwarn(ctx: commands.context.Context, id: int, reason='Unspecific'):
    chn=bot.get_channel(1152158163064340551)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM warn WHERE id = ?", (id, ))
    try:
        user=c.fetchall()[0][0]
    except:
        await ctx.reply(embed=discord.Embed(description='경고 ID를 찾을 수 없습니다.', color=discord.Color.red()))
        return
    user=ctx.guild.get_member(user)
    c.execute(f"DELETE FROM warn WHERE id = (?)", (id, ))
    conn.commit()
    conn.close()
    embed=discord.Embed(title=f'경고 철회', description=f'처리자: {ctx.author.mention}\n대상: {user.mention}\n사유: {reason}', color=discord.Color.green())
    await ctx.reply(embed=embed)
    await chn.send(embed=embed)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM warn WHERE user = ?", (user.id, ))
    warn=len(c.fetchall())
    if warn==2:
        if user.timed_out_until:
            await user.timeout(None)
            embed=discord.Embed(title=f'타임아웃 해제', description=f'처리자: {ctx.guild.get_role(1151473241865596988).mention}\n대상: {user.mention}\n사유: 경고 철회', color=discord.Color.green())
            await chn.send(embed=embed)
        c.execute(f"UPDATE manywarn SET three = ? WHERE user = ?", (0, user.id))
        c.execute(f"UPDATE manywarn SET five = ? WHERE user = ?", (0, user.id))
    elif warn==4:
        if user.timed_out_until:
            await user.timeout(None)
            embed=discord.Embed(title=f'타임아웃 해제', description=f'처리자: {ctx.guild.get_role(1151473241865596988).mention}\n대상: {user.mention}\n사유: 경고 철회', color=discord.Color.green())
        c.execute(f"UPDATE manywarn SET five = ? WHERE user = ?", (1, user.id))
        await chn.send(embed=embed)
    elif warn==6:
        try:
            dm=await user.create_dm()
            embed=discord.Embed(title=f'{user.name}님은 E10 Support 서버에서 차단 해제되셨습니다.', description=f'[서버 초대 링크](https://discord.gg/F7ZnCHFxFg)\n처리자: {ctx.guild.get_role(1151473241865596988).mention}\n대상: {user.mention}\n사유: 경고 철회', color=discord.Color.green())
            await dm.send(embed=embed)
        except:
            pass
        await user.unban()
        embed=discord.Embed(title=f'차단 해제', description=f'처리자: {ctx.guild.get_role(1151473241865596988).mention}\n대상: {user.mention}\n사유: 경고 철회', color=discord.Color.green())
        await chn.send(embed=embed)
    conn.commit()
    conn.close()

@unwarn.error
async def unwarn_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.reply(embed=discord.Embed(description='`!unwarn [철회할 경고 ID] (이유)` 형식으로 입력해주세요!', color=discord.Color.red()))
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.reply(embed=discord.Embed(description='경고 ID는 자연수여야 합니다.', color=discord.Color.red()))


@bot.command(name='timeout', aliases=['mute', '타임아웃', '뮤트'])
@commands.check(is_owner)
async def timeout(ctx: commands.context.Context, user: discord.Member, duration, reason='Unspecific'):
    try:
        if re.match(r'([0-9]+d[0-9]+h[0-9]m)|([0-9]+d[0-9]+h)|([0-9]+d[0-9]m)|([0-9]+h[0-9]m)|([0-9]+d)|([0-9]+h)|([0-9]m)', duration).group()!=duration:
            await ctx.reply(embed=discord.Embed(description='기간을 정확히 입력해주세요.', color=discord.Color.red()))
            return
    except:
        await ctx.reply(embed=discord.Embed(description='기간을 정확히 입력해주세요.', color=discord.Color.red()))
        return
    chn=bot.get_channel(1152158163064340551)
    dur_exist={'d': False, 'h': False, 'm': False}
    for i in ['d', 'h', 'm']:
        try:
            duration.index(i)
            dur_exist[i]=True
        except:
            pass
    day, hour, minute=0, 0, 0
    if dur_exist['d']==True:
        day=duration[:duration.index('d')]
    if dur_exist['h']==True:
        if dur_exist['d']==True:
            hour=duration[duration.index('d')+1:duration.index('h')]
        else:
            hour=duration[:duration.index('h')]
    if dur_exist['m']==True:
        if dur_exist['h']==True:
            minute=duration[duration.index('h')+1:duration.index('m')]
        elif dur_exist['d']==True:
            minute=duration[duration.index('d')+1:duration.index('m')]
        else:
            minute=duration[:duration.index('m')]
    await user.timeout(datetime.timedelta(days=int(day), hours=int(hour), minutes=int(minute)))
    embed=discord.Embed(title=f'타임아웃', description=f'처리자: {ctx.author.mention}\n대상: {user.mention}\n기간: {duration}\n사유: {reason}', color=discord.Color.red())
    await ctx.reply(embed=embed)
    await chn.send(embed=embed)

@timeout.error
async def timeout_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.reply(embed=discord.Embed(description='`!timeout [멤버] [기간] (이유)` 형식으로 입력해주세요!', color=discord.Color.red()))
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.reply(embed=discord.Embed(description='멤버를 정확히 입력해주세요.', color=discord.Color.red()))


@bot.command(name='untimeout', aliases=['unmute', '타임아웃해제', '뮤트해제'])
@commands.check(is_owner)
async def untimeout(ctx: commands.context.Context, user: discord.Member, reason='Unspecific'):
    chn=bot.get_channel(1152158163064340551)
    await user.timeout(None)
    embed=discord.Embed(title=f'타임아웃 해제', description=f'처리자: {ctx.author.mention}\n대상: {user.mention}\n사유: {reason}', color=discord.Color.green())
    await ctx.reply(embed=embed)
    await chn.send(embed=embed)

@untimeout.error
async def untimeout_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.reply(embed=discord.Embed(description='`!untimeout [멤버] (이유)` 형식으로 입력해주세요!', color=discord.Color.red()))
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.reply(embed=discord.Embed(description='멤버를 정확히 입력해주세요.', color=discord.Color.red()))
    

@bot.command(name='ban', aliases=['차단', '밴'])
@commands.check(is_owner)
async def ban(ctx: commands.context.Context, user: discord.Member, reason='Unspecific'):
    try:
        dm=await user.create_dm()
        embed=discord.Embed(title=f'{user.name}님은 E10 Support 서버에서 차단되셨습니다.', description=f'처리자: {ctx.author.mention}\n대상: {user.mention}\n사유: {reason}', color=discord.Color.red())
        await dm.send(embed=embed)
    except:
        pass
    embed=discord.Embed(title=f'차단', description=f'처리자: {ctx.author.mention}\n대상: {user.mention}\n사유: {reason}', color=discord.Color.red())
    chn=bot.get_channel(1152158163064340551)
    await user.ban()
    await ctx.reply(embed=embed)
    await chn.send(embed=embed)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.reply(embed=discord.Embed(description='`!ban [멤버] (이유)` 형식으로 입력해주세요!', color=discord.Color.red()))
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.reply(embed=discord.Embed(description='멤버를 정확히 입력해주세요.', color=discord.Color.red()))
    

@bot.command(name='unban', aliases=['차단해제', '밴해제'])
@commands.check(is_owner)
async def unban(ctx: commands.context.Context, user: discord.User, reason='Unspecific'):
    try:
        dm=await user.create_dm()
        embed=discord.Embed(title=f'{user.name}님은 E10 Support 서버에서 차단 해제되셨습니다.', description=f'[서버 초대 링크](https://discord.gg/F7ZnCHFxFg)\n처리자: {ctx.author.mention}\n대상: {user.mention}\n사유: {reason}', color=discord.Color.red())
        await dm.send(embed=embed)
    except:
        pass
    chn=bot.get_channel(1152158163064340551)
    await ctx.guild.unban(user)
    embed=discord.Embed(title=f'차단 해제', description=f'처리자: {ctx.author.mention}\n대상: {user.mention}\n사유: {reason}', color=discord.Color.green())
    await ctx.reply(embed=embed)
    await chn.send(embed=embed)

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.reply(embed=discord.Embed(description='`!unban [멤버] (이유)` 형식으로 입력해주세요!', color=discord.Color.red()))
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.reply(embed=discord.Embed(description='멤버를 정확히 입력해주세요.', color=discord.Color.red()))


@bot.command(name='warning', aliases=['warnings', 'infraction', 'infractions', '경고확인', '경고목록'])
async def warning(ctx: commands.context.Context, user: discord.Member=None):
    if user:
        if not await is_owner(ctx) and user!=ctx.author:
            await ctx.reply(embed=discord.Embed(description='자신의 경고만 확인할 수 있습니다.', color=discord.Color.red()))
            return
    else:
        user=ctx.author
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM warn WHERE user = ?", (user.id, ))
    warn=c.fetchall()
    conn.close()
    if len(warn)==0:
        embed=discord.Embed(title=f'{user.name}님의 경고 목록', description=f'아직 받은 경고가 없습니다.', color=discord.Color.green())
    else:
        field=[]
        for i in warn:
            field.append(f'ID: {i[1]}\n사유: {i[2]}')
        embed=discord.Embed(title=f'{user.name}님의 경고 목록', description=f'총 {len(warn)}개의 경고가 있습니다.', color=discord.Color.red())
        for i in field:
            embed.add_field(name='', value=i, inline=False)
    await ctx.reply(embed=embed)

@warning.error
async def warning_error(ctx, error):
    if isinstance(error, commands.errors.BadArgument):
        await ctx.reply(embed=discord.Embed(description='멤버를 정확히 입력해주세요.', color=discord.Color.red()))


@bot.command(name='sync')
@commands.check(is_owner)
async def sync(ctx):
    synced=await bot.tree.sync()
    print(f'Synced {len(synced)} commands.')
    await ctx.reply(f'Synced {len(synced)} commands.')


bot.run(os.environ.get('TOKEN'))
