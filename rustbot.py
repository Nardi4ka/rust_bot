import disnake
from disnake.ext import commands, tasks
import a2s

# === КОНФИГУРАЦИЯ ===
BOT_TOKEN = "DISCORD_BOT_TOKEN"
RUST_SERVER = ("185.189.255.113", 35210)  # ТОТ САМЫЙ ПОРТ!

intents = disnake.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@tasks.loop(minutes=3)
async def update_rust_status():
    """Обновление статуса бота каждые 3 минуты"""
    try:
        info = a2s.info(RUST_SERVER, timeout=10.0)
        status_text = f"{info.player_count}/{info.max_players} игроков | {info.map_name}"
        
        await bot.change_presence(
            activity=disnake.Activity(
                type=disnake.ActivityType.watching, 
                name=status_text
            )
        )
        print(f"✅ Статус обновлен: {status_text}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        await bot.change_presence(
            activity=disnake.Activity(
                type=disnake.ActivityType.watching, 
                name="Сервер оффлайн"
            )
        )

@bot.event
async def on_ready():
    print(f'✅ Бот {bot.user} запущен!')
    print(f'🎯 Подключение к {RUST_SERVER[0]}:{RUST_SERVER[1]}')
    update_rust_status.start()

@bot.command()
async def status(ctx):
    """Проверка статуса сервера"""
    try:
        info = a2s.info(RUST_SERVER, timeout=10.0)
        
        embed = disnake.Embed(
            title="🏗️ Статус Rust сервера",
            color=0x00ff00,
            description=f"**Сервер онлайн** ✅\n"
                       f"IP: `connect {RUST_SERVER[0]}:{RUST_SERVER[1]}`"
        )
        embed.add_field(name="👥 Игроки", value=f"{info.player_count}/{info.max_players}", inline=True)
        embed.add_field(name="🗺️ Карта", value=info.map_name, inline=True)
        embed.add_field(name="🆚 Версия", value=info.version, inline=True)
        embed.add_field(name="🏷️ Название", value=info.server_name, inline=False)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        embed = disnake.Embed(
            title="🏗️ Статус Rust сервера", 
            color=0xff0000,
            description=f"**Сервер оффлайн** ❌\n"
                       f"IP: `connect {RUST_SERVER[0]}:{RUST_SERVER[1]}`"
        )
        await ctx.send(embed=embed)

@bot.command()
async def connect(ctx):
    """Получить данные для подключения"""
    embed = disnake.Embed(
        title="🎮 Подключение к серверу",
        color=0x0099ff,
        description=f"```connect {RUST_SERVER[0]}:{RUST_SERVER[1]}```\n"
                   f"**Скопируй эту команду в консоль Rust (F1)**"
    )
    await ctx.send(embed=embed)

# === ЗАПУСК ===
if __name__ == "__main__":
    print("🚀 Запуск бота с портом 35210...")

    bot.run(DISCORD_BOT_TOKEN)
