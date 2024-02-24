import settings
import discord
from db import db
from discord import app_commands
from discord.ext import commands
import requests
from mylibs import get_color

logger = settings.logging.getLogger("bot")

def run():
    bot = commands.Bot(
        command_prefix="!",
        intents=discord.Intents.all()
    )
    
    @bot.event
    async def on_ready() -> None:
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
    
    
    @bot.event
    async def setup_hook() -> None:
        await bot.tree.sync()
    
    
    @bot.tree.command()
    @app_commands.describe(atcoder_id="あなたの AtCoder ID を入力")
    async def register(interaction: discord.Interaction, atcoder_id: str) -> None:
        """registerコマンド
        
        registerコマンドを打ったユーザーのAtCoder IDとレートを登録する.
        
        Args:
            interaction (discord.Interaction): コマンドの Interntion.
            atcoder_id (str): 登録する AtCoder ID.
        """
        
        try:
            async with await db.create_server_connection() as conn:
                # MySQL からコマンド入力者の AtCoder ID を拾ってくる.
                # 未登録ならば None が返ってくる.
                existing_atcoder_id, _ = await db.fetch_user(conn, interaction.user.id)
                
                if existing_atcoder_id is None:
                    # 未登録ならば、MySQLにコマンド入力者のユーザ情報を保存する.
                    res = requests.get(
                        url=f"http://kyopro-ratings.jp1.su8.run/json?atcoder={atcoder_id}"
                    )
                    
                    logger.info(res.text)
                    
                    data = res.json()
                    
                    if data['atcoder']['status'] == 'success':
                        rating = data['atcoder']['rating']
                        
                        await db.set_user(conn, atcoder_id, interaction.user.id, rating)
                        
                        await interaction.response.send_message(
                            f"{interaction.user.mention} AtCoder IDを登録しました! ({atcoder_id})"
                        )
                    
                    else:
                        await interaction.response.send_message(
                            f"{interaction.user.mention} 当該Atcoderユーザーは存在しませんでした. ({atcoder_id})",
                            ephemeral=True
                        )
                    
                else:
                    # 登録済ならば、既に登録していることをユーザに伝える.
                    await interaction.response.send_message(
                        f"{interaction.user.mention} 既に登録しています. ({existing_atcoder_id})",
                        ephemeral=True
                    )

        except db.aiomysql.Error as err:
            # MySQL との通信時にエラーが発生した場合の処理.
            await interaction.response.send_message(
                f"{interaction.user.mention} 登録に失敗しました….",
                ephemeral=True
            )
            
            logger.error(err)
    
    
    @bot.tree.command()
    async def show_me(interaction: discord.Interaction) -> None:
        try:
            async with await db.create_server_connection() as conn:
                atcoder_id, rating = await db.fetch_user(conn, interaction.user.id)
                
                if atcoder_id is None:
                    await interaction.response.send_message(
                        f"{interaction.user.mention} まだ登録していません！",
                        ephemeral=True
                    )
                else:
                    embed = discord.Embed(
                        title=f"{interaction.user.display_name}",
                        description=f"https://atcoder.jp/users/{atcoder_id}",
                        color=get_color(rating),
                    )
                    embed.set_author(
                        name=interaction.user.name,
                        icon_url=interaction.user.display_avatar.url
                    )
                    embed.add_field(name="AtCoder ID",value=atcoder_id)
                    embed.add_field(name="Rating", value=rating)
                    await interaction.response.send_message(
                        embed=embed
                    )
                    
        except db.aiomysql.Error as err:
            # MySQL との通信時にエラーが発生した場合の処理.
            await interaction.response.send_message(
                f"{interaction.user.mention} 参照に失敗しました.",
                ephemeral=True
            )
            
            logger.error(err)
        
        
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()

