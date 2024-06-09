import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B5%D0%B9_%D1%81%D0%B5%D1%80%D0%B8%D0%B8_%D1%80%D0%BE%D0%BC%D0%B0%D0%BD%D0%BE%D0%B2_%D0%BE_%D0%93%D0%B0%D1%80%D1%80%D0%B8_%D0%9F%D0%BE%D1%82%D1%82%D0%B5%D1%80%D0%B5"

# Запрос к странице
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Создание списков для данных
names = []
english_names = []
genders = []
houses = []
blood_statuses = []
positions = []

# Функция для извлечения английского имени
def extract_english_name(name):
    if '(англ.' in name:
        start = name.find('(англ.') + 6
        end = name.find(')', start)
        return name[start:end].split(",")[0].strip()
    return 'Неизвестно'

# Функция для обработки английского имени
def process_english_name(name):
    name = name.split('(')[0].strip()  # Удаляем все после "("
    if ',' in name:
        name = name.split(',')[0].strip()  # Удаляем все после ","
    words = name.split()
    if len(words) > 2:
        name = f"{words[0]} {words[-1]}"
    return name

# Функция для очистки имени персонажа
def clean_character_name(name):
    if '(' in name:
        name = name.split('(')[0].strip()
    if '—' in name:
        name = name.split('—')[0].strip()
    if 'Основная статья:' in name:
        name = name.split('Основная статья:')[0].strip()
    return name

# Извлечение таблиц с персонажами
tables = soup.find_all('table', {"class": "wikitable"})

# Обработка таблиц для извлечения данных персонажей
for table in tables:
    rows = table.find_all('tr')
    headers = [header.text.strip() for header in rows[0].find_all('th')]

    try:
        name_index = headers.index('Имя')
        gender_index = headers.index('Пол')
        blood_status_index = headers.index('Чистота крови')
        faculty_index = headers.index('Факультет') if 'Факультет' in headers else None
    except ValueError as e:
        continue

    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) <= name_index:
            continue
        name = clean_character_name(cols[name_index].text.strip())
        if name in ['', '...', '. . .']:
            continue
        english_name = extract_english_name(cols[name_index].text.strip())
        english_name = process_english_name(english_name)
        gender = cols[gender_index].text.strip() if gender_index < len(cols) else 'Неизвестно'
        blood_status = cols[blood_status_index].text.strip() if blood_status_index < len(cols) else 'Неизвестно'
        faculty = cols[faculty_index].text.strip() if faculty_index and faculty_index < len(cols) else 'Неизвестно'

        names.append(name)
        english_names.append(english_name)
        genders.append(gender)
        houses.append(faculty)
        blood_statuses.append(blood_status)
        positions.append('Неизвестно')

# Дополнительная информация для конкретных персонажей
for i, name in enumerate(names):
    if name == "Помона Стебль":
        houses[i] = "Пуффендуй"
    elif name == "Регулус Блэк":
        houses[i] = "Слизерин"
    elif name == "Флёр Дела́кур":
        english_names[i] = "Fleur Delacour"
    elif name == "Ви́ктор Крам":
        english_names[i] = "Viktor Krum"
    elif name == "Бартемиус Крауч-младший":
        english_names[i] = "Bartemius Crouch, Jr."
    elif name == "Бартемиус «Ба́рти» Крауч-старший":
        english_names[i] = "Bartemius Crouch, Sr."
    elif name == "Джордж Фабиан Уизли":
        genders[i] = "мужской"
        blood_statuses[i] = "чистокровный"
    elif name == "Фредерик Гидеон Уизли":
        blood_statuses[i] = "чистокровный"
    elif name == "Ру́фус Скри́мджер":
        houses[i] = "Неизвестно"
    elif name == "Корне́лиус Фадж":
        houses[i] = "Когтевран"
    elif name == "Нимфадо́ра Лю́пин":
        houses[i] = "Пуффендуй"
    elif name == "А́льбус Да́мблдор":
        blood_statuses[i] = "полукровка"
    elif name == "Дже́ймс По́ттер":
        blood_statuses[i] = "чистокровный"

