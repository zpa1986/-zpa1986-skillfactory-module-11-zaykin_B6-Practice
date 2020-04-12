import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    """
    создаем модель таблицы album для последующего хранения записей
    """
    __tablename__ = "album"  # даем название таблице

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    """
    Устанавливает соединение c БД, создает таблицы, если их еще нет
    и на выходе получаем конкретную сессию
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(artist):
    """
    пишем функцию поиска записей по конкретному артисту
    на вход функция принимает строковое наименование артиста,
    а на выходе выдает данные по его альбомам
    """
    session = connect_db() #создаем сессию подключения в базе данных
    """
    в переменную albums записываем отфильтрованную по нужному артисту 
    базу данных, моделью которой служит класс Album
    """
    albums = session.query(Album).filter(Album.artist == artist).all()
    # выводим таблицу записей по нужному артисту
    return albums

def save(year, artist, genre, album):
    """ поднимем ряд исключений, чтобы осуществить корректный
    ввод данных с учетом условий задачи:
    - год должен представлять собой целое число
    - все остальные значение должны быть строковыми
    """
    assert isinstance(year, int), "Проверьте формат даты! Должно быть целое число..."
    assert isinstance(artist, str), "Проверьте формат записи артиста! Нужно вводить только строковое значение..."
    assert isinstance(genre, str), "Проверьте формат записи жанра! Нужно вводить только строковое значение..."
    assert isinstance(album, str), "Проверьте формат записи названия альбома! Нужно вводить только строковое значение..."

    # создаем сессию подключения к БД
    session = connect_db()
    """
    сортируем данные БД по нужному альбому и артисту и записываем это всё
    в переменную saved_album с тем, чтобы потом проверить альбом который мы хотим
    записать на повтор в БД. Поиск осуществляем до первого попавшегося нам значения
    """
    is_new_album = session.query(Album).filter(Album.album == album, Album.artist == artist).first()
    # если в переменную is_new_album что-то записалось, значит сигнализируем об этом
    if is_new_album is not None:
        raise AlreadyExists("Такой альбом уже есть в базе. Его id #{}".format(is_new_album.id))
    #переменной album присваиваем атрибуты класса Album
    album = Album(
        year=year,
        artist=artist,
        genre=genre,
        album=album
    )
    # добавляем в сессию соответствующую запись
    session.add(album)
    # подгружаем в БД эту запись
    session.commit()
    return album