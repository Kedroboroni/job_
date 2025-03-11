from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Создаем базовый класс для всех моделей
Base = declarative_base()

class OBTT(Base):
    # Определяем имя таблицы
    __tablename__ = 'OBTT'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    width = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    dir = Column(String, nullable=False)





if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(r"sqlite:///bd/bd.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    item = OBTT(name="Пример1", width=10, length=20, height=503, dir="вверх")
    session.add(item)
    session.commit()
    session.close()