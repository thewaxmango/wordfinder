from unidecode import unidecode
import sqlite3
import csv
import re

regex = re.compile('[^a-zA-Z]')

s = set()

for k in range(10):
    l = k*10**6 - 1
    r = (k+1)*10**6
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS words(word, frequency)")

    with open("ngram_freq.csv", newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=' ', quotechar='|')
        for a, line in enumerate(f):
            if not l<a<r:
                continue
            if not a%100000:
                print(a)
                conn.commit()
            word, freq = map(str, line.split(","))
            word = regex.sub('', unidecode(word).lower())
            freq = int(freq)

            if word in s:
                continue
            s.add(word)

            cur.execute(f"INSERT INTO words VALUES ('{word}', {freq})")
            

    conn.close()