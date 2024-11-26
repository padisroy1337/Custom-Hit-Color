import discord
from discord.ext import commands
import datetime

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# ID канала, куда бот будет отправлять результаты
RESULT_CHANNEL_ID = 1292505242684100672  # Замените на ID вашего канала
# ID канала для логов
LOG_CHANNEL_ID = 1291835569978216468  # Замените на ID канала для логов



@bot.event
async def on_ready():
    print(f'Бот {bot.user} успешно запущен!')

@bot.command()
async def uptier(ctx, member: discord.Member, previous_tier: str, new_tier: str):
    """
    Команда для создания отчёта о повышении уровня.
    Пример использования: /uptier @User LT1 LT2
    """
    try:
        # Генерация текста для отчёта
        embed = discord.Embed(
            title=f"Результат теста {member.display_name} 🏆",
            color=discord.Color.gold(),
            timestamp=datetime.datetime.utcnow()  # Добавляем дату и время
        )
        embed.add_field(name="Никнейм", value=member.display_name, inline=False)
        embed.add_field(name="Предыдущий ранг", value=previous_tier, inline=False)
        embed.add_field(name="Новый ранг", value=new_tier, inline=False)
        embed.add_field(name="Тестер", value=ctx.author.mention, inline=False)  # Упоминание автора команды
        embed.set_thumbnail(url=member.display_avatar.url)

        # Отправка сообщения в канал с результатами
        result_channel = bot.get_channel(RESULT_CHANNEL_ID)
        if result_channel:
            await result_channel.send(embed=embed)
        else:
            await ctx.send("Не удалось найти указанный канал для отправки результатов.")
        
        # Логирование в канал с логами
        log_message = f"**Команда /uptier была выполнена**\n" \
                      f"**Дата и время:** {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n" \
                      f"**Никнейм пользователя:** {member.display_name}\n" \
                      f"**Предыдущий ранг:** {previous_tier}\n" \
                      f"**Новый ранг:** {new_tier}\n" \
                      f"**Тестер:** {ctx.author.mention}\n"
        
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed_log = discord.Embed(
                title="Лог выполнения команды /uptier",
                description=log_message,
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            await log_channel.send(embed=embed_log)
        
    except Exception as e:
        await ctx.send(f"Произошла ошибка: {e}")

# Замените на ваш токен
bot.run('MTMxMDk0MTc4NTE2OTU5MjM5Mg.Gfb_hl.ecCeBgyaDEOw4hQAhAG8es3HezGQSzebBpEVZM')
