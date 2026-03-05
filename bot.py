import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import threading
import os
import sys

from flask import Flask
import threading

# Заглушка для Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_web, daemon=True).start()

# ===== ВРЕМЕННОЕ РЕШЕНИЕ ДЛЯ ЛОКАЛЬНОГО ЗАПУСКА =====
# Вставьте свой токен между кавычками
VK_TOKEN = "vk1.a.Y1rZa7LjxqSIA4lZlb9LcOcgsbNhAaX-nbjwYNRHnqHnB8ExKfp1u6kX73C7xvXoQQIaJDPgtdia01ynra_tPLjY6hDmMG-OpzLd9Nvb52diHL0kWJz9XxaCfjM8S4yWrzsl5xPH17FgpWVpZVr6xLjvGFXuD-oERc2twg8AWE3wRJKoLsRxAVDP6-ePKJPU2X_sgdzmIeMyyc_8amju7g"
SPREADSHEET_NAME = 'Raspisanie_1_chetverti(1)'


# ========== РАСПИСАНИЕ ДЛЯ 10-11 КЛАССОВ ==========
high_school_schedule = {
    '10А': """
📚 10А
📍 Каб: 425
══════════════════════════════

📅 ПОНЕДЕЛЬНИК
   8:00
   1. англ.В 350
   2. литер.В 425
   3. ист.А 425 / ист.В 427
   4. ист.А 425 / ист.В 427
   5. алгебра А 228/алгебра B1 425/алгебра В2  427
   6. алгебра А 228/алгебра B1 425/алгебра В2  427
   7. обществознание В 425        

📅 ВТОРНИК
   1. обществ. В 425/обществ. А 427
   2. обществ. В 425/обществ. А 427
   3. обществознание В 425
   4. обществ. В 425 / обществ. А 427
   5. физ-ра
   6. физ-ра
   7. ВиС А 227/геом.В1 425/геом.В2 427       
   8. геом.В1 425/геом.В2 427         
   


📅 СРЕДА
   8:50
   1. алг.В1 425/алг.В2  427 /история В  352       
   2. алг.В1 425/алг.В2  427/история В   351         
   3. литер.А 425/литер.В 351
   4. литер.А 425/литер.В 351
   5. англ. В 350
   6. англ. В 350


📅 ЧЕТВЕРГ
   1. англ.В 350/англ.А 225
   2. англ.В 350/англ.А 225
   3. геом. А 228/геом.В1 427/геом.В2 425  
   4. алг.А    228/ВиС В1  427/ВиС   В2  425  
   5. русский язык
   6. русский язык
   7. обществознание В 425

📅 ПЯТНИЦА
   1. литер.В
   2. литер.В
   3. ОБЗР
   4. физика А
   5. индив. проект
   6. литература А
""",
    
    '10Б': """
📚 10Б
📍 Каб: 427
══════════════════════════════

📅 ПОНЕДЕЛЬНИК
   1. 8:00
   2. история А 427
   2. история А 427
   3. химия В 156 / ИКТ В 230
   4. химия В 156 / ИКТ В 230
   5. алгебра А 228/алгебра В1 425/алгебра В2  427
   6. алгебра А 228/алгебра В1 425/алгебра В2  427 
   7. обществознание В 425        

📅 ВТОРНИК
   1. обществ. В 425/обществ. А 427
   2. обществ. В 425/обществ. А 427
   3. русский язык
   4. русский язык
   5. ВиС А 227/геом.В1 425/геом.В2 427       
   6. геом.В1 425/геом.В2 427         

📅 СРЕДА
   1. литер.А
   2. алг.В1 425/алг.В2  427 /история В  352       
   3. алг.В1 425/алг.В2  427/история В   351
   4. физ. В 404/физика А 427
   5. физ. В 352/биол. В 427
   6. физ. В 352/биол. В 427             

📅 ЧЕТВЕРГ
   1. литер.А
   2. литер.А
   3. геом. А 228/геом.В1 427/геом.В2 425
   4. алг.А    228/ВиС В1  427/ВиС   В2  425  
   5. англ.А
   6. ОБЗР
   7. обществознание В 425


📅 ПЯТНИЦА
   1. физ-ра
   2. физ-ра
   3. хим.В 155/ИКТ В 427
   4. хим.В 155/ИКТ В 427
   5. англ.А
   6. индив. проект
""",
    
    '11А': """
📚 11А
📍 Каб: 228
══════════════════════════════

📅 ПОНЕДЕЛЬНИК
   1. [8:00] алгебра
   2. геометрия
   3. русский язык
   4. литература

📅 ВТОРНИК
   5. [8:50] физика
   6. информатика
   7. история
   8. обществознание

📅 СРЕДА
   9. [9:40] биология
   10. химия
   11. англ.яз.
   12. физ-ра

📅 ЧЕТВЕРГ
   13. [10:30] алгебра
   14. геометрия
   15. русский язык
   16. литература

📅 ПЯТНИЦА
   17. [11:20] физика
   18. информатика
   19. история
   20. обществознание
""",
    
    '11Б': """
📚 11Б
📍 Каб: 227
══════════════════════════════

📅 ПОНЕДЕЛЬНИК
   1. [8:00] русский язык
   2. литература
   3. алгебра
   4. геометрия

📅 ВТОРНИК
   5. [8:50] история
   6. обществознание
   7. физика
   8. информатика

📅 СРЕДА
   9. [9:40] химия
   10. биология
   11. англ.яз.
   12. физ-ра

📅 ЧЕТВЕРГ
   13. [10:30] русский язык
   14. литература
   15. алгебра
   16. геометрия

📅 ПЯТНИЦА
   17. [11:20] история
   18. обществознание
   19. физика
   20. информатика
"""
}

