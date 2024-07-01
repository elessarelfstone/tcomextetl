# -*- coding: utf-8 -*-
import gzip
import json
import os
import shutil
from collections import deque
from datetime import datetime, timedelta, date
from math import floor
from pathlib import Path
from time import sleep
import logging

import luigi
from luigi import TupleParameter
from collections import defaultdict
from luigi.contrib.ftp import RemoteTarget
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from tasks.base import Runner, ApiToCsv, ExternalFtpCsvDFInput, FtpUploadedOutput
from tcomextetl.common.csv import dict_to_row, save_csvrows
from tcomextetl.common.dates import first_day_of_previous_month, last_day_of_previous_month, DEFAULT_FORMAT
from tcomextetl.common.utils import append_file_tuple, rewrite_file, read_csv_tuples
from tcomextetl.extract.gosreestrkz_requests import GosreestrKzRequests
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ProxyError, SSLError, ReadTimeout, ConnectionError
from settings import PROXY_FACTORY_USER, PROXY_FACTORY_PASS

base_url = 'https://gr5.gosreestr.kz/p/ru/gr-search/search-objects'
region_dict = {
    "11819,11819036,11819037,11819049,11819043,11819041,11819042,11819045,11819047,11819033,11819035,11805,11805061,11805068,11805062,11805063,11805064,11805066,11805067,11805065,11805069,11805070,11805071,11805060,11805072,11807,11807093,11807094,11807085,11807095,11807084,11807211,11807210,11807097,11807098,11807099,11807088,11807089,11807091,11807096,11807086,11807087,11807090,11807100,11807092,11807101,11808,11808106,11808107,11808103,11808108,11808109,11808110,11808111,11808112,11808113,11808114,11808102,11808115,11808104,11808116,11808117,11808119,11808105,11808118,11808120,11808121,11809,11809123,11809130,11809124,11809125,11809126,11809127,11809122,11809128,11809129,11810,11810130,11810132,11810131,11810133,11810134,11810210,11810135,11815,11815199,11815210,11815209,11815200,11815211,11812,11812160,11812153,11812155,11812156,11812157,11812158,11812161,11812152,11812162,11812159,11812163,11812165,11812154,11813,11813166,11813167,11813174,11813169,11813170,11813171,11813172,11813164,11813178,11813168,11813173,11813175,11813177,11813176,11811,11811140,11811137,11811141,11811152,11811142,11811153,11811138,11811143,11811144,11811145,11811146,11811147,11811154,11811148,11811149,11811139,11811150,11811136,11807213,11807212,11807214,11807215,11811151,11820,11820096,11820086,11820087,11820090,11820100,11817,11817001,11817002,11817003,11817004,11817005,014,01400,01400000,013,01300,01300000,016,01600,01600000,006,00600,00600000,058,05800,05800000,012,01200,01200000,100,10000,10000000,009,00900,00900000,005,00500,00500000,001,00100,00100000,010,01000,01000000,004,00400,00400000,011,01100,01100000,007,00700,00700000,015,01500,01500000,003,00300,00300000,019,01900,01900000,018,01800,01800000,030,03000,03000000,023,02300,02300000,034,03400,03400000,035,03500,03500000,020,02000,02000000,025,02500,02500000,026,02600,02600000,022,02200,02200000,028,02800,02800000,017,01700,01700000,033,03300,03300000,029,02900,02900000,027,02700,02700000,021,02100,02100000,024,02400,02400000,031,03100,03100000,232,23200,23200000,226,22600,22600000,221,22100,22100000,095,09500,09500000,228,22800,22800000,229,22900,22900000,230,23000,23000000,213,21300,21300000,231,23100,23100000,073,07300,07300000,080,08000,08000000,077,07700,07700000,092,09200,09200000,082,08200,08200000,086,08600,08600000,081,08100,08100000,088,08800,08800000,075,07500,07500000,053,05300,05300000,078,07800,07800000,090,09000,09000000,074,07400,07400000,079,07900,07900000,084,08400,08400000,244,24400,087,08700,08700000,089,08900,08900000,055,05500,05500000,054,05400,05400000,057,05700,05700000,056,05600,05600000,061,06100,06100000,240,24000,24000000,239,23900,23900000,062,06200,06200000,241,24100,24100000,098,09800,09800000,099,09900,09900000,096,09600,09600000,106,10600,10600000,101,10100,10100000,102,10200,10200000,097,09700,09700000,103,10300,10300000,064,06400,06400000,104,10400,10400000,235,23500,23500000,117,11700,11700000,110,11000,11000000,044,04400,04400000,036,03600,03600000,049,04900,04900000,178,17800,17800000,108,10800,10800000,051,05100,05100000,111,11100,11100000,045,04500,04500000,037,03700,03700000,046,04600,04600000,112,11200,11200000,039,03900,03900000,047,04700,04700000,041,04100,04100000,048,04800,04800000,116,11600,11600000,109,10900,10900000,119,11900,11900000,128,12800,12800000,120,12000,12000000,125,12500,12500000,124,12400,12400000,129,12900,12900000,126,12600,12600000,243,24300,24300000,122,12200,12200000,127,12700,12700000,242,24200,24200000,142,14200,14200000,133,13300,13300000,236,23600,23600000,139,13900,13900000,135,13500,13500000,147,14700,14700000,149,14900,14900000,069,06900,06900000,146,14600,14600000,136,13600,13600000,144,14400,14400000,141,14100,14100000,134,13400,13400000,145,14500,14500000,137,13700,13700000,148,14800,14800000,150,15000,15000000,132,13200,13200000,131,13100,13100000,138,13800,13800000,143,14300,14300000,130,13000,13000000,151,15100,15100000,160,16000,16000000,008,00800,00800000,222,22200,22200000,161,16100,16100000,159,15900,15900000,153,15300,15300000,155,15500,15500000,157,15700,15700000,156,15600,15600000,162,16200,16200000,163,16300,16300000,152,15200,15200000,158,15800,15800000,154,15400,15400000,002,00200,00200000,164,16400,16400000,032,03200,03200000,233,23300,23300000,042,04200,04200000,191,19100,19100000,203,20300,20300000,070,07000,07000000,091,09100,09100000,050,05000,05000000,170,17000,17000000,176,17600,17600000,165,16500,16500000,168,16800,16800000,177,17700,17700000,166,16600,16600000,173,17300,17300000,171,17100,17100000,175,17500,17500000,174,17400,17400000,179,17900,17900000,181,18100,18100000,182,18200,18200000,180,18000,18000000,234,23400,23400000,194,19400,19400000,200,20000,20000000,113,11300,11300000,121,12100,12100000,198,19800,19800000,183,18300,18300000,189,18900,18900000,172,17200,17200000,202,20200,20200000,085,08500,08500000,114,11400,11400000,185,18500,18500000,195,19500,19500000,245,24500,24500000,188,18800,18800000,201,20100,20100000,192,19200,19200000,190,19000,19000000,227,22700,22700000,199,19900,19900000,184,18400,18400000,196,19600,19600000,186,18600,18600000,197,19700,19700000,223,22300,22300000,193,19300,19300000,208,20800,20800000,207,20700,20700000,217,21700,21700000,218,21800,21800000,206,20600,20600000,209,20900,20900000,212,21200,21200000,215,21500,21500000,216,21600,21600000,211,21100,21100000,210,21000,21000000,214,21400,21400000,220,22000,22000000,225,22500,22500000,219,21900,21900000,224,22400,22400000,068,06800,06800000,067,06700,06700000,066,06600,06600000,169,16900,16900000,071,07100,07100000,072,07200,07200000,076,07600,07600000,167,16700,16700000,094,09400,09400000,093,09300,09300000,083,08300,08300000,038,03800,03800000,204,20400,20400000,246,24600,24600000,052,05200,05200000,043,04300,04300000,040,04000,04000000,187,18700,18700000,123,12300,12300000,059,05900,05900000,063,06300,06300000,060,06000,06000000,065,06500,06500000,237,23700,23700000,238,23800,23800000,115,11500,11500000,140,14000,14000000,205,20500,20500000,105,10500,10500000,107,10700,10700000": "область Жетісу; Аксуский район; Алакольский район; Ескельдинский район; Каратальский район; Кербулакский район; Коксуский район; Панфиловский район; Саркандский район; Талдыкорган г.а.; Текели г.а.; Западно-Казахстанская область; Акжаикский район; Бокейординский район; Бурлинский район; Джангалинский район; Жанибекский район; Казталовский район; Каратобинский район; район Бәйтерек; Сырымский район; Таскалинский район; Теректинский район; Уральск г.а.; Чингирлауский район; Карагандинская область; Абайский район; Актогайский район; Балхаш г.а.; Бухар-Жырауский район; Караганды г.а.; Караганды г.а. - район им. Казыбек би; Караганды г.а. - район Әлихан Бөкейхан; Каркаралинский район; Нуринский район; Осакаровский район; Приозерск г.а.; Сарань г.а.; Темиртау г.а.; УСТАРЕВШЕЕ - Жанааркинский район; УСТАРЕВШЕЕ - Жезказган г.а.; УСТАРЕВШЕЕ - Каражал г.а.; УСТАРЕВШЕЕ - Сатпаев г.а.; УСТАРЕВШЕЕ - Улытауский район; Шахтинск г.а.; Шетский район; Костанайская область; Алтынсаринский район; Амангельдинский район; Аркалык г.а.; Аулиекольский район; Денисовский район; Джангельдинский район; Житикаринский район; Камыстинский район; Карабалыкский район; Карасуский район; Костанай г.а.; Костанайский район; Лисаковск г.а.; Мендыкаринский район; Наурзумский район; Район Беимбета Майлина; Рудный г.а.; Сарыкольский район; Узункольский район; Федоровский район; Кызылординская область; Аральский район; Байконыр г.а.; Жалагашский район; Жанакорганский район; Казалинский район; Кармакшинский район; Кызылорда г.а.; Сырдарьинский район; Шиелийский район; Мангистауская область; Актау г.а.; Бейнеуский район; Жанаозен г.а.; Каракиянский район; Мангистауский район; Мунайлинский район; Тупкараганский район; Астана г.а.; Алматинская р.а.; Байконыр р.а.; Есильский р. а.; Сарыаркинская р.а.; Нура р.а.; Павлодарская область; Аккулы район; Аксу г.а.; Актогайский район; Баянаульский район; Железинский район; Иртышский район; Майский район; Павлодар г.а.; Павлодарский район; Теренколь район; Успенский район; Щербактинский район; Экибастуз г.а.; Северо-Казахстанская область; Айыртауский район; Акжарский район; Аккайынский район; Есильский район; Жамбылский район; Кызылжарский район; Мамлютский район; Петропавловск г.а.; Район Габита Мусрепова; Район Магжана Жумабаева; Район Шал акына; Тайыншинский район; Тимирязевский район; Уалихановский район; Туркестанская область; Арысский район; Арысь г.а.; Байдибек район; Жетысайский район; Казыгуртский район; Келесский район; Кентау г.а.; Махтааральский район; Ордабасынский район; Отрарский район; Сайрамский район; Сарыагашский район; Сауран район; Сузакский район; Толебийский район; Туркестан г.а.; Тюлькубасский район; УСТАРЕВШЕЕ - Шымкент г.а.; УСТАРЕВШЕЕ - Шымкент г.а. - Абайский район; УСТАРЕВШЕЕ - Шымкент г.а. - Аль-Фарабийский район; УСТАРЕВШЕЕ - Шымкент г.а. - Енбекшинский район; УСТАРЕВШЕЕ - Шымкент г.а. - Каратауский район; Шардаринский район; область Ұлытау; Жанааркинский район; Жезказган г.а.; Каражал г.а.; Сатпаев г.а.; Улытауский район; Шымкент г.а.; Абайский р.а.; Аль-Фарабийский р.а.; Енбекшинский р.а.; Каратауский р.а.; район Тұран; Австралия; Зарубеж; Зарубеж; Австрия; Зарубеж; Зарубеж; Азербайжан; Зарубеж; Зарубеж; Албания; Зарубеж; Зарубеж; Алгерия; Зарубеж; Зарубеж; Американская Самоа; Зарубеж; Зарубеж; Англ. Терр. в Индийском Океане; Зарубеж; Зарубеж; Ангола; Зарубеж; Зарубеж; Ангуилла; Зарубеж; Зарубеж; Андора; Зарубеж; Зарубеж; Антарктика; Зарубеж; Зарубеж; Антигуа и Барбуда; Зарубеж; Зарубеж; Аргентина; Зарубеж; Зарубеж; Армения; Зарубеж; Зарубеж; Аруба; Зарубеж; Зарубеж; Афганистан; Зарубеж; Зарубеж; Бангладеш; Зарубеж; Зарубеж; Барбадос; Зарубеж; Зарубеж; Бахамас; Зарубеж; Зарубеж; Бахрейн; Зарубеж; Зарубеж; Беларусия; Зарубеж; Зарубеж; Белиз; Зарубеж; Зарубеж; Бельгия; Зарубеж; Зарубеж; Бенин; Зарубеж; Зарубеж; Бермуды; Зарубеж; Зарубеж; Болгария; Зарубеж; Зарубеж; Боливия; Зарубеж; Зарубеж; Босния Герцеговина; Зарубеж; Зарубеж; Ботсвана; Зарубеж; Зарубеж; Бразилия; Зарубеж; Зарубеж; Бруней Даррусалам; Зарубеж; Зарубеж; Буркина Фасо; Зарубеж; Зарубеж; Бурундия; Зарубеж; Зарубеж; Бхутан; Зарубеж; Зарубеж; Вануату; Зарубеж; Зарубеж; Ватикан; Зарубеж; Зарубеж; Великобритания; Зарубеж; Зарубеж; Венгрия; Зарубеж; Зарубеж; Венесуэлла; Зарубеж; Зарубеж; Виргинские острова (Великобритания); Зарубеж; Зарубеж; Виргинские острова (США); Зарубеж; Зарубеж; Восточный Тимор; Зарубеж; Зарубеж; Вьетнам; Зарубеж; Зарубеж; Габон; Зарубеж; Зарубеж; Гамбия; Зарубеж; Зарубеж; Гана; Зарубеж; Зарубеж; Гандурас; Зарубеж; Зарубеж; Гваделупа; Зарубеж; Зарубеж; Гватемала; Зарубеж; Зарубеж; Гвинея; Зарубеж; Зарубеж; Гвинея-Биссау; Зарубеж; Зарубеж; Георгия; Зарубеж; Зарубеж; Германия; Зарубеж; Зарубеж; Гибралтар; Зарубеж; Зарубеж; Гонк-Конг; Зарубеж; Зарубеж; Гренада; Зарубеж; Зарубеж; Гренландия; Зарубеж; Зарубеж; Греция; Зарубеж; Зарубеж; Грузия; Зарубеж; Гуам; Зарубеж; Зарубеж; Гуйяна; Зарубеж; Зарубеж; Дания; Зарубеж; Зарубеж; Джибуту; Зарубеж; Зарубеж; Доминиканская Республика; Зарубеж; Зарубеж; Доминикия; Зарубеж; Зарубеж; Египет; Зарубеж; Зарубеж; Заир; Зарубеж; Зарубеж; Замбия; Зарубеж; Зарубеж; Западная Сахара; Зарубеж; Зарубеж; Зимбабве; Зарубеж; Зарубеж; Израиль; Зарубеж; Зарубеж; Индия; Зарубеж; Зарубеж; Индонезия; Зарубеж; Зарубеж; Иордан; Зарубеж; Зарубеж; Ирак; Зарубеж; Зарубеж; Иран; Зарубеж; Зарубеж; Ирландия; Зарубеж; Зарубеж; Исландия; Зарубеж; Зарубеж; Испания; Зарубеж; Зарубеж; Италия; Зарубеж; Зарубеж; Йемен; Зарубеж; Зарубеж; Каймановы Острова; Зарубеж; Зарубеж; Камбоджа; Зарубеж; Зарубеж; Камерун; Зарубеж; Зарубеж; Канада; Зарубеж; Зарубеж; Капе Верде; Зарубеж; Зарубеж; Катар; Зарубеж; Зарубеж; Кения; Зарубеж; Зарубеж; Кипр; Зарубеж; Зарубеж; Кирибати; Зарубеж; Зарубеж; Китай; Зарубеж; Зарубеж; Кокос (Килевы Острова); Зарубеж; Зарубеж; Колумбия; Зарубеж; Зарубеж; Коморос; Зарубеж; Зарубеж; Конго; Зарубеж; Зарубеж; Коста-Рика; Зарубеж; Зарубеж; Кот Ди Вуар (о.Слоновой Кости); Зарубеж; Зарубеж; Куба; Зарубеж; Зарубеж; Кувейт; Зарубеж; Зарубеж; Кыргызстан; Зарубеж; Зарубеж; Лаос; Зарубеж; Зарубеж; Латвия; Зарубеж; Зарубеж; Лебанон; Зарубеж; Зарубеж; Лесото; Зарубеж; Зарубеж; Либерия; Зарубеж; Зарубеж; Либия; Зарубеж; Зарубеж; Лизуания; Зарубеж; Зарубеж; Литва; Зарубеж; Зарубеж; Лихтенштейн; Зарубеж; Зарубеж; Люксембург; Зарубеж; Зарубеж; Маврикий; Зарубеж; Зарубеж; Мавритания; Зарубеж; Зарубеж; Мадагаскар; Зарубеж; Зарубеж; Майотте; Зарубеж; Зарубеж; Макау; Зарубеж; Зарубеж; Македония; Зарубеж; Зарубеж; Малавия; Зарубеж; Зарубеж; Малайзия; Зарубеж; Зарубеж; Малайзия; Зарубеж; Зарубеж; Малдивы; Зарубеж; Зарубеж; Мали; Зарубеж; Зарубеж; Мальта; Зарубеж; Зарубеж; Мантигуа; Зарубеж; Зарубеж; Маршалловы Острова; Зарубеж; Зарубеж; Мауритиус; Зарубеж; Зарубеж; Маянмар; Зарубеж; Зарубеж; Мексика; Зарубеж; Зарубеж; Мозамбик; Зарубеж; Зарубеж; Молдова; Зарубеж; Зарубеж; Монако; Зарубеж; Зарубеж; Монголия; Зарубеж; Зарубеж; Монсеррат; Зарубеж; Зарубеж; Морокко; Зарубеж; Зарубеж; Намибия; Зарубеж; Зарубеж; Науру; Зарубеж; Зарубеж; Незерландские Антиллы; Зарубеж; Зарубеж; Незначительно отдаленные острова США; Зарубеж; Зарубеж; Нейтральная зона (Саудовская Аравия/Ирак); Зарубеж; Зарубеж; Непал; Зарубеж; Зарубеж; Нигер; Зарубеж; Зарубеж; Нигерия; Зарубеж; Зарубеж; Нидерланды; Зарубеж; Зарубеж; Никарагуа; Зарубеж; Зарубеж; Ниу; Зарубеж; Зарубеж; Новая Зеландия; Зарубеж; Зарубеж; Новая Каледония; Зарубеж; Зарубеж; Норвегия; Зарубеж; Зарубеж; Норфлокские Острова; Зарубеж; Зарубеж; ОАЭ; Зарубеж; Зарубеж; Оман; Зарубеж; Зарубеж; Остров Боувет; Зарубеж; Зарубеж; Острова Валлис и Футуна; Зарубеж; Зарубеж; Острова Кука; Зарубеж; Зарубеж; Острова Свалбард и Жан Маньен; Зарубеж; Зарубеж; Острова Турецкие и Каикос; Зарубеж; Зарубеж; Острова Форое; Зарубеж; Зарубеж; Острова Хеард и Макдональд; Зарубеж; Зарубеж; Острова Христа; Зарубеж; Зарубеж; Пакистан; Зарубеж; Зарубеж; Палау; Зарубеж; Зарубеж; Панама; Зарубеж; Зарубеж; Папуа Новая Гвинея; Зарубеж; Зарубеж; Парагвай; Зарубеж; Зарубеж; Перу; Зарубеж; Зарубеж; Питкайрн; Зарубеж; Зарубеж; Польша; Зарубеж; Зарубеж; Португалия; Зарубеж; Зарубеж; Пуэрто Рико; Зарубеж; Зарубеж; Реюньон; Зарубеж; Зарубеж; Российская Федерация; Зарубеж; Зарубеж; Руанда; Зарубеж; Зарубеж; Румыния; Зарубеж; Зарубеж; Самоа; Зарубеж; Зарубеж; Сан-Марино; Зарубеж; Зарубеж; Сан-Сальвадор; Зарубеж; Зарубеж; Сант Китс и Левис; Зарубеж; Зарубеж; Сант Люсия; Зарубеж; Зарубеж; Сан-Томе и Принципе; Зарубеж; Зарубеж; Саудовская Аравия; Зарубеж; Зарубеж; Св. Елена; Зарубеж; Зарубеж; Св. Прьерре и Микьелон; Зарубеж; Зарубеж; Свазиленд; Зарубеж; Зарубеж; Святая Джорджия и Сандвичевы Острова; Зарубеж; Зарубеж; Северная Корея; Зарубеж; Зарубеж; Сейшеллы; Зарубеж; Зарубеж; Сенегал; Зарубеж; Зарубеж; Сербия; Зарубеж; Зарубеж; Сингапур; Зарубеж; Зарубеж; Сирия; Зарубеж; Зарубеж; Словакия; Зарубеж; Зарубеж; Словения; Зарубеж; Зарубеж; Снт Винсент и Гранат; Зарубеж; Зарубеж; Советский Союз (формальный); Зарубеж; Зарубеж; Соломоновы острова; Зарубеж; Зарубеж; Сомали; Зарубеж; Зарубеж; Судан; Зарубеж; Зарубеж; Суринам; Зарубеж; Зарубеж; США; Зарубеж; Зарубеж; Сьерра Леоне; Зарубеж; Зарубеж; Таджикистан; Зарубеж; Зарубеж; Таиланд; Зарубеж; Зарубеж; Тайвань; Зарубеж; Зарубеж; Танзания; Зарубеж; Зарубеж; Того; Зарубеж; Зарубеж; Токелау; Зарубеж; Зарубеж; Тонга; Зарубеж; Зарубеж; Тринидад и Тобаго; Зарубеж; Зарубеж; Тувалу; Зарубеж; Зарубеж; Тунис; Зарубеж; Зарубеж; Туркменистан; Зарубеж; Зарубеж; Турция; Зарубеж; Зарубеж; Уганда; Зарубеж; Зарубеж; Узбекистан; Зарубеж; Зарубеж; Украина; Зарубеж; Зарубеж; Уругвай; Зарубеж; Зарубеж; Фалклендские Острова (Малвинас); Зарубеж; Зарубеж; Фиджи; Зарубеж; Зарубеж; Финляндия; Зарубеж; Зарубеж; Флипины; Зарубеж; Зарубеж; Франция; Зарубеж; Зарубеж; Французкие Метрополии; Зарубеж; Зарубеж; Французская Гуана; Зарубеж; Зарубеж; Французская Полинезия; Зарубеж; Зарубеж; Хайти; Зарубеж; Зарубеж; Хорватия; Зарубеж; Зарубеж; Центральная Гвинея; Зарубеж; Зарубеж; Центрально -Африканская Республика; Зарубеж; Зарубеж; Чад; Зарубеж; Зарубеж; Черногория; Зарубеж; Зарубеж; Чехия; Зарубеж; Зарубеж; Чили; Зарубеж; Зарубеж; Швейцария; Зарубеж; Зарубеж; Швеция; Зарубеж; Зарубеж; Шри Ланка; Зарубеж; Зарубеж; Эквадор; Зарубеж; Зарубеж; Эритрея; Зарубеж; Зарубеж; Эстония; Зарубеж; Зарубеж; Эфиопия; Зарубеж; Зарубеж; Югославия; Зарубеж; Зарубеж; Южная Африка; Зарубеж; Зарубеж; Южная Корея; Зарубеж; Зарубеж; Южные Марианские Острова; Зарубеж; Зарубеж; Южные Французские территории; Зарубеж; Зарубеж; Ямайка; Зарубеж; Зарубеж; Япония; Зарубеж; Зарубеж",
    "11818,11818185,11818184,11818186,11818187,11818188,11818190,11818192,11818183,11818182,11818198,11818199,11801,11801003,11801004,11801005,11801006,11801009,11801007,11801019,11801008,11801010,11801011,11801012,11801013,11801014,11801001,11801015,11801020,11801016,11801002,11801017,11801018,11802,11802022,11802033,11802034,11802021,11802023,11802032,11802024,11802026,11802027,11802029,11802028,11802020,11802025,11802030,11802031,11803,11803038,11803039,11803040,11803051,11803044,11803052,11803034,11803046,11803048,11803050,11803036,11803037,11803049,11803043,11803041,11803042,11803045,11803047,11803033,11803035,11816,11816208,11816201,11816204,11816206,11816207,11816202,1181609,11816205,11804,11804052,11804053,11804054,11804055,11804057,11804056,11804058,11804059,11814,11814180,11814189,11814191,11814195,11814194,11814193,11814179,11814196,11814197,11814185,11814184,11814186,11814187,11814188,11814190,11814192,11814183,11814182,11814198,11814181,11814203,11814204,11806,11806074,11806075,11806076,11806077,11806079,11806080,11806081,11806082,11806073,11806078,11806083": "область Абай; Абайский район; Аягоз г.а.; Аягозский район; Бескарагайский район; Бородулихинский район; Жарминский район; Кокпектинский район; Курчатов г.а.; Семей г.а.; Урджарский район; район Аксуат; Акмолинская область; Аккольский район; Аршалынский район; Астраханский район; Атбасарский район; Биржан сал район; Буландынский район; Бурабайский район; Егиндыкольский район; Ерейментауский район; Есильский район; Жаксынский район; Жаркаинский район; Зерендинский район; Кокшетау г.а.; Коргалжынский район; Косшы г.а.; Сандыктауский район; Степногорск г.а.; Целиноградский район; Шортандинский район; Актюбинская область; Айтекебийский район; Актобе г.а. - район Алматы; Актобе г.а. - район Астана; Алгинский район; Байганинский район; Иргизский район; Каргалинский район; Мартукский район; Мугалжарский район; Темирский район; Уилский район; УСТАРЕВШЕЕ - Актобе г.а.; Хобдинский район; Хромтауский район; Шалкарский район; Алматинская область; Балхашский район; Енбекшиказахский район; Жамбылский район; Илийский район; Карасайский район; Кегенский район; Конаев г.а.; Райымбекский район; Талгарский район; Уйгурский район; УСТАРЕВШЕЕ - Аксуский район; УСТАРЕВШЕЕ - Алакольский район; УСТАРЕВШЕЕ - Ескельдинский район; УСТАРЕВШЕЕ - Каратальский район; УСТАРЕВШЕЕ - Кербулакский район; УСТАРЕВШЕЕ - Коксуский район; УСТАРЕВШЕЕ - Панфиловский район; УСТАРЕВШЕЕ - Саркандский район; УСТАРЕВШЕЕ - Талдыкорган г.а.; УСТАРЕВШЕЕ - Текели г.а.; Алматы г.а.; Алатауский р. а.; Алмалинская р.а.; Ауэзовская р.а.; Бостандыкская р.а.; Жетысуская р.а.; Медеуская р.а.; Наурызбайский р.а.; Турксибский р.а.; Атырауская область; Атырау г.а.; Жылыойский район; Индерский район; Исатайский район; Кзылкогинский район; Курмангазинский район; Макатский район; Махамбетский район; Восточно-Казахстанская область; Алтай г.а.; Глубоковский район; Зайсанский район; Катон-Карагайский район; Курчумский район; район Алтай; Риддер г.а.; Тарбагатайский район; Уланский район; УСТАРЕВШЕЕ - Абайский район; УСТАРЕВШЕЕ - Аягоз г.а.; УСТАРЕВШЕЕ - Аягозский район; УСТАРЕВШЕЕ - Бескарагайский район; УСТАРЕВШЕЕ - Бородулихинский район; УСТАРЕВШЕЕ - Жарминский район; УСТАРЕВШЕЕ - Кокпектинский район; УСТАРЕВШЕЕ - Курчатов г.а.; УСТАРЕВШЕЕ - Семей г.а.; УСТАРЕВШЕЕ - Урджарский район; Усть-Каменогорск г.а.; Шемонаихинский район; район Самар; Жамбылская область; Байзакский район; Жамбылский район; Жуалынский район; Кордайский район; Меркенский район; Мойынкумский район; Сарысуский район; Таласский район; Тараз г.а.; Турар Рыскуловский район; Шуский район"
}
errors = (ProxyError, MaxRetryError, SSLError, ConnectionError, ReadTimeout)
company_fieldnames = ['Идентификатор', 'БИН', 'РНН', 'ОКПО', 'Наименование (рус. яз)', 'Наименование (каз. яз)', 'ОПФ',
                      'КФС (уровень 4)', 'КФС', '№ госрегистрации', 'Дата госрегистрации',
                      'Дата первичной госрегистрации', 'Статус', 'Блокировка', 'Орган гос.управления', 'Собственник',
                      'Отрасль (уровень 1)', 'Отрасль (уровень 4)', 'company_id', 'contact_id']
