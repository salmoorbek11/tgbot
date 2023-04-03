import os
import logging
from aiogram import Bot
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from db_map import Base, MediaIds
from config import TOKEN, MY_ID, DB_FILENAME

logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

engine = create_engine(f'sqlite:///{DB_FILENAME}')

if not os.path.isfile(f'./{DB_FILENAME}'):
    Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

bot = Bot(token=TOKEN)


def uploadMediaFiles(file_id, file_name, file_type):
            session = Session()
            newItem = MediaIds(file_id=file_id, file_name=file_name, file_type=file_type)
            try:
                session.add(newItem)
                session.commit()
            except Exception as e:
                logging.error(
                    'Couldn\'t upload {}. Error is {}'.format(file_name, e))
            else:
                logging.info(
                    f'Successfully uploaded and saved to DB file {file_name} with id {file_id}')
            finally:
                session.close()

Session.remove()