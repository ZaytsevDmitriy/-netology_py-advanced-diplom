import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError

# Подключение к БД
Base = declarative_base()
engine = sa.create_engine('postgresql://vkinder:netology@localhost:5432/vkinder',
                          client_encoding='utf8')
Session = sessionmaker(bind=engine)
session = Session()
connection = engine.connect()


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    vk_id = sa.Column(sa.Integer, unique=True)


# анкеты пользователей
class User_profiles(Base):
    __tablename__ = 'user_profiles'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    vk_id = sa.Column(sa.String, unique=True)
    first_name = sa.Column(sa.String)
    second_name = sa.Column(sa.String)
    city = sa.Column(sa.String)
    link = sa.Column(sa.String)
    id_user = sa.Column(sa.Integer, sa.ForeignKey('user.id', ondelete='CASCADE'))


# фото
class PHotos(Base):
    __tablename__ = 'photos'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    link_foto = sa.Column(sa.String)
    count_likes = sa.Column(sa.Integer)
    id_user_profiles = sa.Column(sa.Integer, sa.ForeignKey('user_profiles.id', ondelete='CASCADE'))


# черный список
class Black_list(Base):
    __tablename__ = 'black_list'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    vk_id = sa.Column(sa.String, unique=True)
    first_name = sa.Column(sa.String)
    second_name = sa.Column(sa.String)
    city = sa.Column(sa.String)
    link = sa.Column(sa.String)
    link_photo = sa.Column(sa.String)
    id_user = sa.Column(sa.Integer, sa.ForeignKey('user.id', ondelete='CASCADE'))

# регистрация пользователя
def reg_user(vk_id):
    try:
        new_user = User(vk_id=vk_id)
        session.add(new_user)
        session.commit()
        return True
    except(IntegrityError, InvalidRequestError):
        return False

# проверить есть-ли пользователь в БД
def chek_user(id_):
    current_user_id = session.query(User).filter_by(vk_id=id_).first()
    return (current_user_id)



if __name__ == '__main__':
    Base.metadata.create_all(engine)

    print(chek_user(1))