contact_fieldnames = ['Идентификатор', 'БИН', 'РНН', 'ОКПО', 'Наименование (рус. яз)', 'Первый руководитель',
                      'Главный бухгалтер', 'Страна', 'Индекс', 'Область', 'Регион', 'Нас. пункт, дом, кв.', 'Телефон',
                      'Факс', 'e-mail', 'Веб-сайт', 'company_id', 'contact_id']
gosreestrkz_company_url = 'https://gr5.gosreestr.kz/p/ru/GrObjects/objects/teaser-view/{}?OptionName=BlockGrObjectsExtraInformation'
gosreestrkz_contact_url = "https://gr5.gosreestr.kz/p/ru/GrObjects/objects/teaser-view/{}?flGlobalObjectId={}&OptionName=Contacts"


class ProxyFactory:
    user = luigi.Parameter(default=PROXY_FACTORY_USER, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=PROXY_FACTORY_PASS, visibility=ParameterVisibility.HIDDEN)
    _proxies = deque()
    _base_address = "gate.smartproxy.com"

    def __init__(self):
        ports = range(10000, 10099)

        for port in ports:
            _p = f"http://{self.user}:{self.password}@{self._base_address}:{port}"
            self._proxies.append(_p)

    def get(self):
        p = self._proxies.pop()
        self._proxies.appendleft(p)
        return p


