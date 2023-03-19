# wordfinder

supplements mudae's blacktea with example words!

invite with https://discord.com/api/oauth2/authorize?client_id=1086350121660325968&permissions=85056&scope=bot

database.db stores frequency data

main.py runs discord bot

Ret.py provides supporting classes

sql1.py sets up database.db given the csv (with the column name line removed)

    db: https://www.kaggle.com/datasets/wheelercode/english-word-frequency-list?resource=download

commands:

%help - default help from discord.py

%listen/li <mode> - toggles automatic review on miss

    <mode=on> : 'on', 'i', '1', 'yes', 'y'

    <mode=off> : 'off', 'o', '0', 'no', 'n'

%misslist/ml - prints up to 10 last missed trigrams

%numresponses/nr <count> - sets number of words given on review

    <count=n> : n is int > 0
    
%review/re/rv/r <trigram> <count> - queries for data for trigram

    <trigram=str> : if field empty, reviews last prompt given, else <trigram> should be a three-letter string with no case restriction
    
    <count=n> : sets number of word examples given, n is int > 0

    response format - 

        <trigram> (<% of words have this trigram>, <% of words weighted by frequency have this trigram>):

        <word1> (<% of words weighted by frequency with given trigram are this word>), <word2> (<...>)...

%reviewmiss/rm <count> - same as review with no trigram field, but checks last missed prompt
