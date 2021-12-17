import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from vk_function import get_photo, sort_photo

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
class UserProfiles(Base):
    __tablename__ = 'user_profiles'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    vk_id = sa.Column(sa.Integer, unique=True)
    first_name = sa.Column(sa.String)
    second_name = sa.Column(sa.String)
    city = sa.Column(sa.String)
    link = sa.Column(sa.String)
    id_user = sa.Column(sa.Integer, sa.ForeignKey('user.id', ondelete='CASCADE'))


# фото
class Photos(Base):
    __tablename__ = 'photos'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    link_foto = sa.Column(sa.String)
    count_likes = sa.Column(sa.Integer)
    id_user_profiles = sa.Column(sa.Integer, sa.ForeignKey('user_profiles.id', ondelete='CASCADE'))


# черный список
class BlackList(Base):
    __tablename__ = 'black list'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    vk_id = sa.Column(sa.Integer, unique=True)
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


# добавить анкеты в БД
def add_user_profile(list_):
    if chek_user_profile(list_[0]) is None:
        new_profile = UserProfiles(vk_id=list_[0], first_name=list_[1], second_name=list_[2], link=list_[3])
        session.add(new_profile)
        session.commit()
        return True
    else:
        return False


# Проверяет есть ли анкета в избранном
def chek_user_profile(id_):
    current_user_id = session.query(UserProfiles).filter_by(vk_id=id_).first()
    return (current_user_id)


# Добавляет фото в БД
def add_photo(id_):
    list_ = sort_photo(get_photo(id_))
    for i in list_:
        new_photo = Photos(count_likes=i[0], link_foto=i[1])
        session.add(new_photo)
        session.commit()
    return True


# добавить в ЧС
def add_user_black_list(list_):
    if chek_user_black_list(list_[0]) is None:
        new_profile = BlackList(vk_id=list_[0], first_name=list_[1], second_name=list_[2])
        session.add(new_profile)
        session.commit()
        return True
    else:
        return False


# проверяет есть-ли анкета в ЧС
def chek_user_black_list(id_):
    current_user_id = session.query(BlackList).filter_by(vk_id=id_).first()
    return (current_user_id)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # print(chek_user_black_list(552707168))
    # print(chek_user(552707168))
