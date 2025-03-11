import numpy as np
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from entities import Base, OBTT
from sqlalchemy import text

# Настройка подключения к базе данных
DATABASE_URI = r'sqlite:///bd/bd.db'  # Замените на ваш URI базы данных
#engine = create_engine(DATABASE_URI)
##Session = sessionmaker(bind=engine)
#session = Session()

# Создание нового объекта
def create_obtt(engin, name, width, length, height, dir):
    Session = sessionmaker(bind=engine)
    session = Session() 
    new_obtt = OBTT(name=name, width=width, length=length, height=height, dir=dir)
    session.add(new_obtt)
    session.commit()
    session.close()
    return new_obtt


# Чтение всех значений
def read_all_obtt(engine, to_array=False):
    Session = sessionmaker(bind=engine)
    session = Session()
    obtts = session.query(OBTT).all()
    session.close()
    if to_array:
        return np.array([[obtt.id, obtt.name, obtt.width, obtt.length, obtt.height, obtt.dir] for obtt in obtts])
    return obtts


# Фильтр значений по колонке
def filter_obtt_by_column(engine, column_name, value, to_array=False):
    Session = sessionmaker(bind=engine)
    session = Session() 
    column = getattr(OBTT, column_name)
    obtts = session.query(OBTT).filter(column == value).all()
    session.commit()
    session.close()
    if to_array:
        return np.array([[obtt.id, obtt.name, obtt.width, obtt.length, obtt.height, obtt.dir] for obtt in obtts])
    return obtts

# Вывод только тех объектов, значений в колонке которой больше или равно значению указанному пользователем
def filter_obtt_greater_equal(engine, column_name, value, to_array=False):
    Session = sessionmaker(bind=engine)
    session = Session()
    column = getattr(OBTT, column_name)
     
    obtts = session.query(OBTT).filter(column >= value).all()
    session.commit()
    session.close()
    if to_array:
        return np.array([[obtt.id, obtt.name, obtt.width, obtt.length, obtt.height, obtt.dir] for obtt in obtts])
    return obtts

# Чтение объекта по его колонке
def read_obtt_by_column(engine, column_name, value, to_array=False):
    Session = sessionmaker(bind=engine)
    session = Session() 
    column = getattr(OBTT, column_name)
    obtt = session.query(OBTT).filter(column == value).first()
    session.close()
    if to_array and obtt:
        return np.array([[obtt.id, obtt.name, obtt.width, obtt.length, obtt.height, obtt.dir]])
    return obtt


def add_column_to_obtt(engine, column_name, column_type):
    """
    Добавляет новую колонку в таблицу OBTT.
    :param column_name: Имя новой колонки.
    :param column_type: Тип данных новой колонки (например, String, Integer, Float и т.д.).
    """
    # Формируем SQL-запрос для добавления колонки
    sql = text(f'ALTER TABLE OBTT ADD COLUMN {column_name} {column_type}')
    
    # Выполняем запрос
    with engine.connect() as connection:
        connection.execute(sql)
        connection.commit()
        connection.close()
    
    print(f"Колонка '{column_name}' типа '{column_type}' успешно добавлена в таблицу OBTT.")

def update_column_by_id(engine, obj_id, column_name, new_value):
    """
    Обновляет значение в указанной колонке для объекта с заданным id.
    :param obj_id: ID объекта, который нужно обновить.
    :param column_name: Имя колонки, которую нужно обновить.
    :param new_value: Новое значение для колонки.
    """
    # Получаем объект по id
    Session = sessionmaker(bind=engine)
    session = Session() 
    obtt = session.query(OBTT).filter(OBTT.id == obj_id).first()
    session.commit()
    session.close()
        
    if obtt:
            # Обновляем значение в указанной колонке
        setattr(obtt, column_name, new_value)
        session.commit()
        print(f"Значение в колонке '{column_name}' для объекта с ID={obj_id} успешно обновлено на '{new_value}'.")
    else:
        print(f"Объект с ID={obj_id} не найден.")




if __name__ == "__main__":
    # 1. Создание нового объекта
    DATABASE_URI = r'sqlite:///bd/bd.db'  # Замените на ваш URI базы данных
    engine = create_engine(DATABASE_URI)
    print("Создание нового объекта OBTT5:")
    new_obtt = create_obtt(engine, name="OBTT20", width=62.0, length=55.0, height=6.5, dir="North")
    print(f"Создан объект: ID={new_obtt.id}, Name={new_obtt.name}, Width={new_obtt.width}, Length={new_obtt.length}, Height={new_obtt.height}, Dir={new_obtt.dir}")
    print()

    # 2. Чтение всех значений
    print("Чтение всех объектов:")
    obtts = read_all_obtt(engine)
    for obtt in obtts:
        print(f"ID={obtt.id}, Name={obtt.name}, Width={obtt.width}, Length={obtt.length}, Height={obtt.height}, Dir={obtt.dir}")
    print()

    # 3. Фильтр значений по колонке
    print("Фильтр объектов по колонке 'dir' со значением 'North':")
    filtered_obtts = filter_obtt_by_column(engine, column_name="dir", value="North", to_array=True)
    print(filtered_obtts)
    print()

    # 4. Вывод объектов, у которых значение в колонке больше или равно указанному
    print("Фильтр объектов по колонке 'width' со значением >= 15.0:")
    filtered_obtts = filter_obtt_greater_equal(engine, column_name="width", value=15.0, to_array=True)
    print(filtered_obtts)
    print()

    # 5. Чтение объекта по его колонке
    print("Поиск объекта по колонке 'name' со значением 'OBTT3':")
    obtt = read_obtt_by_column(engine, column_name="name", value="OBTT3", to_array=True)
    print(obtt)

    # Добавляем новую колонку 'weight' типа Float
    #add_column_to_obtt(column_name="weight777", column_type="FLOAT")

    # Проверяем, что колонка добавлена
    #obtts = read_all_obtt(to_array=True)
    #print(obtts)


    new_obtt = create_obtt(engine, name="Новый об1", width=12.0, length=24.0, height=6.5, dir="cvat")
    print(f"Создан объект: ID={new_obtt.id}, Name={new_obtt.name}, Width={new_obtt.width}, Length={new_obtt.length}, Height={new_obtt.height}, Dir={new_obtt.dir}")
    print()

    update_column_by_id(engine, 5, column_name="weight777", new_value=999.0)

    #obtt = session.query(OBTT).filter(OBTT.id == 5).first()
    #print(obtt.weight777)
    #session.commit()