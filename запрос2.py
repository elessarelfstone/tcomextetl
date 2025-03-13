import requests
import csv
import datetime
import time

# URL для запроса
url = 'https://api.rocketdata.io/public/v4/reviews/'

# Заголовки, включая авторизацию
headers = {
    'Authorization': 'Token 2f1f89b21bb1b3da6e2280fa2f1bc4dee1fda68f'
}

# Начальная и конечная дата
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2025, 2, 20)

# Файл для записи данных на рабочем столе
output_file = r'C:\Users\telecom.kz\Desktop\report2.csv'

# Открытие CSV файла для записи данных
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Записываем заголовки для CSV (включаем все возможные поля)
    writer.writerow([
        'date', 'author', 'created_in_catalog', 'created_in_rd', 'parsed_at', 'comment', 'rating', 'origin_url',
        'location_url', 'company_name', 'company_code', 'company_country', 'company_region', 'company_city', 
        'company_street', 'company_housenumber', 'company_postcode', 'brand_name', 'brand_is_test', 
        'able_to_reply', 'able_to_abuse', 'tags', 'is_changed', 'catalog_id', 'reply_author', 'reply_comment',
        'reply_created_in_catalog', 'reply_created_in_rd', 'reply_parsed_at', 'is_company_comment', 
        'is_autoreply', 'able_to_edit', 'able_to_delete'
    ])

    # Цикл для перебора дней от start_date до end_date
    current_date = start_date
    while current_date <= end_date:
        # Преобразуем дату в строку в нужном формате (например, '2020-01-01')
        date_str = current_date.strftime('%Y-%m-%d')

        # Параметры фильтрации по конкретной дате
        params = {
            'date_gte': date_str,  # Начальная дата
            'date_lte': date_str     # Конечная дата (та же самая, что и start_date)
        }

        # Отправка GET-запроса
        print(f"Отправка запроса для даты {date_str}...")
        response = requests.get(url, headers=headers, params=params)

        # Если запрос вернул ошибку 429 (слишком много запросов), ждём некоторое время
        if response.status_code == 429:
            retry_after = response.headers.get('Retry-After')  # Получаем информацию о времени ожидания
            if retry_after:
                print(f"Превышен лимит запросов, ждем {retry_after} секунд...")
                time.sleep(int(retry_after))  # Ждём, как указано в заголовке Retry-After
            else:
                print("Превышен лимит запросов, ждем 60 секунд...")
                time.sleep(60)  # Если заголовок Retry-After не указан, ждём 60 секунд
            continue  # После паузы возвращаемся к следующей итерации

        # Проверка успешности запроса
        if response.status_code == 200:
            data = response.json()  # Преобразуем ответ в JSON

            # Перебираем результаты и записываем в CSV
            for item in data.get('results', []):  # Извлекаем только данные отзывов
                author = item.get('author', 'N/A')
                created_in_catalog = item.get('created_in_catalog', 'N/A')
                created_in_rd = item.get('created_in_rd', 'N/A')
                parsed_at = item.get('parsed_at', 'N/A')
                comment = item.get('comment', 'N/A')
                rating = item.get('rating', 'N/A')
                origin_url = item.get('origin_url', 'N/A')
                location_url = item.get('location_url', 'N/A')
                
                # Компания
                company = item.get('company', {})
                company_name = company.get('name', 'N/A')
                company_code = company.get('code', 'N/A')
                company_country = company.get('address', {}).get('country', 'N/A')
                company_region = company.get('address', {}).get('region', 'N/A')
                company_city = company.get('address', {}).get('city', 'N/A')
                company_street = company.get('address', {}).get('street', 'N/A')
                company_housenumber = company.get('address', {}).get('housenumber', 'N/A')
                company_postcode = company.get('address', {}).get('postcode', 'N/A')

                # Бренд
                brand = item.get('brand', {})
                brand_name = brand.get('name', 'N/A')
                brand_is_test = brand.get('is_test', 'N/A')

                able_to_reply = item.get('able_to_reply', 'N/A')
                able_to_abuse = item.get('able_to_abuse', 'N/A')
                tags = item.get('tags', 'N/A')
                is_changed = item.get('is_changed', 'N/A')
                catalog_id = item.get('catalog_id', 'N/A')

                # Ответы на отзывы (если есть)
                children = item.get('children', [])
                for reply in children:
                    reply_author = reply.get('author', 'N/A')
                    reply_comment = reply.get('comment', 'N/A')
                    reply_created_in_catalog = reply.get('created_in_catalog', 'N/A')
                    reply_created_in_rd = reply.get('created_in_rd', 'N/A')
                    reply_parsed_at = reply.get('parsed_at', 'N/A')
                    is_company_comment = reply.get('is_company_comment', 'N/A')
                    is_autoreply = reply.get('is_autoreply', 'N/A')
                    able_to_edit = reply.get('able_to_edit', 'N/A')
                    able_to_delete = reply.get('able_to_delete', 'N/A')

                    # Записываем данные в CSV (включая информацию о ответах)
                    writer.writerow([
                        date_str, author, created_in_catalog, created_in_rd, parsed_at, comment, rating, origin_url,
                        location_url, company_name, company_code, company_country, company_region, company_city,
                        company_street, company_housenumber, company_postcode, brand_name, brand_is_test, able_to_reply,
                        able_to_abuse, tags, is_changed, catalog_id, reply_author, reply_comment, reply_created_in_catalog,
                        reply_created_in_rd, reply_parsed_at, is_company_comment, is_autoreply, able_to_edit, able_to_delete
                    ])
                
                # Если нет ответов, то записываем только основной отзыв
                if not children:
                    writer.writerow([
                        date_str, author, created_in_catalog, created_in_rd, parsed_at, comment, rating, origin_url,
                        location_url, company_name, company_code, company_country, company_region, company_city,
                        company_street, company_housenumber, company_postcode, brand_name, brand_is_test, able_to_reply,
                        able_to_abuse, tags, is_changed, catalog_id, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
                    ])

            print(f"Данные за {date_str} успешно записаны в CSV.")
        else:
            print(f"Ошибка на {date_str}: {response.status_code}")

        # Переход к следующему дню
        current_date += datetime.timedelta(days=1)

        # Задержка между запросами (например, 1 секунда)
        time.sleep(1)

print(f"Данные успешно записаны в {output_file}")
