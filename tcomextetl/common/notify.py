from tcomextetl.extract.http_requests import HttpRequest


def send_message(token: str, message: str):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {
        'text': message,
        'chat_id': 498912844,
        'parse_mode': 'HTML'
    }

    s = HttpRequest()
    r = s.request(
        url,
        data=data
    )


def send_document(token: str, caption: str, fpath: str):
    url = f'https://api.telegram.org/bot{token}/sendDocument'
    data = {
        'chat_id': 498912844,
        'parse_mode': 'HTML',
        'caption': caption
    }

    s = HttpRequest()
    r = s.request(
        url,
        data=data,
        files={'document': open(fpath, 'rb')}
    )
    print(r.text)