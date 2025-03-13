import requests
import csv
import datetime
import time


url = 'https://api.rocketdata.io/public/v4/reviews/'


auth_headers = {
    'Authorization': 'Token 2f1f89b21bb1b3da6e2280fa2f1bc4dee1fda68f'
}


yesterday = datetime.date.today() - datetime.timedelta(days=1)
date_str = yesterday.strftime('%Y-%m-%d')


output_file = r'C:\Users\telecom.kz\Desktop\report2.csv'


csv_headers = [
    'date', 'author', 'created_in_catalog', 'created_in_rd', 'parsed_at', 'comment', 'rating', 'origin_url',
    'location_url', 'company_name', 'company_code', 'company_country', 'company_region', 'company_city', 
    'company_street', 'company_housenumber', 'company_postcode', 'brand_name', 'brand_is_test', 
    'able_to_reply', 'able_to_abuse', 'tags', 'is_changed', 'catalog_id', 'review_id', 'reply_author', 
    'reply_comment', 'reply_created_in_catalog', 'reply_created_in_rd', 'reply_parsed_at', 'is_company_comment', 
    'is_autoreply', 'able_to_edit', 'able_to_delete'
]


existing_reviews = {}
try:
    with open(output_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            review_id = row['review_id']
            existing_reviews[review_id] = row  
except FileNotFoundError:
    print("Файл не найден. Создается новый файл.")


params = {
    'date_gte': date_str,
    'date_lte': date_str
}


print(f"Отправка запроса для даты {date_str}...")
response = requests.get(url, headers=auth_headers, params=params)


if response.status_code == 429:
    retry_after = response.headers.get('Retry-After')
    if retry_after:
        print(f"Превышен лимит запросов, ждем {retry_after} секунд...")
        time.sleep(int(retry_after))
    else:
        print("Превышен лимит запросов, ждем 60 секунд...")
        time.sleep(60)
    response = requests.get(url, headers=auth_headers, params=params)


if response.status_code == 200:
    data = response.json()

   
    for item in data.get('results', []):
        review_id = item.get('id', 'N/A')

        
        record = {
            'date': date_str,
            'author': item.get('author', 'N/A'),
            'created_in_catalog': item.get('created_in_catalog', 'N/A'),
            'created_in_rd': item.get('created_in_rd', 'N/A'),
            'parsed_at': item.get('parsed_at', 'N/A'),
            'comment': item.get('comment', 'N/A'),
            'rating': item.get('rating', 'N/A'),
            'origin_url': item.get('origin_url', 'N/A'),
            'location_url': item.get('location_url', 'N/A'),
            'company_name': item.get('company', {}).get('name', 'N/A'),
            'company_code': item.get('company', {}).get('code', 'N/A'),
            'company_country': item.get('company', {}).get('address', {}).get('country', 'N/A'),
            'company_region': item.get('company', {}).get('address', {}).get('region', 'N/A'),
            'company_city': item.get('company', {}).get('address', {}).get('city', 'N/A'),
            'company_street': item.get('company', {}).get('address', {}).get('street', 'N/A'),
            'company_housenumber': item.get('company', {}).get('address', {}).get('housenumber', 'N/A'),
            'company_postcode': item.get('company', {}).get('address', {}).get('postcode', 'N/A'),
            'brand_name': item.get('brand', {}).get('name', 'N/A'),
            'brand_is_test': item.get('brand', {}).get('is_test', 'N/A'),
            'able_to_reply': item.get('able_to_reply', 'N/A'),
            'able_to_abuse': item.get('able_to_abuse', 'N/A'),
            'tags': item.get('tags', 'N/A'),
            'is_changed': item.get('is_changed', 'N/A'),
            'catalog_id': item.get('catalog_id', 'N/A'),
            'review_id': review_id
        }

      
        existing_reviews[review_id] = record

    
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(existing_reviews.values())

    print(f"Данные за {date_str} успешно обновлены в CSV.")
else:
    print(f"Ошибка на {date_str}: {response.status_code}")
