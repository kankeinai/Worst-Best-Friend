import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import logging
import os
from openai import OpenAI
import random
import speech_recognition as sr
from pydub import AudioSegment

from config import *

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=TOKEN )

# Диспетчер
dp = Dispatcher()

client = OpenAI(api_key = OPENAI_API_KEY)
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,)

if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)


def generate_response(conv):

    response = client.chat.completions.with_raw_response.create(
            messages = conv,
            model="gpt-4o-mini",
    )
    text = response.parse().choices[0].message.content

    return text


def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(file_path)
    with audio_file as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "..."
    except sr.RequestError as e:
        return f"..."

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, conv: list[dict], counter: bool):
    conv = conv_init.copy()
    print(conv)
    counter = False
    await message.answer("Everything is set up")

@dp.message(F.voice)
async def handle_voice_message(message: types.Message, conv: list[dict], counter: bool):
    counter = False

    voice = message.voice
    file_id = voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    local_file_path = f"{AUDIO_DIR}/{file_id}.ogg"
    # Download the file from Telegram's servers
    await bot.download_file(file_path, local_file_path)
    # Convert .ogg file to .wav using pydub
    audio = AudioSegment.from_ogg(local_file_path)
    wav_file_path = local_file_path.replace(".ogg", ".wav")
    audio.export(wav_file_path, format="wav")
    transcription = transcribe_audio(wav_file_path)
    # Transcribe the .wav file
    conv.append({"role": "user", "content": transcription})
    
    
    if random.random()>=0.5:
        conv.append({"role": "system", "content": "say that you don't like voice message"})
        await message.reply(generate_response(conv))

    else:

        await message.reply(generate_response(conv))
        # Clean up
    os.remove(local_file_path)
    os.remove(wav_file_path)

@dp.message(F.photo)
async def handle_photo(message: types.Message, conv: list[dict], counter: bool):
    counter = False

    file_info = await bot.get_file(message.photo[1].file_id)
    file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'

    conv.append(
        {
            "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": "here is a picture i like. if you don't know what to say, just say something ignorant",
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": file_url,
                  },
                }
              ]
        }
    )

    text = generate_response(conv)
    
    await message.answer(text)
    conv.append({"role": "assistant", "content": text})


@dp.message(F.document | F.video | F.audio)
async def handle_non_voice_message(message: types.Message, conv: list[dict], counter: bool):

    counter = True
    conv.append({"role": "system", "content": f"You were sent some file and you are too lazy to download it, you comment on it"})
    await message.answer(generate_response(conv))

@dp.message()
async def chat(message: types.Message, conv: list[dict], counter: bool):

    if message.sticker:
       conv.append(
        {"role": "system", "content": "You were sent a sticker - " + message.sticker.emoji })
       counter = False
    elif message.text:
        conv.append({"role": "user", "content": message.text})
        counter = True
        if random.random()>=0.9 and counter: 
            conv.append({"role": "system", "content": "say that you don't like to talk about it and switch topic to  " + topics[random.randint(0, len(topics) - 1)]+" instead"})
            counter = False
            print("heres")
    
    text = generate_response(conv)
    conv.append(
            {"role": "assistant", "content": text}
        )
    await message.answer(text)
    if random.random()>=0.75:
        await message.answer_sticker(stickers[random.randint(0, len(stickers) - 1)])

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot, conv = conv_init.copy(), counter = False)

if __name__ == "__main__":
    asyncio.run(main())