class IdsManager:
    def __init__(self, ids_fpath, output_fpath, parsed_fpath):
        self.failed_ids = deque([])
        self.output_fpath = output_fpath

        parsed_ids = []
        if os.path.exists(parsed_fpath):
            parsed_ids = read_csv_tuples(parsed_fpath)

        self._parsed_ids_count = len(parsed_ids)

        source_ids = read_csv_tuples(ids_fpath)
        self._source_ids_count = len(source_ids)

        # excluding parsed ids
        if parsed_ids:
            s = set(source_ids)
            s.difference_update(set(parsed_ids))
            self.ids = deque(list(s))
        else:
            self.ids = deque(source_ids)

    @property
    def total(self):
        return self._source_ids_count

    @property
    def parsed(self):
        return self._parsed_ids_count

    def status_info(self, ids, stat=None):
        s = f'Total: {self._source_ids_count}. Parsed: {self._parsed_ids_count}.' + '\n'
        s += f'Parsing payments on {ids} in {self.output_fpath}.' + '\n'
        s += stat
        return s


class GosreestrKzCompanyOutput(ApiToCsv):

    all_data = luigi.Parameter(default=False)
    ftp_file_mask = luigi.Parameter(visibility=ParameterVisibility.HIDDEN)
    from_to = luigi.TupleParameter(default=())
    timeout = luigi.FloatParameter(default=1.5)
    timeout_ban = luigi.FloatParameter(default=5.0)

    @property
    def dates_params(self):
        params = dict()
        params['date_from'], params['date_to'] = self.from_to
        return params

    @property
    def ids_fpath(self):
        return self._file_path('.ids')

    @property
    def failed_fpath(self):
        return self._file_path('.failed')

    def requires(self):
        return ExternalFtpCsvDFInput(ftp_file_mask=self.ftp_file_mask)

    def output(self):
        return [luigi.LocalTarget(self.parsed_ids_fpath),
                super().output()
                ]

    @property
    def bins_list(self):
        bins = []
        date_from= self.dates_params["date_from"]
        date_to = self.dates_params["date_to"]
        date_from_format = datetime.strptime(date_from, DEFAULT_FORMAT)
        date_to_format = datetime.strptime(date_to, DEFAULT_FORMAT)
        current_date = date_from_format
        while current_date <= date_to_format:
            bins.append(current_date.strftime("%y%m"))
            current_date += timedelta(days=31)  # Прибавляем количество дней, достаточное для перехода к следующему месяцу
            current_date = current_date.replace(day=1)
        return bins

    def run(self):
        if not os.path.exists(self.ids_fpath):
            self.input().get(str(self.ids_fpath))

        bins_list = self.bins_list
        parser = GosreestrKzRequests(base_url, bins_list)
        company_data_dict = parser.get_all_bins_json
        company_tuples = list(
            zip(company_data_dict['bin'], company_data_dict['company_id'], company_data_dict['contact_id']))
        company_deque = deque(company_tuples)

        ids_manager = IdsManager(
            self.ids_fpath,
            self.output_fpath,
            self.parsed_ids_fpath
        )

        if not self.all_data:
            ids = ids_manager.ids
            company_deque.extend(ids)

        parsed_cnt = ids_manager.parsed
        failed_ids = deque()
        length = len(company_deque)

        # Счетчик попыток для каждого идентификатора
        attempt_counts = defaultdict(int)
        max_attempts = 5  # Максимальное количество попыток для каждого идентификатора

        while company_deque:
            if failed_ids:
                _id = failed_ids.popleft()
            else:
                _id = company_deque.popleft()

            try:
                bin_id, company_id, contact_id = _id
                print(f'BIN: {bin_id}. Company_ID: {company_id}. Contact_ID: {contact_id}')
                parser = GosreestrKzRequests(gosreestrkz_company_url.format(company_id))
                company_data = parser.process_company_id(company_id, contact_id)

            except errors:
                attempt_counts[_id] += 1
                if attempt_counts[_id] < max_attempts:
                    failed_ids.append(_id)
                else:
                    # Логировать проблемные ID и не добавлять их обратно
                    logging.error(f"Max attempts reached for bin: {bin_id}")
                sleep(self.timeout)

            else:
                data = dict_to_row(company_data, self.struct)
                save_csvrows(self.output_fpath, [data], delimiter=';')

                append_file_tuple(self.parsed_ids_fpath, (company_id, contact_id))
                parsed_cnt += 1

            s = f'Total: {length}. Parsed: {parsed_cnt}. BIN: {_id[0]}. Company_ID: {_id[1]}. Contact_ID: {_id[2]}' + '\n'
            stat = {'total': length, 'parsed': parsed_cnt}
            rewrite_file(self.stat_fpath, json.dumps(stat))

            p = floor((parsed_cnt * 100) / length)
            self.set_status_info(s, p)

        self.finalize()


