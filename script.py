import requests
from bs4 import BeautifulSoup
import re
import json

articules = open('LandRover.txt') #файл с артикулами

monthsRus = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
monthsEng = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

date = ''

for j, articule in enumerate(articules.readlines()):
	articule = articule.replace('\n', '') #убирает лишние переносы

	#получает json обхект, содержаший инфу о товаре и поставщиках
	r = requests.get('https://emex.ru/api/search/search?detailNum=' + articule + '&make=Land%2BRover&latitude=55.753960&longitude=37.620393&showAll=false')
	r.encoding = 'utf-8'

	data = json.loads(r.text)

	if 'points' in data['searchResult']: #проверяет есть ли артикул на сайте
		for i, l in enumerate(data['searchResult']['points']['list']):
			r = requests.get('https://emex.ru/products/' + articule + '/Land+Rover/' + str(l['locationId'])) #запрашивает страницу с товаром
			r.encoding = 'utf-8'

			soup = BeautifulSoup(r.text, features="lxml")

			articulClassRegex = re.compile('ProductDescription__ProductMakerAndDetailNumber.*') #поиск инфы о товаре через обращение к соотвествующему классу
			articulFromPage = soup.find('span', {'class': articulClassRegex}).find('a').getText()

			manufacturerClassRegex = re.compile('ProductDescription__ProductMakerAndDetailNumber.*')
			manufacturer = soup.find('span', {'class': manufacturerClassRegex}).find('span').getText()

			nameClassRegex = re.compile('ProductDescription__DetailDescription.*')
			name = soup.find('span', {'class': nameClassRegex}).getText()

			countClassRegex = re.compile('ProductTableItem__QuantityWrapper.*')
			count = re.match(r'\d*', soup.find('div', {'class': countClassRegex}).getText()).group(0)

			dillerClassRegex = re.compile('ProductTooltip__Wrapper')
			diller = soup.find('div', {'class': dillerClassRegex}).find('h2').getText()

			deliveryClassRegex = re.compile('ProductTableItem__DeliveryWrapper')
			delivery = re.match(r'\d*', soup.find('div', {'class': deliveryClassRegex}).getText()).group(0)

			priceClassRegex = re.compile('ProductTableItem__PriceWrapper')
			price = re.match(r'\d*', soup.find('div', {'class': priceClassRegex}).getText()).group(0)

			dateClassRegex = re.compile('ProductTooltip__DateContent')
			dateUpdate = soup.find('span', {'class': dateClassRegex}).getText().split(' ')

			if dateUpdate[2] in monthsRus: #название месяца может быть на английском и на русском
				num = str(monthsRus.index(dateUpdate[2]) + 1)

				if len(num) == 1:
					num = '0' + num

				date = dateUpdate[1] + '.' + num + '.2020' #возвращает доту добавления товара (год поменять по необходиости)

			if dateUpdate[2] in monthsEng:
				num = str(monthsEng.index(dateUpdate[2]) + 1)

				if len(num) == 1:
					num = '0' + num

				date = dateUpdate[1] + '.' + num + '.2020'

			#формирует строку таблицы
			row = str(articule) + ',' + articulFromPage + ',' + name + ',' + url + ',' + manufacturer + ',' + count + ',' + diller + ',' + delivery + ',' + price + ',' + date

			#вывод прогресса
			print('Артикль: ' + str(j + 1) + '(' + articule + ')' + ', элемент: ' + str(i + 1) + '/' + str(len(data['searchResult']['points']['list'])))

			#открывает файл на дозапись и записывает строку
			f = open('LandRover.csv', 'a')
			f.write(row + '\n')
			f.close()
	else: #на случай если артикула нет
		row = str(articule) + '\t999999\t999999\t999999\t999999\t0'
		f = open('LandRover.csv', 'a')
		f.write(row + '\n')
		f.close()