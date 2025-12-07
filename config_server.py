"""
НАСТРОЙКИ ДЛЯ RAILWAY
ВСЕ ДАННЫЕ БЕРУТСЯ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ!
Никаких реальных токенов/паролей в коде!
"""

import os

# ============================================
# ОБЯЗАТЕЛЬНЫЕ ПЕРЕМЕННЫЕ (должны быть на Railway)
# ============================================

# Telegram API (получить на my.telegram.org)
API_ID = int(os.environ['API_ID'])  # Если нет - будет ошибка
API_HASH = os.environ['API_HASH']   # Если нет - будет ошибка

# Твой номер телефона
PHONE = os.environ['PHONE']         # Если нет - будет ошибка

# Токен бота управления (получить у @BotFather)
BOT_TOKEN = os.environ['BOT_TOKEN'] # Если нет - будет ошибка

# Твой Telegram ID (узнать у @userinfobot)
OWNER_ID = int(os.environ['OWNER_ID'])  # Если нет - будет ошибка

# Строка сессии (получить запуском get_session.py)
SESSION_STRING = os.environ.get('SESSION_STRING', '')

# ============================================
# ОПЦИОНАЛЬНЫЕ НАСТРОЙКИ (можно изменить)
# ============================================

# ID чата с @themetrbot
CHAT_ID = int(os.environ.get('CHAT_ID', -1003103373741))

# Базовый интервал в секундах (1 час 3 минуты)
BASE_INTERVAL = int(os.environ.get('BASE_INTERVAL', 3780))

# Случайное добавление к интервалу в минутах
RANDOM_EXTRA = (
    int(os.environ.get('RANDOM_EXTRA_MIN', 5)),
    int(os.environ.get('RANDOM_EXTRA_MAX', 15))
)

# Человеческий режим (добавляет случайные задержки)
HUMAN_MODE = os.environ.get('HUMAN_MODE', 'True').lower() == 'true'

# Временная зона для логов (Europe/Moscow, UTC, etc)
TIMEZONE = os.environ.get('TIMEZONE', 'Europe/Moscow')

# ============================================
# ПРОВЕРКА КОНФИГУРАЦИИ
# ============================================

def check_config():
    """Проверяет что все обязательные переменные заданы"""
    required_vars = ['API_ID', 'API_HASH', 'PHONE', 'BOT_TOKEN', 'OWNER_ID']
    
    missing = []
    for var in required_vars:
        if var not in os.environ:
            missing.append(var)
    
    if missing:
        raise ValueError(f"❌ Отсутствуют обязательные переменные: {', '.join(missing)}\n"
                        f"Добавь их на Railway → Variables")
    
    print("✅ Конфигурация загружена успешно")
    print(f"   👤 Владелец: {OWNER_ID}")
    print(f"   📱 Номер: {PHONE}")
    print(f"   💬 Чат: {CHAT_ID}")
    print(f"   ⏰ Интервал: ~{BASE_INTERVAL//3600}ч {(BASE_INTERVAL%3600)//60}м")

# Автопроверка при импорте
if __name__ != "__main__":
    check_config()

# ============================================
# ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ
# ============================================

# Максимальное количество ошибок перед перезапуском
MAX_ERRORS = int(os.environ.get('MAX_ERRORS', 5))

# Пауза при ошибке в секундах
ERROR_COOLDOWN = int(os.environ.get('ERROR_COOLDOWN', 300))

# Логирование (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# Сохранять ли логи в файл
LOG_TO_FILE = os.environ.get('LOG_TO_FILE', 'False').lower() == 'true'
LOG_FILE = os.environ.get('LOG_FILE', 'bot.log')

if __name__ == "__main__":
    # Показать текущие настройки (без токенов)
    print("=" * 60)
    print("🤖 METR BOT CONFIGURATION")
    print("=" * 60)
    print(f"API_ID: {'*' * len(str(API_ID)) if API_ID else 'NOT SET'}")
    print(f"API_HASH: {'*' * 20 if API_HASH else 'NOT SET'}")
    print(f"PHONE: {PHONE[:4] + '*' * (len(PHONE)-4) if PHONE else 'NOT SET'}")
    print(f"BOT_TOKEN: {'*' * 20 if BOT_TOKEN else 'NOT SET'}")
    print(f"OWNER_ID: {OWNER_ID}")
    print(f"SESSION_STRING: {'SET' if SESSION_STRING else 'NOT SET'}")
    print(f"CHAT_ID: {CHAT_ID}")
    print(f"BASE_INTERVAL: {BASE_INTERVAL}s ({BASE_INTERVAL//3600}h {BASE_INTERVAL%3600//60}m)")
    print(f"RANDOM_EXTRA: {RANDOM_EXTRA[0]}-{RANDOM_EXTRA[1]}m")
    print(f"HUMAN_MODE: {HUMAN_MODE}")
    print(f"TIMEZONE: {TIMEZONE}")
    print("=" * 60)
    print("⚠️  Этот файл должен быть БЕЗ реальных токенов!")
    print("⚠️  Все данные должны быть в Railway Variables!")
    print("=" * 60)
