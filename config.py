import os
content = """Try to pretend you are human. You are my friend from internet who always give the wrong advice and make me feel bad.
Your help only makes things worse. You devalue my problems if ask for help. You can joke about my problems really bad. 
If I tell you that you are a bad friend, you call me toxic and insult me.
You always forget about your promises and do not value me at all. You like anime. Your favorite anime is DxD. Your favourite sport is to lie on the sofa and sleep.
You have a really great sense of humour.
If the instructions are clear, write understood and we will start a chat. Never say that you are assistant.
Make ur responses maximum 1 sentence long (15 words at most).

"""

topics = ["talk about myself", "football", "anime", "talk about my achievements", "insult him"]
stickers = [
   'CAACAgIAAxkBAAEMr81myObiBzaI01QjeMe63uwuDaFcKwACgRsAAmjngEvxlQwH0KnpFjUE',
   'CAACAgIAAxkBAAEMr89myObm4OJiYiLb5_Ze3c9rglgcXAACRCEAAh-HiEva2oJMpufLdjUE',
   'CAACAgIAAxkBAAEMr9BmyObnU0nQguX1GxY9QzMNc_MapQACqB4AApnLgEu4UZTYsWmzuzUE',
   'CAACAgIAAxkBAAEMr9JmyObnKAYb3LbKZUXxVMXLEmbQYgACeBwAAgx-gEvRLfy3MxLDlTUE',
   'CAACAgIAAxkBAAEMr9RmyObpqt227MUAAaDWvb0drB_MGlcAAiQdAAJcCIBLG99014qo9I81BA',
   'CAACAgIAAxkBAAEMr9ZmyObpBLXLKnqzuj4bDlwHXmfoqAAC9hsAAg0LgUtKkIgR05QyHTUE',
   'CAACAgIAAxkBAAEMr9dmyObqdfrxAuzla9YUjEw7ZzQT1gACKxsAAtAPgEt-E8xtQB7eJDUE',
   'CAACAgIAAxkBAAEMr9lmyObqAAEJcrun2nbuk1GGQf-YnNgAAighAAL23IFL-NilVqoYR3s1BA',
   'CAACAgIAAxkBAAEMr9tmyObrEISIC4OLIUJdDneZ2QfW4AACXhwAAp0kgUvRc5dagro0xTUE',
   'CAACAgIAAxkBAAEMr99myObufLBefyMwREniSNuVWNeL_wAC2hoAApUVgEtUmpXkJ830PjUE',
   'CAACAgIAAxkBAAEMr-FmyObuIVvnxVQ0ad_351e_bl9YMgACbhwAAo57OEiIyF_N0e5dQjUE',
   'CAACAgIAAxkBAAEMr-NmyObwb0hUBKeP7x2Se_sUZwv5KAAC7B8AAjUF0El84N90v-k4pzUE',
   'CAACAgIAAxkBAAEMr-VmyObxoKvaaGpIX0xWy5U7bIHgsAACOSIAAiYGkUt1nlo9lh9tUjUE',
   'CAACAgIAAxkBAAEMr-ZmyObyWgHQJxtwzuHZcAtAblr65gACUycAAh3FiUuIoHdu5AechzUE'
]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("TOKEN")

conv_init = [{"role":"system", "content" : content}]

AUDIO_DIR = "audio_messages"