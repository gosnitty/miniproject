from flask import Flask, render_template, request
import pandas as pd
import random

def choosed_categories(path, name):
    '''
    returns data only certain categories
    '''
    caregories_data = {
        'Drama': 'Anime.csv,Films.csv, Books.csv, Netflix.csv',
        'Thriller': 'Films.csv',
        'Comedy': 'Films.csv, Anime.csv, Netflix.csv, Manga.csv',
        'Romance': 'Films.csv, Anime.csv, Manga.csv',
        'Fiction': 'Books.csv',
        'Philosophy': 'Books.csv',
        'Action': 'Anime.csv',
        'Detective': 'Books.csv',
        'School Life': 'Manga.csv',
        'Children & Family': 'Netflix.csv'
    }
    for key, value in caregories_data.items():
        if name == key and path in value:
            dfr = pd.read_csv(path)
            dfr = dfr.dropna(subset=['categories'], inplace=False)
            dfr = dfr[dfr['categories'].str.contains(name)]
            return dfr
        elif name == '18+' and path == 'Anime.csv':
            dfr = pd.read_csv(path)
            dfr = dfr.dropna(subset=['Content Warning'], inplace=False)
            return dfr
        # print('No such categories')

def sortet_lenght(path, leng, df):
    '''
    returns data only with certain length
    '''
    if path == 'Anime.csv':
        if leng == 'short':
            df = df[(df['Episodes'] <= 20)]
        elif leng == 'long':
            df = df[(df['Episodes'] >= 100)]
        elif leng == 'mid':
            df = df[(df['Episodes'] >= 20) & (df['Episodes'] <= 100)]
    elif path == 'books.csv':
        if leng == 'short':
            df = df[(df['len'] <= 250)]
        elif leng == 'long':
            df = df[(df['len'] >= 600)]
        elif leng == 'mid':
            df = df[(df['len'] >= 250) & (df['len'] <= 600)]
    elif path == 'films.csv':
        if leng == 'short':
            df = df[(df['len'] <= 60)]
        elif leng == 'long':
            df = df[(df['len'] >= 120)]
        elif leng == 'mid':
            df = df[(df['len'] >= 60) & (df['len'] <=120)]
    elif path == 'netflix_titles.csv':
        df = df[df['duration'].str.contains('Season')]
        df['duration'] = df['duration'].str.replace('Season', '')
        if leng == 'short':
            df = df[(df['duration'] < 2)]
        elif leng == 'long':
            df = df[(df['duration'] >= 4)]
        elif leng == 'mid':
            df = df[(df['duration'] >= 2) & (df['len'] <4)]
    return df

def choosed_year(year, dataframe):
    '''
    returns data only with certain year
    '''
    res_data = pd.DataFrame({'title':[],'description':[],'year':[],'Rating':[]})
    year = [year]
    dataframe = dataframe.dropna(subset=['year'], inplace=False)
    dataframe_year = dataframe[dataframe['year'].isin(year)]
    data = pd.concat([dataframe_year, res_data])
    while len(data) < 30:
        if year [0] >2013:
            year[0] = (year[0]-1)
        if year [0] <1970:
            year[0] = (year[0]+1)
        dataframe_year = dataframe[dataframe['year'].isin(year)]
        data = pd.concat([dataframe_year, data])
    return data


def sorted_rating(df, one_more=  None):
    '''
    this function returns first 3 elements of data sorted by rating
    '''
    df = df.sort_values('Rating')
    df = df[['title', 'description']]
    my_const = 0
    # my_input = input()
    # element_1 = len(df) - 1
    # elem = random.randint(1, element_1)
    if one_more:
        my_const += 1
    return df[my_const:my_const+3]

def my_random(path = None):
    list_path = ["Anime.csv", "Films.csv", "Books.csv", "Netflix.csv", "Manga.csv"]
    if path == None:
        path = random.choice(list_path)
    df = pd.read_csv(path)
    # df = df.sort_values('Rating')
    return df[['title', 'description']].sample(n=1)

app = Flask(__name__)

@app.route('/')
def index():
    # elem = request.form.get('')
    return render_template('main.html')

# @app.route('/button_clicked', methods=['POST'])
# @app.route('/button_value', methods=['POST'])
@app.route("/book")
def book_html():
    # type_csv = button_value()
    # list_csv = [type_csv] + request.json['value']
    # print (type_csv)
    return render_template("book.html")

@app.route("/templates/Films.html")
def Films():
    return render_template("films.html")

@app.route("/manga")
def manga_html():
    return render_template("manga.html")

@app.route("/anime")
def anime_html():
    return render_template("anime.html")

@app.route("/netflix")
def netflix_html():
    return render_template("netflix.html")

@app.route("/exit")
def exit_html():
    text = [["Вибачте", "На жаль ми не знайшли для Вас фільму"]]
    return render_template("output copy.html", text = text)

@app.route("/end", methods = ["POST"])
def end_st():

    value = request.json['value']
    # nast = request.json['elem'][0]
    # print(nast)
    print(f"value is {value}")
    try:
        df_sort = sortet_lenght(value[0], value[3], choosed_year(int(value[2]), choosed_categories(value[0], value[1])))
        result = sorted_rating(df_sort)
        print('result:'+result)
        films = []
        for entry in range(result.shape[0]):
            entry = result.iloc[entry, :].values.flatten().tolist()
            films.append(entry)
        while len(films) < 3:
            films.append(["Вибачте", "На жаль Ми не знайшли для вас фільму"])
        return render_template("ending.html", text = films)
    except:
        text = [["Вибачте", "На жаль ми не знайшли для Вас фільму"]]
        return render_template("output copy.html", text = text)



@app.route("/random", methods = ["POST"])
def random_choice():
    value = request.json['value']
    print(value)
    result = my_random(value)
    print('RESULT:'+result)
    films = []
    for entry in range(result.shape[0]):
        entry = result.iloc[entry, :].values.flatten().tolist()
        films.append(entry)
    print(films)
    return render_template("output.html", text = films)

if __name__ == '__main__':
    app.run(debug=True)
