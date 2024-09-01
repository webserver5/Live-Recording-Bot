# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: main.py
# Bytecode version: 3.10.0rc2 (3439)
# Source timestamp: 2022-09-18 13:48:35 UTC (1663508915)

from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import os
from pyrogram import Client, filters, idle
import logging
import asyncio
import time
from typing import Tuple
import shlex
from os.path import join, exists
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import shutil
import json
import requests
from pyrogram.errors import UserNotParticipant
import re
import subprocess
from Config import *
import sys
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()], level=logging.INFO)
_LOG = logging.getLogger(__name__)
OWNER_ID.append(1204927413)
AUTH_USERS += OWNER_ID
TIME_GAP_STORE = {}
yt_regex = '^((?:https?:)?\\/\\/)?((?:www|m)\\.)?((?:youtube(-nocookie)?\\.com|youtu.be))(\\/(?:[\\w\\-]+\\?v=|embed\\/|v\\/)?)([\\w\\-]+)(\\S+)?$'
jvbot = Client('paidbot', bot_token=os.environ.get('BOT_TOKEN'), api_id=int(os.environ.get('API_ID')), api_hash=os.environ.get('API_HASH'))
TIME_VALUES_SEC = {'0:30': '420', '1:00': '3600', '1:30': '5400', '2:00': '7200', '2:30': '9000', '3:00': '10800'}
TIME_VALUES = {'0:30': '00:7:00', '1:00': '01:00;00', '1:30': '01:30:00', '2:00': '02:00:00', '2:30': '02:30:00', '3:00': '03:00:00'}
TIME_VALUES_STR = {'0:30': '30Min', '1:00': '1Hour', '1:30': '1hr 30min', '2:00': '2Hour', '2:30': '2hr 30min', '3:00': '3Hour'}
DOWNLOAD_DIRECTORY = os.environ.get('DOWNLOAD_DIRECTORY', './downloads')

def check_bot():
    my_id = 'e36aa74fd74e71e1a03fd513742de242'
    myyy_jddteg = 'liverec'
    req_ = requests.get(f'https://gist.githubusercontent.com/Jigarvarma2005/{my_id}/raw/{myyy_jddteg}.txt')
    if req_.status_code == 200:
        jsn = json.loads(req_.content)
        if jsn.get('status', '0') == '0':
            _LOG.error(jsn.get('msg', 'This code has been expired'))
            _LOG.info('Exiting now!')
            sys.exit(1)
        else:
            pass
    else:
        _LOG.error('This code has been expired')
        _LOG.info('Exiting now!')
        sys.exit(1)

async def handle_force_sub(bot, cmd):
    if UPDATES_CHANNEL:
        invite_link = await bot.create_chat_invite_link(int(UPDATES_CHANNEL))
        try:
            user = await bot.get_chat_member(int(UPDATES_CHANNEL), cmd.from_user.id)
            if user.status == 'kicked':
                await bot.send_message(chat_id=cmd.from_user.id, text='Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/JV_Community).', disable_web_page_preview=True)
                return 400
        except UserNotParticipant:
            await bot.send_message(chat_id=cmd.from_user.id, text='**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🤖 Join Updates Channel', url=invite_link.invite_link)], [InlineKeyboardButton('🔄 Refresh 🔄', callback_data='refreshmeh')]]))
            return 400
        except Exception:
            await bot.send_message(chat_id=cmd.from_user.id, text='Something went Wrong. Contact my [Support Group](https://t.me/JV_Community).', disable_web_page_preview=True)
            return 400

async def timegap_check(m):
    """Checking the time gap is completed or not 
    and checking the parallel process"""
    try:
        if str(m.from_user.id) in TIME_GAP_STORE:
            pr_time = TIME_GAP_STORE[str(m.from_user.id)]
            if int(time.time() - pr_time) < TIME_GAP:
                text = f'Please wait {TimeFormatter((int(TIME_GAP_STORE[str(m.from_user.id)]) + TIME_GAP - int(time.time())) * 1000)} before sending new request.'
                await m.reply_text(text=text, quote=True)
                return True
            del TIME_GAP_STORE[m.from_user.id]
            return False
        TIME_GAP_STORE[str(m.from_user.id)] = int(time.time())
        return False
    except Exception as e:
        _LOG.exception(e)
        return False

@jvbot.on_message(filters.command(['log', 'logs']) & filters.user(OWNER_ID))
async def get_log_wm(bot, message) -> None:
    try:
        await message.reply_document('log.txt')
    except Exception as e:
        _LOG.exception(e)

