### Для начала
```pip install beautifulsoup4```

В данном проекте нет кода, в котором используется прокси, т.к. он остался на сервера, к которому уже нет доступа

### Принцип работы

Тут всё просто:
1. Делается запрос `https://emex.ru/api/search/search?detailNum=' + articule + '&make=Land%2BRover&latitude=55.753960&longitude=37.620393&showAll=false` который возращает json
2. Из json вытаскивается `['searchResult']['points']['list']`, содержащий список id страниц поставщиков
3. Цикл проходит все страницы поставщиков и вытаскивает от туда html
4. BeautifulSoup4 через регулярку дёргает классы, в которых содержится вся необходимая инфа
5. Инфа записывается в строку с разделителем `,`
6. Строка дозаписывается в csv