# ================================

# Кэш для данных
cache = {
    'data': None,
    'time': 0
}
CACHE_TTL = 300  # 5 минут

print("🚀 Бот запускается...")

# Подключение к Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME)
worksheet = sheet.get_worksheet(0)
print("✅ Подключился к Google Sheets!")

# Подключение к ВК
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# Словари для классов
all_classes = {}
classes_by_parallel = {
    '5': [], '6': [], '7': [], '8': [], '9': [], '10': [], '11': []
}

def update_cache():
    """Обновляет кэш данных"""
    global cache
    try:
        print("🔄 Обновление кэша...")
        cache['data'] = worksheet.get_all_values()
        cache['time'] = time.time()
        print(f"✅ Кэш обновлён, строк: {len(cache['data'])}")
    except Exception as e:
        print(f"❌ Ошибка обновления кэша: {e}")

def get_cached_data():
    """Получает данные из кэша"""
    if not cache['data'] or time.time() - cache['time'] > CACHE_TTL:
        update_cache()
    return cache['data']

def find_all_classes():
    """Находит все классы 5-11"""
    global all_classes, classes_by_parallel
    try:
        data = get_cached_data()
        headers = data[0]
        
        for i, header in enumerate(headers):
            if header and header.strip():
                if 'к.' in header:
                    class_name = header.split('к.')[0].strip()
                else:
                    class_name = header.strip()
                
                # Нормализуем буквы
                class_name = (class_name
                    .replace('A', 'А').replace('B', 'Б').replace('C', 'В')
                    .replace('D', 'Г').replace('E', 'Д').replace('F', 'Е'))
                
                if class_name and class_name[0].isdigit():
                    if class_name.startswith('10'):
                        parallel = '10'
                    elif class_name.startswith('11'):
                        parallel = '11'
                    else:
                        parallel = class_name[0]
                    
                    if parallel in ['5','6','7','8','9','10','11']:
                        all_classes[class_name] = i
                        if class_name not in classes_by_parallel[parallel]:
                            classes_by_parallel[parallel].append(class_name)
        
        for p in classes_by_parallel:
            classes_by_parallel[p].sort()
        
        print(f"✅ Найдено классов 5-11: {len(all_classes)}")
        for p in ['5','6','7','8','9','10','11']:
            print(f"{p} классы: {classes_by_parallel[p]}")
            
    except Exception as e:
        print(f"❌ Ошибка поиска классов: {e}")

# Загружаем классы
find_all_classes()

