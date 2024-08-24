import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import logging
import os
from openai import OpenAI
import openai
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
async def cmd_start(message: types.Message, conv: list[dict]):
    conv = conv_init
    await message.answer("Everything is set up")

@dp.message(F.voice)
async def handle_voice_message(message: types.Message, conv: list[dict]):
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
    
    # Transcribe the .wav file
    transcription = transcribe_audio(wav_file_path)
    print(transcription)
    conv.append({"role": "user", "content": transcription})

    await message.reply(generate_response(conv))

    if random.random()>=0.75:
        print("err")
        conv.append({"role": "system", "content": "Someone sent you a voice message, but you don't like it when people send them."})
        await message.answer(generate_response(conv))


    # Clean up
    os.remove(local_file_path)
    os.remove(wav_file_path)

@dp.message(F.photo)
async def handle_photo(message: types.Message, conv: list[dict]):

    file_info = await bot.get_file(message.photo[1].file_id)
    print(file_info)
    file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
    print(file_url)

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
async def handle_non_voice_message(message: types.Message, conv: list[dict]):
    conv.append({"role": "system", "content": f"You were sent some file and you are too lazy to download it, you comment on it"})
    await message.answer(generate_response(conv))

@dp.message()
async def chat(message: types.Message, conv: list[dict]):

    if message.sticker:
       conv.append(
        {"role": "system", "content": "You were sent a sticker - " + message.sticker.emoji + " and it pisses you off when they send them"})
    elif message.text:
        conv.append({"role": "user", "content": message.text})
        print(conv!=conv_init)
        if random.random()>=0.7 and conv!=conv_init:
            conv.append({"role": "system", "content": "You say that you are not interested in talking to me and decide to change the topic of conversation to: " + topics[random.randint(0, len(topics) - 1)]})
    
    text = generate_response(conv)
    conv.append(
            {"role": "assistant", "content": text}
        )
    await message.answer(text)
    if random.random()>=0.75:
        await message.answer_sticker(stickers[random.randint(0, len(stickers) - 1)])

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot, conv = conv_init)

if __name__ == "__main__":
    asyncio.run(main())