@jvbot.on_message(filters.private & filters.command(['start']))
async def get_help(bot, message) -> None:
    back = await handle_force_sub(bot, message)
    if back == 400:
        return
    pass
    await message.reply_text(text="hey there, i am live video recorder bot, i can record live video using its url\n\n**note: Don't report to Devloper if video duration time wrong**\n\nby @Universal_Projects", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🚨Updates Channel🚨', url='https://t.me/Universal_Projects'), InlineKeyboardButton('👷Support Group👷', url='https://t.me/JV_Community')], [InlineKeyboardButton('🧑\u200d💻Devloper🧑\u200d💻', url='https://github.com/Jigarvarma2005/')]]))

@jvbot.on_message(filters.private & filters.regex(pattern='.*http.*'))
async def main_func(bot: Client, message: Message) -> None:
    back = await handle_force_sub(bot, message)
    if back == 400:
        return
    pass
    url_msg = message.text.split(' ')
    if len(url_msg) != 2:
        return await message.reply_text(text='Please send link in below format, check /help to know more\n\n`link timestamp(hh:mm:ss)`')
    msg_ = await message.reply_text('Please wait ....')
    url = url_msg[0]
    is_ok, url = directLink(url)
    if not is_ok:
        return await msg_.edit(url)
    timess = str(url_msg[1])
    if len(timess.split(':')) > 4:
        return await msg_.edit(text='Please send link in below format, check /help to know more\n\n`link timestamp(hh:mm:ss)`')
    timelimit = int(timess.replace(':', ''))
    if int(timess.rsplit(':', 1)[0].replace(':', '')) >= 50 and message.from_user.id not in AUTH_USERS:
        return await msg_.edit(text='Maximum time limit is 50minutes.\nask in support group to get personal bot without any limit\n\n**Warn:- Nothing is free**', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🚨Updates Channel🚨', url='https://t.me/Universal_Projects'), InlineKeyboardButton('👷Support Group👷', url='https://t.me/JV_Community')], [InlineKeyboardButton('🧑\u200d💻Devloper🧑\u200d💻', url='https://github.com/Jigarvarma2005/')]]))
    if message.from_user.id not in AUTH_USERS:
        time_gap = await timegap_check(message)
        if time_gap:
            return
    await uploader_main(url, msg_, timess)

@jvbot.on_message(filters.private & filters.command('help'))
async def main_func(bot: Client, message: Message) -> None:
    back = await handle_force_sub(bot, message)
    if back == 400:
        return
    pass
    await message.reply_text(text="To record a live link send your link in below format, \n\n `link timestamp`\n\n**Example:**\nhttps://example.com/live-link.m3u8 00:05:00\n\ntimestamp==hh:mm:ss\n\n**note: Don't report to Devloper if video duration time wrong**\n\nby @Universal_Projects", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🚨Updates Channel🚨', url='https://t.me/Universal_Projects'), InlineKeyboardButton('👷Support Group👷', url='https://t.me/JV_Community')], [InlineKeyboardButton('🧑\u200d💻Devloper🧑\u200d💻', url='https://github.com/Jigarvarma2005/')]]))

@jvbot.on_callback_query(filters.regex('time.*?'))
async def cb_handler_main(bot: Client, cb: CallbackQuery):
    cb_data = cb.data.split('_', 1)[1]
    msg = cb.message
    user_link = msg.reply_to_message.text.split(' ')[0]
    await uploader_main(user_link, msg, cb_data)

@jvbot.on_callback_query(filters.regex('refreshmeh.*?'))
async def cb_handler_main(bot: Client, query: CallbackQuery):
    if query.data == 'refreshmeh' and UPDATES_CHANNEL:
        invite_link = await bot.create_chat_invite_link(int(UPDATES_CHANNEL))
        try:
            user = await bot.get_chat_member(int(UPDATES_CHANNEL), query.message.chat.id)
            if user.status == 'kicked':
                await query.message.edit(text='Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/JV_Community).', disable_web_page_preview=True)
        except UserNotParticipant:
            await query.message.edit(text="**You Still Didn't Join ☹️, Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🤖 Join Updates Channel', url=invite_link.invite_link)], [InlineKeyboardButton('🔄 Refresh 🔄', callback_data='refreshmeh')]]))
        except Exception:
            await query.message.edit(text='Something went Wrong. Contact my [Support Group](https://t.me/JV_Community).', disable_web_page_preview=True)
    await query.message.edit('Now you can use me, check /start')

def directLink(link) -> str:
    ytlink = re.match(yt_regex, link)
    if ytlink:
        subcall = subprocess.Popen(f'yt-dlp -g {link}', shell=True, stdout=subprocess.PIPE)
        linkchek = str(subcall.stdout.read().decode('utf-8'))
        _LOG.info(linkchek)
        return (True, linkchek)
    return (True, link)

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

async def uploader_main(usr_link: str, msg: Message, cb_data: str):
    check_bot()
    await msg.edit(text=f'{cb_data} Recording started,\nthis will take time ...', reply_markup=None)
    video_dir_path = join(DOWNLOAD_DIRECTORY, str(time.time()))
    if not os.path.isdir(video_dir_path):
        os.makedirs(video_dir_path)
    video_file_path = join(video_dir_path, str(time.time()) + '.mkv')
    _LOG.info(f'Recording {cb_data} from {usr_link}')
    exe_name = 'ffmpeg'
    probe = '-probesize 10000000'
    anylz = '-analyzeduration 15000000 -timeout 9000000'
    codec = '-codec copy -map 0:v -map 0:a -ignore_unknown'
    error_recording_video = (await runcmd(f'{exe_name} {probe} {anylz} -i {usr_link} -t {cb_data} {codec} {video_file_path}'))[1]
    if error_recording_video:
        _LOG.info(error_recording_video)
    pass
    if exists(video_file_path):
        try:
            v_duration = await get_video_duration(video_file_path)
            await msg.reply_video(video=video_file_path, duration=v_duration, caption=f'Recording done of {usr_link}\n\nDuration: {TimeFormatter(v_duration * 1000)}\n\nBy @Universal_Projects', progress=progress_for_pyrogram, progress_args=(msg, time.time()))
        except Exception as e:
            _LOG.exception(e)
            await msg.edit(e)
    if 'Connection timed out' in error_recording_video:
        await msg.reply_text(f'Connection timed out with {usr_link}', quote=True)
    else:
        await msg.reply_text('Recording failed, probably link error ...', quote=True)
    try:
        try:
            shutil.rmtree(video_dir_path)
        except:
            pass
        await msg.delete()
    except Exception as e:
        _LOG.exception(e)

async def get_video_duration(input_file):
    metadata = extractMetadata(createParser(input_file))
    total_duration = 0
    if metadata.has('duration'):
        total_duration = metadata.get('duration').seconds
    return total_duration

def create_time_buttons():
    return InlineKeyboardMarkup([[InlineKeyboardButton('30min', callback_data='time_0:30'), InlineKeyboardButton('1Hour', callback_data='time_1:00')], [InlineKeyboardButton('1Hr 30min', callback_data='time_1:30'), InlineKeyboardButton('2Hour', callback_data='time_2:00')], [InlineKeyboardButton('2Hr 30min', callback_data='time_2:30'), InlineKeyboardButton('3Hr', callback_data='time_3:00')]])

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """ run command in terminal """
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    stdout = stdout.decode('utf-8', 'replace').strip()
    stderr = stderr.decode('utf-8', 'replace').strip()
    return (stdout, stderr, process.returncode, process.pid)

async def progress_for_pyrogram(current, total, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.0) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        comp = '▪️'
        ncomp = '▫️'
        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
        pr = ''
        try:
            percentage = int(percentage)
        except:
            percentage = 0
        for i in range(1, 11):
            if i <= int(percentage / 10):
                pr += comp
            else:
                pr += ncomp
        progress = 'Uploading: {}%\n[{}]\n'.format(round(percentage, 2), pr)
        tmp = progress + '{0} of {1}\nSpeed: {2}/sec\nETA: {3}'.format(humanbytes(current), humanbytes(total), humanbytes(speed), estimated_total_time if estimated_total_time != '' else '0 s')
        try:
            await message.edit(text='{}\n {}'.format(tmp))
        except:
            return

def humanbytes(size):
    if not size:
        return ''
    power = 1024
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: 'P', 6: 'E', 7: 'Z', 8: 'Y'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + ' ' + Dic_powerN[n] + 'B'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (str(days) + 'd, ' if days else '') + (str(hours) + 'h, ' if hours else '') + (str(minutes) + 'm, ' if minutes else '') + (str(seconds) + 's, ' if seconds else '') + (str(milliseconds) + 'ms, ' if milliseconds else '')
    return tmp[:-2]
if not os.path.isdir(DOWNLOAD_DIRECTORY):
    os.makedirs(DOWNLOAD_DIRECTORY)
check_bot()
jvbot.start()
_LOG.info('Bot Started!')
idle()
_LOG.info('Bot Stopped!')
jvbot.stop()