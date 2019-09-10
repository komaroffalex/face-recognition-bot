import face_recognition
import sys
import os
import requests
import time
import datetime


url = "https://api.telegram.org/bot937357111:AAEzuYg08qB6601q5LbjHSmox8vROHSSnU8/"
token = "937357111:AAEzuYg08qB6601q5LbjHSmox8vROHSSnU8"


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


greet_bot = BotHandler(token)
greetings = ('здравствуй', 'привет', 'ку', 'здорово')
now = datetime.datetime.now()


def recognition_sample():
    picture_of_me = face_recognition.load_image_file("db/me.jpg")
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

    # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

    unknown_picture = face_recognition.load_image_file("db/also_me.jpg")
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

    # Now we can see the two face encodings are of the same person with `compare_faces`!

    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

    if results[0] == True:
        print("It's a picture of me!")
        sys.stdout.write("It's a picture of me!")
        os.write(1, b"It's a picture of me!")
    else:
        print("It's not a picture of me!")
        sys.stdout.write("It's not a picture of me!")
        os.write(1, b"It's not a picture of me!")


def main():
    new_offset = None
    today = now.day
    hour = now.hour
    print("Main entered!")
    sys.stdout.write("Main entered!")
    os.write(1, b"Main entered!")

    while True:
        print("While iterator entered!")
        sys.stdout.write("While iterator entered!")
        os.write(1, b"While iterator entered!")
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
            today += 1

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        recognition_sample()
        main()
    except KeyboardInterrupt:
        exit()
