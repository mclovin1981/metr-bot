"""
ГЛАВНЫЙ БОТ ДЛЯ СЕРВЕРА - РАБОТАЕТ 24/7 НА RAILWAY
"""

import asyncio
import logging
import random
import os
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.sessions import StringSession
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Импортируем настройки
from config_server import *

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class ServerMetrBot:
    def __init__(self):
        """Инициализация бота для сервера"""
        # Userbot с готовой сессией для Railway
        if 'SESSION_STRING' in os.environ and os.environ['SESSION_STRING']:
            # Используем строку сессии из переменных окружения
            session = StringSession(os.environ['SESSION_STRING'])
            self.user_client = TelegramClient(session, API_ID, API_HASH)
            logger.info("✅ Использую SESSION_STRING из переменных окружения")
        else:
            # Используем файл сессии (для локального запуска)
            self.user_client = TelegramClient('server_session', API_ID, API_HASH)
            logger.info("✅ Использую файл сессии server_session")
        
        # Бот для управления
        self.control_bot = Bot(BOT_TOKEN)
        
        # Настройки
        self.chat_id = CHAT_ID
        self.owner_id = OWNER_ID
        self.is_running = False
        self.task = None
        self.sent_count = 0
        self.last_sent = None
        
        logger.info("=" * 60)
        logger.info("🤖 SERVER METR BOT ИНИЦИАЛИЗИРОВАН")
        logger.info(f"👑 Владелец: {self.owner_id}")
        logger.info(f"🎯 Чат: {self.chat_id}")
        logger.info("=" * 60)
    
    async def connect_userbot(self):
        """Подключение userbot (от твоего имени)"""
        try:
            # Если есть SESSION_STRING - не спрашиваем код
            if 'SESSION_STRING' in os.environ and os.environ['SESSION_STRING']:
                await self.user_client.connect()
                if not await self.user_client.is_user_authorized():
                    logger.error("❌ SESSION_STRING невалидный!")
                    return False
            else:
                # Если нет SESSION_STRING - обычный вход с кодом
                await self.user_client.start(phone=PHONE)
            
            me = await self.user_client.get_me()
            logger.info(f"✅ Userbot подключен как: {me.first_name} ({me.phone})")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка подключения userbot: {e}")
            return False
    
    async def send_command_as_user(self):
        """Отправка команды от твоего имени"""
        try:
            # Вариации команды
            variations = [
                "/dick@themetrbot",
                "/dick @themetrbot",
                "/dick@themetrbot🍌",
                "/dick@themetrbot ",
            ]
            
            command = random.choice(variations)
            
            # Человеческая задержка
            await asyncio.sleep(random.uniform(1, 3))
            
            # Отправка
            await self.user_client.send_message(self.chat_id, command)
            
            self.sent_count += 1
            self.last_sent = datetime.now()
            
            logger.info(f"✅ #{self.sent_count} | Отправлено от твоего имени")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки: {e}")
            return False
    
    def calculate_interval(self):
        """Расчет интервала"""
        interval = BASE_INTERVAL
        extra = random.randint(*RANDOM_EXTRA) * 60
        jitter = random.randint(-120, 120)
        
        return interval + extra + jitter
    
    async def auto_loop(self):
        """Основной цикл авто-отправки"""
        logger.info("🔄 Авто-цикл запущен")
        
        while self.is_running:
            try:
                success = await self.send_command_as_user()
                
                if success:
                    interval = self.calculate_interval()
                    next_time = datetime.now() + timedelta(seconds=interval)
                    
                    hours = interval // 3600
                    minutes = (interval % 3600) // 60
                    
                    logger.info(f"⏰ Следующая через: {hours}ч {minutes}м")
                    logger.info(f"🕐 Время: {next_time.strftime('%H:%M:%S')}")
                    
                    # Ожидание с возможностью прерывания
                    for _ in range(interval):
                        if not self.is_running:
                            break
                        await asyncio.sleep(1)
                else:
                    await asyncio.sleep(300)  # 5 минут при ошибке
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"💥 Ошибка в цикле: {e}")
                await asyncio.sleep(60)
    
    async def start_auto(self):
        """Запуск авто-режима"""
        if self.is_running:
            return "❌ Уже запущено!"
        
        self.is_running = True
        self.task = asyncio.create_task(self.auto_loop())
        
        logger.info("🚀 Авто-режим запущен")
        return """
✅ АВТО-РЕЖИМ ЗАПУЩЕН!

🎯 Работает на сервере 24/7
📈 Отправляет от твоего имени
⏰ Интервал: ~1ч5м-1ч20м
🛑 Остановить: /stop
        """
    
    async def stop_auto(self):
        """Остановка авто-режима"""
        if not self.is_running:
            return "❌ Уже остановлено!"
        
        self.is_running = False
        
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        
        logger.info("🛑 Авто-режим остановлен")
        return "🛑 Авто-режим остановлен."
    
    async def get_status(self):
        """Получить статус"""
        if self.is_running:
            status = "🟢 РАБОТАЕТ"
            if self.last_sent:
                next_time = self.last_sent + timedelta(seconds=BASE_INTERVAL + 600)
                next_info = f"\n⏰ Следующая отправка: ~{next_time.strftime('%H:%M:%S')}"
            else:
                next_info = ""
        else:
            status = "🔴 ОСТАНОВЛЕН"
            next_info = ""
        
        return f"""
📊 СТАТУС: {status}
📈 Отправлено: {self.sent_count}
🕐 Последняя: {self.last_sent.strftime('%H:%M:%S') if self.last_sent else 'Нет'}
{next_info}
        """
    
    # Команды для управления через Telegram
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /start"""
        if update.effective_user.id != self.owner_id:
            await update.message.reply_text("⛔ Доступ запрещен!")
            return
        
        keyboard = [
            [InlineKeyboardButton("🚀 Запустить", callback_data='start')],
            [InlineKeyboardButton("🛑 Остановить", callback_data='stop')],
            [InlineKeyboardButton("📊 Статус", callback_data='status')],
            [InlineKeyboardButton("🔬 Тест", callback_data='test')],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"🤖 Управление Metr Bot\n\n{await self.get_status()}",
            reply_markup=reply_markup
        )
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик кнопок"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != self.owner_id:
            await query.edit_message_text("⛔ Доступ запрещен!")
            return
        
        if query.data == 'start':
            text = await self.start_auto()
        elif query.data == 'stop':
            text = await self.stop_auto()
        elif query.data == 'status':
            text = await self.get_status()
        elif query.data == 'test':
            # Тестовая отправка
            success = await self.send_command_as_user()
            text = "✅ Тест отправлен!" if success else "❌ Ошибка теста!"
        else:
            text = "❌ Неизвестная команда"
        
        # Обновляем кнопки
        keyboard = [
            [InlineKeyboardButton("🚀 Запустить", callback_data='start')],
            [InlineKeyboardButton("🛑 Остановить", callback_data='stop')],
            [InlineKeyboardButton("📊 Статус", callback_data='status')],
            [InlineKeyboardButton("🔬 Тест", callback_data='test')],
        ]
        
        await query.edit_message_text(
            text=f"🤖 Управление Metr Bot\n\n{text}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# Глобальный экземпляр бота
bot_instance = None

async def main():
    """Основная функция запуска"""
    global bot_instance
    
    # Создаем бота
    bot_instance = ServerMetrBot()
    
    # Подключаем userbot
    logger.info("🔗 Подключаю userbot...")
    if not await bot_instance.connect_userbot():
        logger.error("❌ Не удалось подключить userbot!")
        logger.info("ℹ️ Если на Railway: добавь SESSION_STRING в Variables")
        logger.info("ℹ️ Если локально: запусти на компьютере для получения кода")
        return
    
    # Создаем приложение для бота управления
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", bot_instance.start_command))
    app.add_handler(CallbackQueryHandler(bot_instance.button_handler))
    
    # Дополнительные команды
    async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != bot_instance.owner_id:
            await update.message.reply_text("⛔ Доступ запрещен!")
            return
        await update.message.reply_text(await bot_instance.get_status())
    
    async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != bot_instance.owner_id:
            await update.message.reply_text("⛔ Доступ запрещен!")
            return
        
        help_text = """
🤖 *Metr Bot Server Edition*

*Команды:*
/start - Панель управления
/status - Текущий статус
/help - Справка

*Как работает:*
• Работает 24/7 на Railway
• Отправляет команды от ТВОЕГО имени
• Управляется через этого бота
• Интервалы: 1ч5м-1ч20м
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    
    # Запускаем
    logger.info("=" * 60)
    logger.info("🚀 БОТ ЗАПУЩЕН НА RAILWAY!")
    logger.info(f"👑 Владелец: {OWNER_ID}")
    logger.info("📱 Напиши боту /start для управления")
    logger.info("=" * 60)
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Бесконечный цикл
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("🛑 Останавливаю бота...")
        await bot_instance.stop_auto()
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())