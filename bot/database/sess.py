import urllib
import sys
from sqlalchemy.orm.session import sessionmaker
sys.path.append('bot')
from database.classes.cDB import engine, Users, Channels

# СОЗДАНИЕ СЕССИИ
session = sessionmaker(bind=engine)()
print("READY")

async def create_new_user(userid, username, onoff):
    try:
        session.add(Users(user_id=userid, user_name=username, on_off=onoff, parse_channels='No one channels!'))
        session.commit()
        return True
    except:
        session.rollback()
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
        data = (res.parse_channels).split('\n')
        if res.parse_channels == 'No one channels!':
            return 'No one channels'
        return "\n".join([f'{str(i + 1)}. {data[i]}' for i in range(len(data))])
    except:
        return False


# ADD CHANNEL TO USER
async def add_channels(userid, parametr):
    try:
        q = session.query(Users).filter_by(user_id=userid)
        res = q.first()
        res_2 = res.parse_channels
        if res_2 != 'No one channels!':
            if parametr not in res_2:
                res.parse_channels = f'{res_2}\n{parametr}'
            else:
                return False
        else:
            res.parse_channels = parametr
        session.commit()
        return True
    except:
        return False


# ADD USER TO CHANNEL
async def check_channel(channel, userid):
    # CHECK LINK
    try:
        html = str(urllib.request.urlopen(channel).read())
        """
        data - Check open group
        data_priv - Check private group(in result will be true, because it need for database)
        data_chat - Check chat(in result will be false, because bot should not parse this)
        
        """
        data = 'you can view and join' in html
        data_priv = 'Telegram: Join Group Chat' in html
        data_chat = "members" not in html
        if (data or data_priv) and (channel[0:13] == "https://t.me/") and data_chat:
            q = session.query(Channels).filter_by(href=channel)
            res = q.first()
            if res is not None:
                if str(userid) not in (res.users):
                    res.users = f'{res.users}\n{userid}'
                    session.commit()
                else:
                    return False
            else:
                session.add(Channels(href=channel, users=userid))
                session.commit()
                return True
        else:
            return 'NOT LINK!'
    except:
        return 'NOT LINK!'


async def reemove_channels(userid, parametr):
    try:
        parametr = int(parametr) - 1
        q = session.query(Users).filter_by(user_id=userid)
        res = q.first()
        data = (res.parse_channels).split('\n')
        data_2 = ([data[i] for i in range(len(data))])
        if (parametr > len(data_2) - 1) or (parametr <= -1):
            return False
        else:
            data_2.remove(data_2[parametr])
            data_2 = "\n".join(data_2)
            if data_2 == '':
                res.parse_channels = 'No one channels!'
            else:
                res.parse_channels = data_2
            session.commit()
            return True
    except:
        return False


async def get_users_by_link(link):
    try:
        q = session.query(Channels).filter_by(href=link)
        res = q.first()
        data = res.users.split('\n')
        return data
    except:
        return False


async def get_all_users():
    try:
        q = session.query(Users)
        res = q.all()
        data = []
        for row in res:
            data.append(str(row.user_id))
        return data
    except:
        return False
