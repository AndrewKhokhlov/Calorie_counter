import json
import datetime
import os
import csv

print("Привет! Это калькулятор калорий.")

try:
    with open("calories.json", "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content:  
            products = json.loads(content)
        else:
            products = {}
except FileNotFoundError:
    products = {}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def add_product():
        name = input("Введите название продукта: ").strip().casefold()
        calories = int(input("Введите количество калорий: "))
        data_added = datetime.date.today().isoformat()
        products[name] = {"value": calories, "date": data_added}
        save_data()
        print(f"Продукт {name} с {calories} калориями добавлен, {data_added}.")
        input("\nНажмите Enter, чтобы вернуться в меню...")
        clear_screen()
    
def show_products():
    if not products:
        print("Список продуктов пуст.")
    else:
        print("Список продуктов:")
        days = {}
        no_date = []
        for name, info in products.items():
            if isinstance(info, dict) and "date" in info:
                date = info["date"]
                if date not in days:
                    days[date] = []
                days[date].append((name, info["value"]))
            else:
                no_date.append((name, info if not isinstance(info, dict) else info.get("value", 0)))

        for date in sorted(days.keys()):
            print(f"Дата: {date}")
            for name, value in days[date]:
                print(f"  {name}: {value} калорий")

        if no_date:
            print("Без даты:")
            for name, value in no_date:
                print(f"  {name}: {value} калорий")
    input("\nНажмите Enter, чтобы вернуться в меню...")
    clear_screen()

def delete_product():
    name = input("Введите название продукта для удаления: ").strip().casefold()
    if name in products:
        del products[name]
        save_data()
        print(f"Продукт {name} удален.")
    else:
        print(f"Продукт {name} не найден.")
    input("\nНажмите Enter, чтобы вернуться в меню...")
    clear_screen()

def calculate_calories():
        total_calories = 0
        for info in products.values():
            if isinstance(info, dict):
                total_calories += info.get("value", 0)
            else:
                total_calories += info
        print(f"Общее количество калорий: {total_calories}")
        input("\nНажмите Enter, чтобы вернуться в меню...")
        clear_screen()

def search_products():
    name = input("Введите название продукта: ").strip().casefold()
    if name in products:
        info = products[name]
        if isinstance(info, dict):
            print(f"Калории {name} ровняются {info['value']} (дата добавления: {info.get('date', '-')})")
        else:
            print(f"Калории {name} ровняются {info}")
    else:
        print(f"Продукт {name} не найден.")

    input("\nНажмите Enter, чтобы вернуться в меню...")
    clear_screen()

def clean_all():
    delete_all = input("Вы уверенны что готовы очистить все данные?\nВведите Да или Нет\n").strip().casefold()
    if delete_all == 'Да':
        products.clear()
        save_data()
        print("Все данные очищены.")
    else:
        print("Очистка данных отменена.")
    input("\nНажмите Enter, чтобы вернуться в меню...")
    clear_screen()

def edit_product():
    name = input("Введите название продукта для редактирования: ").strip().casefold()
    if name in products:
        new_calories = int(input(f"Введите новое количество калорий для {name}: "))
        if isinstance(products[name], dict):
            products[name]["value"] = new_calories
        else:
            products[name] = {"value": new_calories, "date": datetime.date.today().isoformat()}
        print(f"Продукт {name} обновлен до {new_calories} калорий.")
        save_data()
    else:
        print(f"Продукт {name} не найден.")
    input("\nНажмите Enter, чтобы вернуться в меню...")
    clear_screen()

def sort_products():
    sort = input("В каком Вы хотите виде видить свой список?\n1. По алфавиту?\n2. По калорийности? ")
    def get_calories(info):
        if isinstance(info, dict):
            return info.get("value", 0)
        return info
    if sort == '1':
        sorted_items = sorted(products.items())
        for name, info in sorted_items:
            if isinstance(info, dict):
                print(f"{name}: {info['value']} калорий (дата добавления: {info.get('date', '-')})")
            else:
                print(f"{name}: {info} калорий")
    else:
        sorted_item1 = sorted(products.items(), key=lambda item: get_calories(item[1]), reverse=True)
        for name, info in sorted_item1:
            if isinstance(info, dict):
                print(f"{name}: {info['value']} калорий (дата добавления: {info.get('date', '-')})")
            else:
                print(f"{name}: {info} калорий")
    input("\nНажмите Enter, чтобы вернуться в меню...")
    clear_screen()

def mini_report():
    key_count = len(products)

    calories_list = [info["value"] if isinstance(info, dict) else info for info in products.values()]
    if calories_list:
        avg_calories = sum(calories_list) / len(calories_list)
        max_calories = max(calories_list)
    else:
        avg_calories = 0
        max_calories = 0

    print(f"Количество продуктов в списке: {key_count}")
    print(f"Cреднее количество калорий: {avg_calories}")
    print(f"Продукт с наибольшей калорийностью: {max_calories}")

    input("\nНажмите Enter, чтобы вернуться в меню...")
    clear_screen()

def calories_day():
    date_calories = input("Введите дату дня для вывода продуктов и колорий в формате: YYYY-MM-DD:\n").strip()
    try:
        datetime.datetime.strptime(date_calories, "%Y-%m-%d")
    except ValueError:
        print("Неверный формат даты! Используйте YYYY-MM-DD.")
        input("\nНажмите Enter, чтобы вернуться в меню...")
        return
    clear_screen()

    for name, info in products.items():
        if isinstance(info, dict) and info.get("date") == date_calories:
            print(f"{name}, калории: {info['value']}")
    else:
        print(f"Ничего не найдено за эту дату")
    input("\nНажмите Enter, чтобы вернуться в меню...")
    clear_screen()

def delete_day():
    del_day = input("Введите дату дня для удаления: ").strip().casefold()
    try:
        datetime.datetime.strptime(del_day, "%Y-%m-%d")
    except ValueError:
        print("Неверный формат даты! Используйте YYYY-MM-DD.")
        input("\nНажмите Enter, чтобы вернуться в меню...")
        return

    to_delete = []

    for name, info in products.items():
        if isinstance(info, dict) and info.get("date") == del_day:
            to_delete.append(name)
    if not to_delete:
        print(f"Ничего не найдено за эту дату")
    else:
        for name in to_delete:
            del products[name]
        save_data()
        print(f"Удалено продуктов за {del_day}: {len(to_delete)}")

    input("\nНажмите Enter, чтобы вернуться в меню...")
    clear_screen()

def save_report_day():
    days = {}
    for name, info in products.items():
        if isinstance(info, dict) and "date" in info:
            date = info["date"]
            if date not in days:
                days[date] = []
            days[date].append((name, info["value"]))

    with open("report.txt", "w", encoding="utf-8") as f:
        for date in sorted(days.keys()):
            f.write(f"Дата: {date}\n")
            for name, value in days[date]:
                f.write(f"  {name}: {value} калорий\n")
            f.write("\n")
    print("Отчёт сохранён в report.txt")
    input("\nНажмите Enter, чтобы вернуться в меню...")
    clear_screen()

def save_data():    
    with open("calories.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
    print("Данные обновленны!")
    input("\nНажмите Enter, чтобы вернуться в меню...")
    clear_screen()

def reading_csv():
    with open('products_calories.csv', newline='', encoding='utf-8') as f:14
    reader = csv.reader(f)
    for row in reader:
            if len(row) >= 2:
                name, calories = row[0].strip().casefold(), int(row[1])
                products[name] = {"value": calories, "date": datetime.date.today().isoformat()}
    save_data()
    print("CSV импортирован")

        

while True: 
    print("\nМеню:")
    print("1. Добавить продукт")
    print("2. Показать все продукты")
    print("3. Подсчитать общую стоимость калории")
    print("4. Сохранить данные")
    print("5. Удалить продукт")
    print("6. Поиск продукта")
    print("7. Очистка всех продуктов")
    print("8. Редактирование продукта")
    print("9. Сортировка продуктов")
    print("10. Мини-отчёт")
    print("11. Подсчёт калорий за определённую дату")
    print("12. Удаления всех продуктов по дате")
    print("13. Сохранить отчёт за выбранную дату")
    print("14. Импорт из CSV файла")
    print("99. Выйти")

    choise = input("Выберите действие (1-14): \n")

    if choise == '1':
        add_product()
    elif choise == '2':
        show_products()
    elif choise == '3':
        calculate_calories()
    elif choise == '4':
        save_data()
    elif choise == '5':
        delete_product()
    elif choise == '6':
        search_products()
    elif choise == '7':
        clean_all()
    elif choise == '8':
        edit_product()
    elif choise == '9':
        sort_products()
    elif choise == '10':
        mini_report()
    elif choise == '11':
        calories_day()
    elif choise == '12':
        delete_day()
    elif choise == '13':
        save_report_day()
    elif choise == '14':
        reading_csv()
    elif choise == '99':
        print("До свидания!")
        break