@requires(GosreestrKzCompanyOutput)
class GosreestrKzCompanyFtpUploadedOutput(FtpUploadedOutput):

    def file_name(self, input_fpath):
        tomorrow = datetime.today() + timedelta(days=1)
        suff_tomorrow = '{date:%Y%m%d}'.format(date=tomorrow)
        ext = Path(input_fpath).suffix

        # have to break it down to pieces to get file name without date
        pieces = Path(input_fpath).stem.split('_')
        pieces.pop()
        pieces.append(suff_tomorrow)
        f_name = '_'.join(pieces)
        return Path(f_name).with_suffix(ext + self.gzip_ext).name

    def gzip_file(self, input_fpath):

        gzip_fpath = os.path.join(os.path.dirname(os.path.abspath(input_fpath)),
                                  self.file_name(input_fpath))

        with open(input_fpath, 'rb') as src:
            with gzip.open(gzip_fpath, 'wb') as dest:
                shutil.copyfileobj(src, dest)

        return gzip_fpath

    def output(self):

        os_sep = str(self.ftp_os_sep)
        root = self.ftp_path

        # use str.sep.join to avoid problems
        # OS specific separator
        if self.ftp_directory:
            path = os_sep.join([root, self.ftp_directory])
        else:
            path = root

        ftp_remote_targets = []
        for fi in self.input():
            ftp_fpath = os_sep.join([path, self.file_name(fi.path)])
            ftp_remote_targets.append(RemoteTarget(
                ftp_fpath,
                self.ftp_host,
                username=self.ftp_user,
                password=self.ftp_pass)
            )

        return ftp_remote_targets

    def run(self):
        for i, fi in enumerate(self.input()):
            fpath = self.gzip_file(fi.path)
            self.output()[i].put(fpath, atomic=False)


