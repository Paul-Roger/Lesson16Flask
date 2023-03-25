import ParserNewsAtoRu
from datetime import date
import os
from flask import Flask, render_template, request, flash, redirect
import csv
import sqlite3

#Constants
DefDateStr = "2023-03-01"
DefSearchStr = "Mercedes"
FileName = 'resultfile'
file_name = str(FileName) + ".csv"
keyword = ''

#Global flag
req_act = False

app = Flask(__name__) #, static_folder='/static'
#app._static_folder = '/static' #app._static_folder = 'templates/static'
app.config['SECRET_KEY'] = 'a9l11t2v8w4l6e5g4nn9u4g6'

@app.route("/")
def index():
    site_info = {
        'site_str': 'News.auto.ru search',
        'title_str': 'Поиск на News.auto.ru'
    }
    return render_template('index.html', **site_info)


@app.route('/contacts/')
def contacts():
    developer_name = 'Paul Roger'
    return render_template('about.html', name=developer_name, creation_date='10.03.2023')


@app.route('/search/', methods=['GET'])
def search_get():
    global req_act
    print("search-GET", req_act)
    if req_act:
        print("busy, No Results")
        return render_template('noresults.html', info_msg = 'Поиск недоступен, поскольку идёт обработка результатов предыдущего поиска')
    else:
        print("Open search GET")
        # Подключение к базе данных
        conn = sqlite3.connect('AutoDB.sqlite')
        # Создаем курсор
        cursor = conn.cursor()
        cursor.execute('select BrandName from AutoBrand order by NoOfSearches desc Limit 15')
        result = cursor.fetchall()
        brand_list = []
        for d in result:
            brand_list.append(d[0])
        conn.close()
        return render_template('search.html', brand_list = brand_list)

@app.route('/search/', methods=['POST'])
def search_post():
    # Как получть данные формы
    global req_act, keyword
    print("search-PUT", req_act)
    if req_act:
        print("busy, No Results")
        return render_template('noresults.html', info_msg = 'Поиск недоступен, пока идёт обработка результатов предыдущего поиска')
    req_auto = request.form['req_auto']
    req_keyword = request.form['req_keyword']
    req_date = request.form['req_date']
    print(req_auto, req_keyword, req_date)
    if len(req_keyword)<3 and len(req_auto)<3:
        print("No data entered, No Results")
        return render_template('noresults.html', info_msg = 'Поиск не может быть произведен - неверные данные для поиска')

    if len(req_keyword)>=3:
        keyword = req_keyword
    else:
        keyword = req_auto

    try:
        str_startdate = req_date
        startdate = date.fromisoformat(req_date)
    except:
        print(f"неверный формат даты, выбрана {DefDateStr} по умолчанию")
        str_startdate = DefDateStr

    flash('Ваш запрос принят, обрабтка занимает длительное время. Ожидайте результата')
    # Подключение к базе данных
    conn = sqlite3.connect('AutoDB.sqlite')
    # Создаем курсор
    cursor = conn.cursor()
    search_templ = keyword + '%'
    print('search', search_templ)
    cursor.execute('select * from AutoBrand where BrandName Like ?', (search_templ,))
    result = cursor.fetchone()
    print(result)
#clear search results
    cursor.execute('delete from SearchResult where BrandID = ?', (result[0], ))
    conn.commit()
    conn.close()

    req_act = True
    parser_result = 0
    print("parser call")
###    render_template('search.html')
    parser_result = ParserNewsAtoRu.parser(FileName, keyword, str_startdate)
    # print("Parser Call")
    req_act = False
    if parser_result > 0:
        return redirect('/results/')
    else:
        return render_template('noresults.html', info_msg = 'Не найдены данные соотествующие критериям поиска')


@app.route('/results/')
def results():
    global req_act
    global keyword
    print("result", req_act)
    if req_act:
        print("busy, No Results")
        return render_template('noresults.html',info_msg='Результаты пока недостуаны, поскольку идёт обработка результатов поиска')
    db_rows = []
    # Подключение к базе данных
    conn = sqlite3.connect('AutoDB.sqlite')
    # Создаем курсор
    cursor = conn.cursor()
    search_templ = keyword + '%'
    print("search_templ = ", search_templ)
    cursor.execute('select * from AutoBrand where BrandName Like ?', (search_templ,))
    result = cursor.fetchone()
    if result != None:
        cursor.execute('select Title, PubDate, Link, ShortText from SearchResult where BrandID = ?', (result[0],))
        db_rows = cursor.fetchall()
        print(db_rows)
        conn.close()
        print(db_rows)
        header = ["Заголовок", "Дата", "Ссылка", "Начало статьи"]
        return render_template("results.html", header=header, rows=db_rows)
        """   if os.path.exists(file_name):
        print("File found - Results")
        with open("resultfile.csv", encoding='utf-8-sig', newline='') as file:
        reader = csv.reader(file, delimiter=';', quotechar='"')
        header = next(reader)"""

    else:
        print("No File - No Results")
        return render_template('noresults.html',info_msg='Результаты недостуаны, что-то пошло не так')


if __name__ == "__main__":
    app.run(debug=True)

########################################


