from tcomextetl.extract.http_requests import HttpRequest


def send_message(token: str, chats: list, message: str):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {
        'text': message,
        # 'chat_id': 498912844,
        'parse_mode': 'HTML'
    }

    s = HttpRequest()
    for chat_id in chats:
        d = data
        d['chat_id'] = chat_id
        r = s.request(url, data=d)


def send_document(token: str, chats: list, caption: str, fpath: str):
    url = f'https://api.telegram.org/bot{token}/sendDocument'
    data = {
        # 'chat_id': 498912844,
        'parse_mode': 'HTML',
        'caption': caption
    }

    s = HttpRequest()
    for chat_id in chats:
        d = data
        d['chat_id'] = chat_id
        r = s.request(
            url,
            data=d,
            files={'document': open(fpath, 'rb')}
        )