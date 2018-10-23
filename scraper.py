import urllib.request
import sys, os
import sqlite3
import requests
import argparse
import random
import re
# import nltk
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':RC4-SHA'

BASE_URL = "http://www.gutenberg.org/files/[a]/[b].txt"

# t = ("jane austen",)
# c.execute("select * from books where author=?", t)
# print(c.fetchall())

def create_db(fname):
    conn = sqlite3.connect(fname)
    c = conn.cursor()
    c.execute("drop table if exists books")
    c.execute('''CREATE TABLE  books
    (title text, author text, lang text, url text)''')
    conn.commit()
    print("Database {} initialized with table 'books'".format(fname))
    return conn, c

def connect_db(fname):
    conn = sqlite3.connect(fname)
    c = conn.cursor()
    return conn, c

def info_to_d(h_i):
    d = {}
    for i in h_i:
        #make this regex better!!
        i = re.sub(r'[^\w]', ' ', i)
        print(i)
        d[i.split(":")[0]] = ":".join(i.split(":")[1:]).strip()
    return d

def get_info(n):
    try:
        url = BASE_URL.replace("[a]", str(n))
        url = url.replace("[b]", str(n))
        #print(url)
        with urllib.request.urlopen(url) as r:
            text = r.read().decode("utf-8")
        header_info = [i.strip() for i in text.split("***")[0].split("\n") if ":" in i]
        header_info.append("url:{}".format(url))
        return info_to_d(header_info)
    except Exception as e:
        print(e)
    try:
        url = BASE_URL.replace("[a]", str(n))
        url = url.replace("[b]", str(n)+"-0")
        #print(url)
        with urllib.request.urlopen(url) as r:
            text = r.read().decode("utf-8")
        header_info = [i.strip() for i in text.split("***")[0].split("\n") if ":" in i]
        header_info.append("url:{}".format(url))
        #print(header_info)
        return info_to_d(header_info)
    except Exception as e:
        print(e)
    return {}

def add_to_table(d,c):
    if d:
        query = "INSERT INTO books VALUES('{}', '{}', '{}', '{}')".format(d.get("Title", "").lower(),
                        d.get("Author", "").lower(),
                        d.get("Language", "").lower(),
                        d.get("url", ""))
        query = query.encode('unicode-escape')
        print(query)
        c.execute(str(query))
    else:
        print("asdf wtf")
def query(c, t):
    c.execute(t)
    return c.fetchall()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("fname", action="store", help="specify database file")
    parser.add_argument('--makedb', action="store_true", default=False,
                            help="intitialize new database")
    parser.add_argument('--all', '-a', action="store_true", default=False,
                            help="not yet implemented")
    parser.add_argument('-q', action="store", dest="query",
                            help="An sql query to return records and download documents")
    parser.add_argument('--output_dir','-o', action="store", dest="output_dir",
                            help="destination to store documents")
    parser.add_argument('--test', action="store_true", default=False)
    args = parser.parse_args()
    if args.test:
            conn, c = create_db("test.db")
            for i in range(20):
                d = get_info(random.randrange(58153))
                add_to_table(d,c)
            conn.commit()
            print(query(c, "select * from books where lang is 'english'"))

    elif args.makedb:
        if os.path.exists(args.fname):
            if input("File {} exists, overwrite(y/n)? ".format(args.fname)) == "y":
                create_db(args.fname)
        else:
            create_db(args.fname)