class GosreestrKzCompany(Runner):

    name = luigi.Parameter(default='gosreestrkz_company')
    start_date = luigi.DateParameter(default=first_day_of_previous_month())
    end_date = luigi.DateParameter(default=last_day_of_previous_month())
    all_data = luigi.Parameter(default=False)

    def params(self):

        params = super(GosreestrKzCompany, self).params
        if self.all_data:
            start_year = 1900 + int(datetime.now().strftime("%y")) + 1
            start_date = datetime(start_year, 1, 1)
            end_date = datetime(datetime.now().year, datetime.now().month, 1) - timedelta(days=1)
            params['from_to'] = (
                start_date.isoformat(),
                end_date.isoformat()
            )
        else:
            params['from_to'] = (
                self.start_date.isoformat(),
                self.end_date.isoformat()
            )
        return params

    def requires(self):
        return GosreestrKzCompanyFtpUploadedOutput(
            **self.params()
        )


class GosreestrKzContactOutput(ApiToCsv):

    all_data = luigi.Parameter(default=False)
    ftp_file_mask = luigi.Parameter(visibility=ParameterVisibility.HIDDEN)
    from_to = luigi.TupleParameter(default=())
    timeout = luigi.FloatParameter(default=1.5)
    timeout_ban = luigi.FloatParameter(default=5.0)

    @property
    def dates_params(self):
        params = dict()
        params['date_from'], params['date_to'] = self.from_to
        return params

    @property
    def ids_fpath(self):
        return self._file_path('.ids')

    @property
    def failed_fpath(self):
        return self._file_path('.failed')

    def requires(self):
        return ExternalFtpCsvDFInput(ftp_file_mask=self.ftp_file_mask)

    def output(self):
        return [luigi.LocalTarget(self.parsed_ids_fpath),
                super().output()]

    @property
    def bins_list(self):
        bins = []
        date_from = self.dates_params["date_from"]
        date_to = self.dates_params["date_to"]
        date_from_format = datetime.strptime(date_from, DEFAULT_FORMAT)
        date_to_format = datetime.strptime(date_to, DEFAULT_FORMAT)
        current_date = date_from_format
        while current_date <= date_to_format:
            bins.append(current_date.strftime("%y%m"))
            current_date += timedelta(
                days=31)  # Прибавляем количество дней, достаточное для перехода к следующему месяцу
            current_date = current_date.replace(day=1)
        return bins

    def run(self):
        if not os.path.exists(self.ids_fpath):
            self.input().get(str(self.ids_fpath))

        bins_list = self.bins_list
        parser = GosreestrKzRequests(base_url, bins_list)
        contact_data_dict = parser.get_all_bins_json
        contact_tuples = list(
            zip(contact_data_dict['bin'], contact_data_dict['company_id'], contact_data_dict['contact_id']))
        contact_deque = deque(contact_tuples)

        ids_manager = IdsManager(
            self.ids_fpath,
            self.output_fpath,
            self.parsed_ids_fpath
        )

        if not self.all_data:
            ids = ids_manager.ids
            contact_deque.extend(ids)

        failed_ids = deque()
        parsed_cnt = ids_manager.parsed
        length = len(contact_deque)

        # Счетчик попыток для каждого идентификатора
        attempt_counts = defaultdict(int)
        max_attempts = 5  # Максимальное количество попыток для каждого идентификатора

        while contact_deque:
            if failed_ids:
                _id = failed_ids.popleft()
            else:
                _id = contact_deque.popleft()

            try:
                bin_id, company_id, contact_id = _id
                parser = GosreestrKzRequests(gosreestrkz_contact_url.format(company_id, contact_id))
                contact_data = parser.process_contact_id(company_id, contact_id)

            except errors:
                attempt_counts[_id] += 1
                if attempt_counts[_id] < max_attempts:
                    failed_ids.append(_id)
                else:
                    # Логировать проблемные ID и не добавлять их обратно
                    logging.error(f"Max attempts reached for ID {_id}")
                sleep(self.timeout)

            else:
                data = dict_to_row(contact_data, self.struct)
                save_csvrows(self.output_fpath, [data], delimiter=';')

                append_file_tuple(self.parsed_ids_fpath, (company_id, contact_id))
                parsed_cnt += 1

            s = f'Total: {length}. Parsed: {parsed_cnt}. BIN: {_id[0]}. Company_ID: {_id[1]}. Contact_ID: {_id[2]}' + '\n'
            stat = {'total': length, 'parsed': parsed_cnt}
            rewrite_file(self.stat_fpath, json.dumps(stat))

            p = floor((parsed_cnt * 100) / length)
            self.set_status_info(s, p)

        self.finalize()


