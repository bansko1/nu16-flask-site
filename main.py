from datetime import datetime
import json
import os
from random import randint
from flask import Flask, render_template, request
from bill_oop import Bill

FILE_NAME = 'bills.json'
FILE_HISTORY = 'histores.json'

app = Flask(__name__)

@app.route("/") # Главная. Описание.
def index():
    return render_template('index.html')

@app.route('/bill-find/', methods=['GET']) # 1.1 Форма для получения имени игрока.
def run_get():
    return render_template('form.html')

@app.route('/bill-find/', methods=['POST']) # 1.2 Получение имени игрока.
def run_post():
    bills = {}
    histores = {}
    # Получть данные формы
    global name
    name = request.form['input_text']
    if os.path.exists(FILE_NAME): # Если файл существует
        with open(FILE_NAME, 'r') as f:
           bills = json.load(f)
    if os.path.exists(FILE_HISTORY):
        with open(FILE_HISTORY, 'r') as f:
            histores = json.load(f)
                   
        if name in bills: # У игрока name есть счет в bills
            count = bills[name]
            bills[name] = count
        else:                   # У игрока name нет счета в bills
            count = 0
            bills[name] = count
            with open(FILE_NAME, 'w') as f:
                json.dump(bills, f)
            now = datetime.now().strftime("%d-%m-%Y")
            lst = []
            hist = f'{now} Игроку {name} открыт счет на {count} единиц.'
            lst.append(hist)
            histores[name] = lst
            with open(FILE_HISTORY, 'w') as f:
                json.dump(histores, f)
    else: # Если файл не существует
        count = 0
        bills[name] = count
        
        with open(FILE_NAME, 'w') as f:
            json.dump(bills, f)
        now = datetime.now().strftime("%d-%m-%Y")
        if name not in histores:
            lst = []
        else:
            lst = histores[name]
        hist = f'{now} Игроку {name} открыт счет.'
        lst.append(hist)
        histores[name] = lst
        with open(FILE_HISTORY, 'w') as f:
            json.dump(histores, f)
            
    return render_template('good.html', name=name, count=count)

@app.route('/bill-data/', methods=['GET']) # 2 - Узнать сумму на счете.
def bill_post():
    # name = request.form['input_text']
    with open(FILE_NAME, 'r') as f:
        bills = json.load(f)
    with open(FILE_HISTORY, 'r') as f:
        histores = json.load(f)
    try:
        return render_template('bill_data.html', name=name, bills=bills, histores=histores)
    except:
        return render_template('info_name.html')

@app.route('/bill-add/', methods=['GET']) # 1.1 Форма для получения имени игрока.
def bill_add_get():
    try:
        return render_template('form_sum.html', name=name)
    except:
        return render_template('info_name.html')

@app.route('/bill-add/', methods=['POST']) # 3 - Добавить сумму на счет.
def bill_add_post():
    #name = request.form['input_text']
    count = int(request.form['input_count'])
    with open(FILE_NAME, 'r') as f:
        bills = json.load(f)
    with open(FILE_HISTORY, 'r') as f:
        histores = json.load(f)
    try:
        bills[name] += count
    except:
            return render_template('info_name.html')
        
    with open(FILE_NAME, 'w') as f:
        json.dump(bills, f)
    now = datetime.now().strftime("%d-%m-%Y")
    if name not in histores:
        lst = []
    else:
        lst = histores[name]
    hist = f'{now} Счет игрока {name} пополнен на {count} единиц.'
    lst.append(hist)
    histores[name] = lst
    with open(FILE_HISTORY, 'w') as f:
        json.dump(histores, f)

    return render_template('bill_add.html', name=name, count=count)    
    

@app.route('/play/', methods=['GET']) # 1.1 Форма для получения имени игрока.
def play_get():
    min = 100
    with open(FILE_NAME, 'r') as f:
        bills = json.load(f)
    try:
        lim = bills[name]
    except:
        return render_template('info_name.html')
          
    return render_template('form_bet.html', name=name, min=min, lim=lim)

@app.route('/play/', methods=['POST']) # 4 - Играть.
def play_post():
    min = 100
    #name = request.form['input_text']
    with open(FILE_NAME, 'r') as f:
        bills = json.load(f)
    lim = bills[name]
    bet = int(request.form['input_count'])
    if bet > lim or bet < min:
        return render_template('info_bet.html', min=min, lim=lim)
    choise_num = int(request.form['input_choise'])
    # Игра
    if choise_num == 1:
        choise = 'Камень'
    elif choise_num == 2:
        choise = 'Ножницы'
    elif choise_num == 3:
        choise = 'Бумага'
    else:
        choise = 'Неправильно ввели. Введите 1, 2 или 3.'
        
    choise_comp =   randint(1,3) # Случайное число (1,2 или 3)
    if choise_comp == 1:
        choise_c = 'Камень'
    elif choise_comp == 2:
        choise_c = 'Ножницы'
    elif choise_comp == 3:
        choise_c = 'Бумага'
        
    with open(FILE_NAME, 'r') as f:
        bills = json.load(f)
    with open(FILE_HISTORY, 'r') as f:
        histores = json.load(f)
        
    if (choise_num == 1 and choise_comp == 2)or(choise_num == 2 and choise_comp == 3)or(choise_num == 3 and choise_comp == 1):
        result = 'Победа :) Счет увеличен.'

        bills[name] += bet
        now = datetime.now().strftime("%d-%m-%Y")
        lst = histores[name]
        hist = f'{now} Выигрыш. Счет игрока {name} пополнен на {bet} единиц.'
        lst.append(hist)
        histores[name] = lst
        
    elif choise_num == choise_comp:
        result = 'Ничья ;) Ставка возвращена.'
        bills[name] += 0
        now = datetime.now().strftime("%d-%m-%Y")
        lst = histores[name]
        hist = f'{now} Ничья. Счет {name} без изменений.'
        lst.append(hist)
        histores[name] = lst
    else:
        result = 'Проигрыш :( Ставка потеряна.'
        bills[name] -= bet
        now = datetime.now().strftime("%d-%m-%Y")
        lst = histores[name]
        hist = f'{now} Проигрыш. Счет игрока {name} уменьшен на {bet} единиц.'
        lst.append(hist)
        histores[name] = lst

    with open(FILE_NAME, 'w') as f:
        json.dump(bills, f)
    with open(FILE_HISTORY, 'w') as f:
        json.dump(histores, f)
    
    return render_template('play.html', name=name, count=bet, choise=choise, choise_c=choise_c, result=result)
    

if __name__ == "__main__":
    app.run(debug=True)