# Список студентов
students = ["Га́рри Дже́ймс По́ттер", "Ро́нальд Би́лиус Уи́зли", "Гермио́на Джин Гре́йнджер",
            "Джине́вра Мо́лли Уи́зли", "Фредерик Гидеон Уизли", "Джордж Фабиан Уизли",
            "Пе́рси Игна́циус Уи́зли", "Не́вилл Долгопу́пс", "Дра́ко Лю́циус Малфой",
            "Ви́нсент Крэбб", "Гре́гори Гойл", "Пэ́нси Па́ркинсон", "Полу́мна", "Се́дрик Ди́ггори"]

# Список преподавателей и персонала
staff = ["А́льбус Да́мблдор", "Мине́рва Макго́нагалл", "Се́верус Снегг", "Ру́беус Ха́грид",
         "Квири́нус Кви́ррелл", "Златопуст Ло́конс", "Фи́лиус Фли́твик", "Сивилла Трелони",
         "Гора́ций Слизнорт", "А́ргус Филч"]

# Список Ордена Феникса
order_of_the_phoenix = ["Дже́ймс По́ттер", "Ли́ли По́ттер", "Си́риус Блэк", "Ри́мус Лю́пин",
                        "Нимфадо́ра Лю́пин", "Арабе́лла До́рин Фигг", "Назе́мникус Фле́тчер",
                        "Ала́стор Грюм", "Уи́льям Би́лли Уи́зли", "Чарльз А́ртур Уи́зли",
                        "А́ртур Уи́зли", "Мо́лли Уи́зли"]

# Список Пожирателей Смерти
death_eaters = ["Волан-де-Мо́рт", "Беллатри́са Лестре́йндж", "Лю́циус Малфой",
                "Нарци́сса Малфой", "Бартемиус Крауч-младший", "Пи́тер Петтигрю"]

# Список Министерства магии
ministry_of_magic = ["Ки́нгсли Бру́ствер", "Корне́лиус Фадж", "Бартемиус «Ба́рти» Крауч-старший",
                     "Ру́фус Скри́мджер", "Доло́рес А́мбридж"]

# Присвоение должностей
for i, name in enumerate(names):
    if name in students:
        positions[i] = "Студент"
    elif name in staff:
        positions[i] = "Преподаватели и Персонал"
    elif name in order_of_the_phoenix:
        positions[i] = "Орден Феникса"
    elif name in death_eaters:
        positions[i] = "Пожиратели Смерти"
    elif name in ministry_of_magic:
        positions[i] = "Министерство магии"
    else:
        positions[i] = "Неизвестно"

# Добавление факультетов для некоторых персонажей
gryffindor_students = ["Га́рри Дже́ймс По́ттер", "Ро́нальд Би́лиус Уи́зли", "Гермио́на Джин Гре́йнджер",
                       "Джине́вра Мо́лли Уи́зли", "Фредерик Гидеон Уизли", "Джордж Фабиан Уизли",
                       "Пе́рси Игна́циус Уи́зли", "Не́вилл Долгопу́пс"]
slytherin_students = ["Дра́ко Лю́циус Малфой", "Ви́нсент Крэбб", "Гре́гори Гойл", "Пэ́нси Па́ркинсон"]
ravenclaw_students = ["Полу́мна"]
hufflepuff_students = ["Се́дрик Ди́ггори"]

for i, name in enumerate(names):
    if name in gryffindor_students:
        houses[i] = "Гриффиндор"
    elif name in slytherin_students:
        houses[i] = "Слизерин"
    elif name in ravenclaw_students:
        houses[i] = "Когтевран"
    elif name in hufflepuff_students:
        houses[i] = "Пуффендуй"

# Создание основного DataFrame
df = pd.DataFrame({
    "Имя": names,
    "Имя на английском": english_names,
    "Пол": genders,
    "Факультет": houses,
    "Чистота крови": blood_statuses,
    "Должность": positions
})