@requires(GosreestrKzContactOutput)
class GosreestrKzContactFtpUploadedOutput(FtpUploadedOutput):

    def file_name(self, input_fpath):
        tomorrow = datetime.today() + timedelta(days=1)
        suff_tomorrow = '{date:%Y%m%d}'.format(date=tomorrow)
        ext = Path(input_fpath).suffix

        # have to break it down to pieces to get file name without date
        pieces = Path(input_fpath).stem.split('_')
        pieces.pop()
        pieces.append(suff_tomorrow)
        f_name = '_'.join(pieces)
        return Path(f_name).with_suffix(ext + self.gzip_ext).name

    def gzip_file(self, input_fpath):

        gzip_fpath = os.path.join(os.path.dirname(os.path.abspath(input_fpath)),
                                  self.file_name(input_fpath))

        with open(input_fpath, 'rb') as src:
            with gzip.open(gzip_fpath, 'wb') as dest:
                shutil.copyfileobj(src, dest)

        return gzip_fpath

    def output(self):

        os_sep = str(self.ftp_os_sep)
        root = self.ftp_path

        # use str.sep.join to avoid problems
        # OS specific separator
        if self.ftp_directory:
            path = os_sep.join([root, self.ftp_directory])
        else:
            path = root

        ftp_remote_targets = []
        for fi in self.input():
            ftp_fpath = os_sep.join([path, self.file_name(fi.path)])
            ftp_remote_targets.append(RemoteTarget(
                ftp_fpath,
                self.ftp_host,
                username=self.ftp_user,
                password=self.ftp_pass)
            )

        return ftp_remote_targets

    def run(self):
        for i, fi in enumerate(self.input()):
            fpath = self.gzip_file(fi.path)
            self.output()[i].put(fpath, atomic=False)


class GosreestrKzContact(Runner):
    name = luigi.Parameter(default='gosreestrkz_contact')
    start_date = luigi.DateParameter(default=first_day_of_previous_month())
    end_date = luigi.DateParameter(default=last_day_of_previous_month())
    all_data = luigi.Parameter(default=False)

    def params(self):

        params = super(GosreestrKzContact, self).params
        if self.all_data:
            start_year = 1900 + int(datetime.now().strftime("%y")) + 1
            start_date = datetime(start_year, 1, 1)
            end_date = datetime(datetime.now().year, datetime.now().month, 1) - timedelta(days=1)
            params['from_to'] = (
                start_date.isoformat(),
                end_date.isoformat()
            )
        else:
            params['from_to'] = (
                self.start_date.isoformat(),
                self.end_date.isoformat()
            )
        return params

    def requires(self):
        return GosreestrKzContactFtpUploadedOutput(
            **self.params()
        )


if __name__ == '__main__':
    luigi.run()
