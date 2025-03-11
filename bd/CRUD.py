import sys, os
sys.path.append(os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from sqlalchemy import create_engine, Float, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import StatementError
from bd.entities import *
from sqlalchemy import text


# Подключение к базе данных (замените 'sqlite:///your_database.db' на ваш путь к базе данных)
engine = create_engine(r"sqlite:///bd\bd.db")
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

def create_obtt(**kargs):
    """
    Создание новой записи в таблице OBTT.
    """
    new_obtt = OBTT(**kargs)
    session.add(new_obtt)
    session.commit()
    return new_obtt

def read_obtt(obtt_id):
    """
    Чтение записи из таблицы OBTT по id.
    """
    return session.query(OBTT).filter(OBTT.id == obtt_id).first()

def update_obtt(obtt_id, column_name, new_value):
    """
    Обновление значения в указанном столбце для записи с указанным id.
    """
    obtt = session.query(OBTT).filter(OBTT.id == obtt_id).first()
    if obtt:
        setattr(obtt, column_name, new_value)
        session.commit()
        return obtt
    return None

def delete_obtt(obtt_id):
    """
    Удаление записи из таблицы OBTT по id.
    """
    obtt = session.query(OBTT).filter(OBTT.id == obtt_id).first()
    if obtt:
        session.delete(obtt)
        session.commit()
        return True
    return False

def search_obtt_by_value(column_name, value):
    """
    Поиск записей в таблице OBTT, где значение в указанном столбце больше или равно указанному значению.
    Результаты сортируются по указанному столбцу.
    """
    return session.query(OBTT).filter(getattr(OBTT, column_name) >= value).order_by(getattr(OBTT, column_name)).all()

def add_column_to_obtt(column_name, column_type):
    """
    Добавление нового столбца в таблицу OBTT.
    """
    from sqlalchemy import text
    sql = text(f'ALTER TABLE OBTT ADD COLUMN {column_name} {column_type.__class__.__name__}')
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(sql)
            connection.commit()
    print(f"Колонка '{column_name}' успешно добавлена в таблицу OBTT.")

def rewrite_value(obtt_id, column_name, new_value):
    """
    Перезапись значения в указанном столбце для записи с указанным id.
    """
    obtt = session.query(OBTT).filter(OBTT.id == obtt_id).first()
    if obtt:
        setattr(obtt, column_name, new_value)
        session.commit()
        return obtt
    return None





if __name__ == "__main__":
    # Пример создания новой записи
    try:
        new_obtt = create_obtt(**{"name":"Object4321", "width":10.5, "length":"20.31", "height":5.0, "dir":"north"})
        print(f"Создана новая запись: ID={new_obtt.id}, Name={new_obtt.name}")
    except StatementError:
        print("УПС!")

    # Пример чтения записи по ID
    obtt = read_obtt(new_obtt.id)
    if obtt:
        print(f"Прочитана запись: ID={obtt.id}, Name={obtt.name}, Width={obtt.width}, Length={obtt.length}, Height={obtt.height}, Dir={obtt.dir}")
    else:
        print("Запись не найдена.")

    # Пример поиска записей с шириной >= 10.0
    results = search_obtt_by_value(column_name="length", value=20.0)
    print("Результаты поиска (ширина >= 10.0):")
    for result in results:
        print(f"ID={result.id}, Name={result.name}, Width={result.width}")

    # Пример обновления записи
    updated_obtt = update_obtt(obtt_id=new_obtt.id, column_name="width", new_value=15.0)
    if updated_obtt:
        print(f"Запись обновлена: ID={updated_obtt.id}, Новое значение width={updated_obtt.width}")
    else:
        print("Запись для обновления не найдена.")

    # Пример перезаписи значения в объекте
    rewritten_obtt = rewrite_value(obtt_id=new_obtt.id, column_name="dir", new_value="123123")
    if rewritten_obtt:
        print(f"Значение перезаписано: ID={rewritten_obtt.id}, Новое значение={rewritten_obtt.dir}")
        
    else:
        print("Запись для перезаписи не найдена.")

    # Пример удаления записи
    #if delete_obtt(new_obtt.id):
        #print(f"Запись с ID={new_obtt.id} удалена.")
    #else:
        #print("Запись для удаления не найдена.")