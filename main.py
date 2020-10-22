# -*- coding: utf-8 -*-
# Taiyaki huyu
# Code by tasuren

from discord.ext import commands

import discord


from PIL import Image, ImageDraw, ImageFont
from datetime import timedelta
from random import randint

import psutil
import rtutil
import json
import os


mode = 0


print(f'-Now loading...\n|MODE:{mode}')


# データ読み込み
with open("data/data.json",mode="r") as f:
    data = json.load(f)


color = [0xbbe2f1,0x33e5c,0xaaaab0]


# Jishaku
team_id = [7715493081247383552,634763612535390209]
class MyBot(commands.Bot):
    async def is_owner(self, user: discord.User):
        if user.id in team_id:
            return True
        return await super().is_owner(user)


pr = data["data"]["pr"][mode]


# 初期設定
intents = discord.Intents.all()
bot = MyBot(command_prefix=pr,intents=intents)
bot.load_extension("jishaku")
bot.remove_command("help")


# 画像認証の画像を作るやつ
async def make_pic():
        im = Image.open("data/auth/desk.png")
        back = im.copy()
        draw = ImageDraw.Draw(back)
        fnt = ImageFont.truetype('data/auth/generic.otf', 70)
        ran = ""
        for i in range(int(6)-1):
            ran = str(randint(0,int(9))) + ran
        draw.text((230,170), str(ran), fill=(0,0,0), font=fnt)
        back.save(f'data/auth/work/{ran}.png')
        return ran


# 行ゲット
def get_line(content,line):
    return content.splitlines()[line-1]


# エラーメッセージ用
def error(smode,title,desc,footer=None,ccolor=color[1]):
    if smode == "error":
        emoji = "<:error:765533830299123753>"
    elif smode == "none":
        emoji = "<:none:765535237702549514>"
        ccolor = color[2]
    embed = discord.Embed(
        title=f"{emoji}  {title}",
        description=desc,
        color=ccolor
    )
    if footer is not None:
        embed.set_footer(text=footer)
    return embed

"""
# エラー時
@bot.event
async def on_command_error(ctx,errorr):
  try:
    if isinstance(errorr, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(embed=error("none","Unknown","そのコマンドはありません。"))
    elif isinstance(errorr, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(embed=error("none","Unknown","引数がたりません。"))
    else:
        await ctx.send(embed=error("error","内部エラー",f"すみませんが、OryoBot内でエラーが発生しました。\n```{errorr}```"))
  except:
    await ctx.send(embed=error("error","エラー","すみませんが、でエラーが発生しました。"))
"""

# 起動時
@bot.event
async def on_ready():
    activity = discord.Activity(
        name=f"{pr}help | {len(bot.guilds)}server", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    print("|Conected\n|Started bot")


# tasuren
@bot.command()
async def tasuren(ctx):
    await ctx.send("BOT開発者が仕込んだ隠しメッセージ!")


# 招待リンク
@bot.command()
async def invite(ctx):
    await ctx.send(
        embed=discord.Embed(
            title="このBOTの招待リンク",
            description=f'{data["data"]["link"][mode]}'
            )
        )


# HELP コマンド
@bot.command()
async def help(ctx,arg=None):
    print(f"-Help\n|<Author>{ctx.author}")
    if arg is None:
        # ノーマル
        embed = discord.Embed(
            title="Taiyaki huyu HELP",
            description=f"**`{pr}help 見たい機能の名前`**  で機能の詳細を見ることができます。",
            color=color[0])
        with open("help/1.txt","r",encoding="utf-8_sig") as f:
            cont = f.read()
        name = get_line(cont,1)
        value = cont.replace(get_line(cont,1),"",1)
        embed.add_field(
            name=name,
            value=value)
        await ctx.send(embed=embed)
    else:
        # 機能詳細
        if (os.path.exists(f"help/{arg}.txt")):
            with open(f"help/{arg}.txt",encoding="utf-8_sig") as f:
                cont = f.read()
            name = get_line(cont,1)
            value = cont.replace(get_line(cont,1),"",1)
            embed = discord.Embed(
                title=name,
                description=value,
                color=color[0])
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=error("none","Unknown",f"`{arg}`の名前の詳細が見つかりませんでした。"))


