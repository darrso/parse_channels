from sqlalchemy.orm.session import sessionmaker
from bot.database.classes.cDB import engine, Users

# СОЗДАНИЕ СЕССИИ
session = sessionmaker(bind=engine)()


async def create_new_user(userid, username, onoff):
    try:
        session.add(Users(user_id=userid, user_name=username, on_off=onoff, parse_channels=None))
        session.commit()
        return True
    except:
        return False


async def check_on_off(userid):
    try:
        data = session.query(Users).filter_by(user_id=userid)
        bData = data.first()
        return bData.on_off
    except:
        return "You didn't send /start!"


async def switch_on_off(parametr, userid):
    try:
        q = session.query(Users).filter_by(user_id=userid)
        res = q.first()
        res.on_off = parametr
        session.commit()
        return True
    except:
        return False


async def check_parse_channels(userid):
    try:
        q = session.query(Users).filter_by(user_id=userid)
        res = q.first()
        return res.parse_channels
    except:
        return False
