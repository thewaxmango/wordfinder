import sqlite3
from urllib.request import urlopen
import re
# 9028030 1847291876619

class Retriever():
    ALPHA = re.compile('[^a-zA-Z]')

    def __init__(self, database):
        self.querier = Querier(database)
        self.listen = False
        self.history = []
        self.missed = []
        self.numresp = 5

    def __call__(self, query):
        return self.querier(query, self)

    def store(self, query):
        self.history.append(self.ALPHA.sub('', query).lower())

    def get_misses(self):
        return [
            "none recorded", "last 10: " + ", ".join(self.missed[-1:-11:-1])
        ][bool(self.missed)]

    def set_numresp(self, query):
        if not query.isdigit():
            return "argument was not an integer between 1 and 10 inclusive"
        q = int(query)
        if q < 1 or q > 10:
            return "argument was not between 1 and 10 inclusive"
        else:
            self.numresp = query
            return f"number of responses is now {query}"


class Querier():
    MISS = 1
    WORDTOT = 9028030
    OCCURTOT = 1847291876619

    def __init__(self, database):
        self.dbfile = database

    def __call__(self, query, retr):
        if query == None:
            if not retr.history:
                return "nothing to review"
            q = retr.history[-1]

        elif query == self.MISS:
            if not retr.missed:
                return "nothing missed to review"
            q = retr.missed[-1]

        elif len(query) != 3 or not query.isalpha():
            return "invalid search term, should be alphabetic string of length 3"

        else:
            q = query.lower()

        vals = self.db_query(q)

        out = f"**{q.upper()}** "
        if len(vals) == 0:
            return out + "has no known words"
        roottot = sum(v[1] for v in vals)
        out += f"({round(len(vals)/self.WORDTOT*100,2)}%, {round(roottot/self.OCCURTOT*100,2)}%):\n"
        for word, ct in vals[0:int(retr.numresp)]:
            out += f"{word} ({round(ct/roottot*100,2)}%), "
        out.strip(", ")
        return out

    def db_query(self, query):
        conn = sqlite3.connect(self.dbfile)
        curs = conn.cursor()
        words = self.getwords(query)
        curs.execute(f"SELECT * FROM words WHERE word IN {tuple(words)}")
        a = curs.fetchall()
        conn.close()
        return a

    def getwords(self, root):
        page = urlopen(
            f"https://www.thefreedictionary.com/words-containing-{root}")
        html_bytes = page.read().decode("utf-8")
        words = [
            a.split("\"")[1].lower()
            for a in re.findall(r"href=\"[a-zA-Z]+\"", html_bytes)
        ] + [root]
        return words