# 画像認証設定コマンド
@bot.command()
async def pauth(ctx,name,wm="None"):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(embed=error("none","権限エラー","このコマンドはサーバーの管理者のみ有効です。"))
        return
    if name != "off":
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role:
            data["pauth"][str(ctx.guild.id)] = {
                "channel": ctx.channel.id,
                "queue": {},
                "roleid": role.id,
                "wm": wm
                }
            with open("data/data.json","w") as f:
                json.dump(data,f,indent=4)
            await ctx.send("画像認証を設定しました。\nこのチャンネルで行われます。")
        else:
            await ctx.send(embed=error("none","Unknown",f"`{name}`の名前の役職が見つかりませんでした。"))
    else:
        if data["pauth"].get(str(ctx.guild.id)) is not None:
            del data["pauth"][str(ctx.guild.id)]
            with open("data/data.json","w") as f:
                json.dump(data,f,indent=4)
            await ctx.send(f"{ctx.author.mention}, 画像認証設定をオフにしました。")
        else:
            await ctx.send(f"{ctx.author.mention}, 既にオフでした。")


# デバッグ用
@bot.group()
async def debug(ctx):
    if not ctx.author.id in team_id:
        await ctx.send(embed=error("none","権限エラー","このコマンドはTaiyaki huyuの開発者のみ有効です。"))
        return
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(
            title="OryoBot",
            description="Running on Glitch (Linux)",
            color=color[0]
        )
        if mode == 1:
            mode_s = "Not Canary"
        elif mode == 0:
            mode_s = "Canary"
        else:
            mode_s = "Unknown"
        embed.add_field(name="MODE",value=mode_s)
        embed.add_field(name="Memory",value=f"{psutil.virtual_memory().percent}%")
        embed.add_field(name="CPU",value=f"{psutil.cpu_percent(interval=1)}%")
        embed.add_field(name="Disk",value=f"{psutil.disk_usage('/').percent}%")
        await ctx.send(embed=embed)


# 再起動用コマンド
@debug.command()
async def reboot(ctx):
    if not ctx.author.id in team_id:
        await ctx.send(embed=error("none","権限エラー","このコマンドはTaiyaki huyuの開発者のみ有効です。"))
        return
    activity = discord.Activity(
        name="再起動中。。。", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    await ctx.send("再起動します。")
    await bot.logout()



# メンバーが入った時
@bot.event
async def on_member_join(member):

    ### 画像認証 ###
    pauth = data["pauth"].get(str(member.guild.id))
    # ON か確認
    if pauth is not None:
        # 画像認証をする場所をゲット
        channel = bot.get_channel(pauth["channel"])

        async with channel.typing():
            # 認証画像作成
            name = await make_pic()

            # 認証リストに追加
            data["pauth"][str(member.guild.id)]["queue"][str(member.id)] = name

            # ウェルカムメッセージ Noneだったらなしにする
            wm = data["pauth"][str(member.guild.id)]["wm"]
            if wm == "None":
                wm = ""

            # セーブ
            with open("data/data.json","w") as f:
                json.dump(data,f,indent=4)
        # 送信
        await channel.send(content=f"{member.mention}\n画像認証をしてください。\n{wm}",file=discord.File(f"data/auth/work/{name}.png"))



# メッセージが来たとき
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    # BOTはreturn
    if message.author.bot:
        return
    

    ### 画像認証 - 認証 ###
    if data["pauth"].get(str(message.guild.id)) is not None:
        if message.channel.id == data["pauth"][str(message.guild.id)]["channel"]:
            if data["pauth"][str(message.guild.id)]["queue"].get(str(message.author.id)) is not None:
                if len(message.content) == 5:
                    # 認証用コード
                    if data["pauth"][str(message.guild.id)]["queue"][str(message.author.id)] == message.content:
                        # 役職をゲット
                        role = discord.utils.get(message.guild.roles, id=data["pauth"][str(message.guild.id)]["roleid"])
                        # なかったらエラー
                        if role is None:
                            error_mes = "認証には成功しましたが役職をつけれませんでした。\nサーバーの管理者に役職の存在確認をしてもらってください。"
                            await message.channel.send(error_mes)
                        else:
                            # 役職あったら
                            async with message.channel.typing():
                                try:        # 役職をつける
                                    await message.author.add_roles(role)
                                except:     # つけれなかったら
                                    await message.channel.send("認証には成功しましたが役職をつけれませんでした。\nTaiyaki huyuに権限があるか、役職の位置がTaiyaki huyuより下にあるか確認してください。")
                                else:       # つけれたら
                                    # セーブ
                                    del data["pauth"][str(message.guild.id)]["queue"][str(message.author.id)]
                                    with open("data/data.json","w") as f:
                                        json.dump(data,f,indent=4)
                                    
                                    # 認証画像削除
                                    os.remove(f"data/auth/work/{message.content}.png")
                                
                            # 成功メッセージ
                            await message.channel.send(f"{message.author.mention}, 認証に成功しました。")   
                    else:
                        await message.channel.send(f"{message.author.mention}, コードが違います。")




print("|Conecting...")


bot.run(data["data"]["TOKEN"])
