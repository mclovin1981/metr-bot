"""
НАСТРОЙКИ ДЛЯ RAILWAY
"""

import os

# Telegram API
API_ID = int(os.environ.get('API_ID', 34500729))
API_HASH = os.environ.get('API_HASH', 'f96cb319a0a1fd63720dd01c4d33a587')
PHONE = os.environ.get('PHONE', '+79136189187')

# Чат с @themetrbot
CHAT_ID = -1003103373741

# Бот для управления (создан через @BotFather)
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8084093954:AAFzhWwWCV5TTtsUBb5Uqn6Ln9k4jgT1Oxc')

# Твой Telegram ID
OWNER_ID = int(os.environ.get('OWNER_ID', 5682286025))

# Настройки отправки
BASE_INTERVAL = 3780  # 1 час 3 минуты
RANDOM_EXTRA = (5, 15)  # +5-15 минут случайности
HUMAN_MODE = True