# wordfinder

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

    <count=n> : 0<n<=10
    
%review/re/rv/r <trigram> - queries for data for trigram

    <trigram=str> : if field empty, reviews last prompt given, else <trigram> should be a three-letter string with no case restriction

    response format - 

        <trigram> (<% of words have this trigram>, <% of words weighted by frequency have this trigram>):

        <word1> (<% of words weighted by frequency with given trigram are this word>), <word2> (<...>)...

%reviewmiss - same as review with no field, but checks last missed prompt