def create_main_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('📚 Выбрать параллель', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('❓ Помощь', color=VkKeyboardColor.SECONDARY)
    return keyboard

def create_parallel_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('5 классы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('6 классы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('7 классы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('8 классы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('9 классы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('10 классы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('11 классы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад', color=VkKeyboardColor.NEGATIVE)
    return keyboard

def create_class_keyboard(parallel):
    keyboard = VkKeyboard(one_time=False)
    classes = classes_by_parallel.get(parallel, [])
    
    for i in range(0, len(classes), 2):
        if i + 1 < len(classes):
            keyboard.add_button(classes[i], color=VkKeyboardColor.PRIMARY)
            keyboard.add_button(classes[i+1], color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
        else:
            keyboard.add_button(classes[i], color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
    
    keyboard.add_button('🔙 Назад к параллелям', color=VkKeyboardColor.NEGATIVE)
    return keyboard

def get_schedule_from_table(class_name):
    """Получает расписание из таблицы для 5-9 классов"""
    try:
        if class_name not in all_classes:
            return f"❌ Класс {class_name} не найден"
        
        class_col = all_classes[class_name]
        data = get_cached_data()
        
        # Получаем кабинет
        header = data[0][class_col]
        cabinet = "—"
        if 'к.' in header:
            cabinet = header.split('к.')[-1].strip()
        
        # Диапазоны для дней
        day_ranges = {
            'понедельник': (2, 11),
            'вторник': (13, 22),
            'среда': (23, 32),
            'четверг': (33, 42),
            'пятница': (43, 58),
        }
        
        days_russian = {
            'понедельник': 'ПОНЕДЕЛЬНИК',
            'вторник': 'ВТОРНИК', 
            'среда': 'СРЕДА',
            'четверг': 'ЧЕТВЕРГ',
            'пятница': 'ПЯТНИЦА',
        }
        
        schedule_by_day = {}
        
        for day, (start, end) in day_ranges.items():
            lessons = []
            current_time = None
            lesson_num = 1
            
            for row_idx in range(start, min(end + 1, len(data))):
                row = data[row_idx]
                if len(row) > class_col:
                    subject = row[class_col].strip() if row[class_col] else ""
                    
                    # Если это время
                    if ':' in subject:
                        current_time = subject
                        continue
                    
                    # Если это урок
                    if subject and 'к.' not in subject and not subject.isdigit():
                        subject = ' '.join(subject.split())
                        
                        # Убираем цифры в начале
                        if subject and subject[0].isdigit():
                            parts = subject.split(' ', 1)
                            if len(parts) > 1:
                                subject = parts[1]
                            else:
                                continue
                        
                        # Форматируем сдвоенные уроки
                        if '/' in subject:
                            parts = subject.split('/')
                            subject = ' / '.join([p.strip() for p in parts])
                        
                        # Добавляем урок
                        if current_time:
                            lessons.append(f"{lesson_num}. [{current_time}] {subject}")
                        else:
                            lessons.append(f"{lesson_num}. {subject}")
                        lesson_num += 1
            
            if lessons:
                schedule_by_day[day] = lessons
        
        # Формируем ответ
        response = f"📚 {class_name}\n📍 Каб: {cabinet}\n"
        response += "═" * 30 + "\n\n"
        
        for day, lessons in schedule_by_day.items():
            response += f"📅 {days_russian[day]}\n"
            for lesson in lessons:
                response += f"   {lesson}\n"
            response += "\n"
        
        return response
        
    except Exception as e:
        print(f"Ошибка в get_schedule_from_table: {e}")
        return f"❌ Ошибка при получении расписания"

def send(user_id, message, keyboard=None):
    try:
        if keyboard:
            vk.messages.send(
                user_id=user_id,
                message=message,
                keyboard=keyboard.get_keyboard(),
                random_id=0
            )
        else:
            vk.messages.send(
                user_id=user_id,
                message=message,
                random_id=0
            )
        time.sleep(0.3)
    except Exception as e:
        print(f"Ошибка отправки: {e}")

# Фоновое обновление кэша
def background_cache_updater():
    while True:
        time.sleep(240)
        update_cache()

threading.Thread(target=background_cache_updater, daemon=True).start()

print("✅ Бот готов! Жду сообщения...")

# Основной цикл
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.strip()
        user_id = event.user_id
        
        try:
            if msg.lower() in ['начать', 'start', 'меню']:
                send(user_id, 
                     '👋 Привет! Я бот с расписанием Гимназии №3',
                     create_main_keyboard())
            
            elif msg == '📚 Выбрать параллель':
                send(user_id, 
                     '📚 Выбери параллель (5-11):',
                     create_parallel_keyboard())
            
            elif msg in ['5 классы', '6 классы', '7 классы', '8 классы', 
                         '9 классы', '10 классы', '11 классы']:
                parallel = msg[0:2] if msg.startswith(('10', '11')) else msg[0]
                send(user_id,
                     f'📚 Выбери класс в {parallel} параллели:',
                     create_class_keyboard(parallel))
            
            elif msg in all_classes:
                # Для 10-11 классов берем готовое расписание
                if msg in high_school_schedule:
                    schedule = high_school_schedule[msg]
                else:
                    schedule = get_schedule_from_table(msg)
                send(user_id, schedule)
                time.sleep(1)
                send(user_id, '👋 Выбери действие:', create_main_keyboard())
            
            elif msg == '❓ Помощь' or msg.lower() == 'помощь':
                send(user_id, 
                     'Нажми "📚 Выбрать параллель", выбери параллель, потом класс')
            
            elif msg == '🔙 Назад':
                send(user_id, '👋 Главное меню:', create_main_keyboard())
            
            elif msg == '🔙 Назад к параллелям':
                send(user_id, '📚 Выбери параллель:', create_parallel_keyboard())
            
            else:
                send(user_id, 'Напиши "меню" для начала')
                
        except Exception as e:
            print(f"Ошибка: {e}")
            send(user_id, "Произошла ошибка, попробуй еще раз")
