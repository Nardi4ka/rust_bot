import disnake
from disnake.ext import commands, tasks
import a2s
import os
from flask import Flask
from threading import Thread

# === КОНФИГУРАЦИЯ ===
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ Токен не найден!")
    exit(1)

RUST_SERVER = ("185.189.255.113", 35210)

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# === Flask сервер для UptimeRobot ===
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Rust Bot is running!", 200

@app.route('/health')
def health():
    return "✅ OK", 200

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# === Функции бота ===
@tasks.loop(minutes=3)
async def update_rust_status():
    try:
        info = a2s.info(RUST_SERVER, timeout=10.0)
        status_text = f"{info.player_count}/{info.max_players} игроков"
        await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name=status_text))
        print(f"✅ Статус: {status_text}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name="Сервер оффлайн"))

@bot.event
async def on_ready():
    print(f'✅ Бот {bot.user} запущен!')
    update_rust_status.start()

@bot.command()
async def status(ctx):
    try:
        info = a2s.info(RUST_SERVER, timeout=10.0)
        embed = disnake.Embed(title="🏗️ Статус Rust", color=0x00ff00)
        embed.add_field(name="👥 Игроки", value=f"{info.player_count}/{info.max_players}")
        embed.add_field(name="🗺️ Карта", value=info.map_name)
        await ctx.send(embed=embed)
    except:
        embed = disnake.Embed(title="🏗️ Статус Rust", color=0xff0000, description="❌ Сервер оффлайн")
        await ctx.send(embed=embed)

if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    Thread(target=run_flask, daemon=True).start()
    print("🚀 Запуск бота с веб-сервером...")
    bot.run(BOT_TOKEN)





