import sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.types.message import ContentType
import upload_my_files


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет!\nИспользуй /help, '
                        'чтобы узнать список доступных команд!')


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text(bold('Я могу ответить на следующие команды:'),
               '/voice', '/photo', '/note', '/file,', '/video', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(content_types=ContentType.PHOTO)
async def process_PHOTO(message: types.Message):
    if message.caption is None:
        name_file =  message.photo[-1].file_unique_id
    else:
        name_file =  message.caption

    id_file = message.photo[-1].file_id
    file_type = 'photo'
    id_user = message.from_user.id
    upload_my_files.uploadMediaFiles(id_file, name_file, file_type, id_user)

@dp.message_handler(content_types=ContentType.DOCUMENT)
async def process_DOCUMENT(message: types.Message):
    if message.caption is None:
        name_file =  message.document.file_unique_id
    else:
        name_file =  message.caption

    id_file = message.document.file_id
    file_type = 'file'
    id_user = message.from_user.id
    upload_my_files.uploadMediaFiles(id_file, name_file, file_type, id_user)

@dp.message_handler(content_types=ContentType.VOICE)
async def process_VOICE(message: types.Message):
    name_file =  message.voice.file_unique_id
    id_file = message.voice.file_id
    file_type = 'voice'
    id_user = message.from_user.id
    upload_my_files.uploadMediaFiles(id_file, name_file, file_type, id_user)

@dp.message_handler(content_types=ContentType.VIDEO)
async def process_VIDEO(message: types.Message):
    if message.caption is None:
        name_file =  message.video.file_unique_id
    else:
        name_file =  message.caption

    id_file = message.video.file_id
    file_type = 'video'
    id_user = message.from_user.id
    upload_my_files.uploadMediaFiles(id_file, name_file, file_type, id_user)

@dp.message_handler(content_types=ContentType.VIDEO_NOTE)
async def process_VIDEO_NOTE(message: types.Message):
    name_file =  message.video_note.file_unique_id
    id_file = message.video_note.file_id
    file_type = 'video_note'
    id_user = message.from_user.id
    upload_my_files.uploadMediaFiles(id_file, name_file, file_type, id_user)

@dp.message_handler(commands=['photo'])
async def process_photo_command(message: types.Message):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute(f"SELECT file_id FROM MediaIds where id_user = '{message.from_user.id}' AND file_type = 'photo'")
    MediaIds = cur.fetchall()

    media = []

    for photo_id in MediaIds:
        media.append(InputMediaPhoto(photo_id[0]))
    
    await bot.send_media_group(message.from_user.id, media)

    cur.close()
    conn.close()


@dp.message_handler(commands=['voice'])
async def process_photo_command(message: types.Message):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute(f"SELECT file_id FROM MediaIds where id_user = '{message.from_user.id}' AND file_type = 'voice'")
    MediaIds = cur.fetchall()

    for voice_id in MediaIds:
        await bot.send_voice(message.from_user.id, voice_id[0])

    cur.close()
    conn.close()

@dp.message_handler(commands=['note'])
async def process_photo_command(message: types.Message):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute(f"SELECT file_id FROM MediaIds where id_user = '{message.from_user.id}' AND file_type = 'video_note'")
    MediaIds = cur.fetchall()

    for video_note_id in MediaIds:
        await bot.send_voice(message.from_user.id, video_note_id[0])

    cur.close()
    conn.close()

@dp.message_handler(commands=['file'])
async def process_photo_command(message: types.Message):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute(f"SELECT file_id FROM MediaIds where id_user = '{message.from_user.id}' AND file_type = 'file'")
    MediaIds = cur.fetchall()

    for file_id in MediaIds:
        await bot.send_voice(message.from_user.id, file_id[0])

    cur.close()
    conn.close()

@dp.message_handler(commands=['video'])
async def process_photo_command(message: types.Message):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute(f"SELECT file_id FROM MediaIds where id_user = '{message.from_user.id}' AND file_type = 'video'")
    MediaIds = cur.fetchall()

    for video_id in MediaIds:
        await bot.send_voice(message.from_user.id, video_id[0])

    cur.close()
    conn.close()

@dp.message_handler(commands=['delete'])
async def process_photo_command(message: types.Message):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute('DELETE FROM MediaIds',)
    await message.reply(message.from_user.id, "Удалено записей:", cur.rowcount)
    conn.commit()

    cur.close()
    conn.close()



if __name__ == '__main__':
    executor.start_polling(dp)