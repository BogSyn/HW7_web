# Домашнє завдання #7

<h1>Основна частина:</h1>

<b>Запуск контейнера:</b> 

    docker run --name hw7-postgres -p 5432:5432 -e POSTGRES_PASSWORD=qwerty -d postgres

<b>Налаштування зв'язку з базою даних:</b>

    файл конфігурації ->    config.ini
               cкрипт ->    conf/conn.py
    

<b>Моделі SQLAlchemy, для таблиць:</b>

    conf/models.py

<b>Alembic в папці:</b>

    migrations

<b>Заповнення бази:</b>

    seeds/seed.py

<b>Всі 12 виборок з бази:</b>

    my_select.py


<h1>Додаткове завдання:</h1>

CLI програма для CRUD операцій (Create, Read, Update, Delete) із базою даних:

        main.py

<b>Створення об'єктів:</b>

        python crud.py -a create -m Teacher -n "Ім'я вчителя"           - створює нового вчителя
        python crud.py -a create -m Group -n "Назва групи"              - створює нову групу
        python crud.py -a create -m Student -n "Ім'я студента" -gp 1    - створює нового студента в групі з ID 1
        python crud.py -a create -m Subject -n "Назва предмету" -th 1   - створює новий предмет, який викладає вчитель з ID 1
        python crud.py -a create -m Grade -gd 5 -sj 1 -st 1             - створює нову оцінку 5 для студента з ID 1 за предмет з ID 1

<b>Перегляд списку об'єктів:</b>

        python crud.py -a list -m Teacher       - виводить список всіх вчителів
        python crud.py -a list -m Group         - виводить список всіх груп
        python crud.py -a list -m Student       - виводить список всіх studentів
        python crud.py -a list -m Subject       - виводить список всіх предметів
        python crud.py -a list -m Grade         - виводить список всіх оцінок

<b>Оновлення об'єктів:</b>

        python crud.py -a update -m Teacher -id 1 -n "Нове ім'я вчителя"            - оновлює ім'я вчителя з ID 1
        python crud.py -a update -m Group -id 1 -n "Нова назва групи"               - оновлює назву групи з ID 1
        python crud.py -a update -m Student -id 1 -n "Нове ім'я студента" -gp 2     - оновлює ім'я та групу студента з ID 1
        python crud.py -a update -m Subject -id 1 -n "Нова назва предмету" -th 2    - оновлює назву предмету з ID 1 та ID викладача
        python crud.py -a update -m Grade -id 1 -gd 4                               - оновлює оцінку з ID 1

<b>Видалення об'єктів:</b>

        python crud.py -a remove -m Teacher -id 1   - видаляє вчителя з ID 1
        python crud.py -a remove -m Group -id 1     - видаляє групу з ID 1
        python crud.py -a remove -m Student -id 1   - видаляє студента з ID 1
        python crud.py -a remove -m Subject -id 1   - видаляє предмет з ID 1
        python crud.py -a remove -m Grade -id 1     - видаляє оцінку з ID 1
