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
               '/voice', '/photo', '/group', '/note', '/file,', '/video', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(content_types=ContentType.PHOTO)
async def process_PHOTO(message: types.Message):
    if message.caption is None:
        name_file =  message.photo[-1].file_unique_id
    else:
        name_file =  message.caption

    id_file = message.photo[-1].file_id
    file_type = 'photo'
    upload_my_files.uploadMediaFiles(id_file, name_file, file_type)

@dp.message_handler(content_types=ContentType.DOCUMENT)
async def process_DOCUMENT(message: types.Message):
    if message.caption is None:
        name_file =  message.document.file_unique_id
    else:
        name_file =  message.caption

    id_file = message.document.file_id
    file_type = 'file'
    upload_my_files.uploadMediaFiles(id_file, name_file, file_type)

@dp.message_handler(content_types=ContentType.VOICE)
async def process_VOICE(message: types.Message):
    name_file =  message.voice.file_unique_id
    id_file = message.voice.file_id
    file_type = 'voice'
    upload_my_files.uploadMediaFiles(id_file, name_file, file_type)

@dp.message_handler(content_types=ContentType.VIDEO)
async def process_VIDEO(message: types.Message):
    if message.caption is None:
        name_file =  message.video.file_unique_id
    else:
        name_file =  message.caption

    id_file = message.video.file_id
    file_type = 'video'
    upload_my_files.uploadMediaFiles(id_file, name_file, file_type)

@dp.message_handler(content_types=ContentType.VIDEO_NOTE)
async def process_VIDEO_NOTE(message: types.Message):
    name_file =  message.video_note.file_unique_id
    id_file = message.video_note.file_id
    file_type = 'video_note'
    upload_my_files.uploadMediaFiles(id_file, name_file, file_type)

@dp.message_handler(commands=['photo'])
async def process_photo_command(message: types.Message):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute("SELECT * FROM MediaIds")
    MediaIds = cur.fetchall()

    media = []

    for photo_id in MediaIds:
        if photo_id[3] == 'photo':
            media.append(InputMediaPhoto(photo_id[1]))
    
    await bot.send_media_group(message.from_user.id, media)

    cur.close()
    conn.close()


@dp.message_handler(commands=['voice'])
async def process_photo_command(message: types.Message):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute("SELECT * FROM MediaIds")
    MediaIds = cur.fetchall()

    for voice_id in MediaIds:
        if voice_id[3] == 'voice':
            await bot.send_voice(message.from_user.id, voice_id[1])

    cur.close()
    conn.close()

@dp.message_handler(commands=['note'])
async def process_photo_command(message: types.Message):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute("SELECT * FROM MediaIds")
    MediaIds = cur.fetchall()

    for video_note_id in MediaIds:
        if video_note_id[3] == 'video_note':
            await bot.send_voice(message.from_user.id, video_note_id[1])

    cur.close()
    conn.close()

@dp.message_handler(commands=['file'])
async def process_photo_command(message: types.Message):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute("SELECT * FROM MediaIds")
    MediaIds = cur.fetchall()

    for file_id in MediaIds:
        if file_id[3] == 'file':
            await bot.send_voice(message.from_user.id, file_id[1])

    cur.close()
    conn.close()

@dp.message_handler(commands=['group'])
async def process_photo_command(message: types.Message):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute("SELECT * FROM MediaIds")
    MediaIds = cur.fetchall()

    for group_id in MediaIds:
        if group_id[3] == 'file':
            await bot.send_voice(message.from_user.id, group_id[1])

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