from flask import Flask, render_template, request
import psycopg2
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import re
import json

app = Flask(__name__)

# Making connection to database
conn = psycopg2.connect(database="project1",user = 'postgres', password = 'Anshul24092004', host='localhost')

@app.route("/",methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route("/check",methods = ['POST'])
def check():
    if request.method == 'POST':
        cur = conn.cursor()
        URL = request.form['url']
        URL = str(URL)
        page = requests.get(URL)

        soup = BeautifulSoup(page.content,'html.parser')

        title = soup.title.string

        h1 = soup.findAll('h1')
        h2 = soup.findAll('h2')
        h3 = soup.findAll('h3')
        p = soup.findAll('p')

        head = ''
        para=[]

        for i in h1:
            cleantext = re.sub(r'<.*?>','',str(i))
            head = head + cleantext+'\n'
        for j in h2:
            c = re.sub(r'<.*?>','',str(j))
            head = head + c +'\n'
        for k in h3:
            d = re.sub(r'<.*?>','',str(k))
            head = head + d +'\n'

        filtered_sentence = []
        sent = 0
        words = 0
        stop_words = set(stopwords.words('english'))
        for z in p:
            e = re.sub(r'<.*?>','',str(z))
            para.append(e.strip())
            sent = sent + 1
            for w in word_tokenize(e.strip()):
                words = words+len(word_tokenize(e.strip()))
                if w not in stop_words:
                    filtered_sentence.append(w)
            filtered_sentence.append('\n')

        result_string = ' '.join(filtered_sentence)
        stop = words - len(filtered_sentence)
        num_stopwords = stop

        pos_dict = {}
        for i in para:
            word_list = word_tokenize(i) 
            x = nltk.pos_tag(word_list, tagset='universal')
            for i in x:
                if i[1] in pos_dict:
                    pos_dict[i[1]] += 1
                else:
                    pos_dict[i[1]] = 1
    
        with open("pos_dict.json", 'w'):
            # Use json.dump() to write the dictionary to the file
                a = json.dumps(pos_dict)

        cur.execute(
            '''INSERT INTO DETAILS \
                (url,no_of_words,no_of_sentences,content,no_of_stopwords,headlines,pos_tags) VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                (URL,words,sent,result_string,num_stopwords,head,a))
        
        cur.execute('''SELECT url,no_of_sentences,no_of_words,no_of_stopwords,headlines,pos_tags,content  FROM DETAILS ORDER BY ID DESC LIMIT 1''')
        data = cur.fetchall()
        conn.commit()   
        cur.close()

        return render_template('result.html',data = data)

@app.route("/verify",methods=["GET","POST"])
def verify():
    return render_template('pass.html')

@app.route("/admin",methods=["GET","POST"])
def admin():
    if request.method == 'POST':
        pin = '1234'
        password = request.form['password']
        if pin == password:
            cur = conn.cursor()
            cur.execute('''SELECT id,url FROM DETAILS''')
            url = cur.fetchall()

            conn.commit()
            cur.close()
            return render_template('history.html',url = url)
        else:
            return render_template('pass.html')

@app.route("/index",methods=['GET', 'POST'])
def index():
    return render_template("index.html")

if __name__=='__main__':
    app.run(debug=True, port=8000)
    conn.close()
    