# Информация о дополнительных персонажах
additional_characters = [
    ('Лава́нда Бра́ун', 'Lavender Brown', 'женский', 'Гриффиндор', 'Неизвестно', 'Студент'),
    ('Си́мус Фи́нниган', 'Seamus Finnigan', 'мужской', 'Гриффиндор', 'Неизвестно', 'Студент'),
    ('Парвати Патил', 'Parvati Patil', 'женский', 'Гриффиндор', 'Неизвестно', 'Студент'),
    ('Дин То́мас', 'Dean Thomas', 'мужской', 'Гриффиндор', 'Неизвестно', 'Студент'),
    ('О́ливер Вуд', 'Oliver Wood', 'мужской', 'Гриффиндор', 'Неизвестно', 'Студент'),
    ('Кэ́ти Белл', 'Katie Bell', 'женский', 'Гриффиндор', 'Неизвестно', 'Студент'),
    ('Ли Джо́рдан', 'Lee Jordan', 'мужской', 'Гриффиндор', 'Неизвестно', 'Студент'),
    ('Анджели́на Джо́нсон', 'Angelina Johnson', 'женский', 'Гриффиндор', 'Неизвестно', 'Студент'),
    ('Ко́лин Кри́ви', 'Colin Creevey', 'мужской', 'Гриффиндор', 'Неизвестно', 'Студент'),
    ('Ма́ркус Флинт', 'Marcus Flint', 'мужской', 'Слизерин', 'Неизвестно', 'Студент'),
    ('Чжо́у Чанг', 'Cho Chang', 'женский', 'Когтевран', 'Неизвестно', 'Студент'),
    ('Те́рри Бут', 'Terry Boot', 'мужской', 'Когтевран', 'Неизвестно', 'Студент'),
    ('Майкл Ко́рнер', 'Michael Corner', 'мужской', 'Когтевран', 'Неизвестно', 'Студент'),
    ('Мариэ́тта Э́джком', 'Marietta Edgecombe', 'женский', 'Когтевран', 'Неизвестно', 'Студент'),
    ('Ро́джер Дэ́вис', 'Roger Davies', 'мужской', 'Когтевран', 'Неизвестно', 'Студент'),
    ('Джа́стин Финч-Фле́тчли', 'Justin Finch-Fletchley', 'мужской', 'Пуффендуй', 'Неизвестно', 'Студент'),
    ('Ханна Аббот', 'Hannah Abbott', 'женский', 'Пуффендуй', 'Неизвестно', 'Студент'),
    ('Эрни Макми́ллан', 'Ernie Macmillan', 'мужской', 'Пуффендуй', 'Неизвестно', 'Студент'),
    ('Заха́рия Смит', 'Zacharias Smith', 'мужской', 'Пуффендуй', 'Неизвестно', 'Студент'),
    ('Помо́на Стебль', 'Pomona Sprout', 'женский', 'Пуффендуй', 'Неизвестно', 'Преподаватели и Персонал')
]

# Создание DataFrame для дополнительных персонажей
df_additional = pd.DataFrame(additional_characters, columns=["Имя", "Имя на английском", "Пол", "Факультет", "Чистота крови", "Должность"])

# Объединение основного и дополнительного DataFrame
df_combined = pd.concat([df, df_additional], ignore_index=True)

# Удаление строк, где "Имя на английском" равно "Неизвестно"
df_combined = df_combined[df_combined["Имя на английском"] != "Неизвестно"]
df_combined = df_combined[df_combined["Имя"] != "Полумна Лавгуд"]
df_combined = df_combined[df_combined["Имя"] != "Сириус Блэк"]
df_combined = df_combined[df_combined["Имя"] != "Питер Петтигрю"]
df_combined = df_combined[df_combined["Имя"] != "Лили Поттер"]

english = pd.DataFrame(df_combined, columns=["Имя на английском"])

# Сохранение объединенного DataFrame в .csv файл
df_combined.to_csv("harry_potter_characters.csv", index=False, encoding='utf-8-sig')
english.to_csv('english_names.csv', index=False, encoding='utf-8-sig')
