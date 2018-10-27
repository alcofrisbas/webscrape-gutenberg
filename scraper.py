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
        i = re.sub(r'[^\w:/.-]', ' ', i)
        #print(type(i))
        d[i.split(":")[0]] = ":".join(i.split(":")[1:]).strip()
    print(d["url"])
    return d

def get_info(n):
    try:
        url = BASE_URL.replace("[a]", str(n))
        url = url.replace("[b]", str(n))
        #print(url)
        with urllib.request.urlopen(url) as r:
            #r.seek(0)
            text = r.read(2000).decode("utf-8")
        header_info = [i.strip() for i in text.split("***")[0].split("\n") if ":" in i]
        header_info.append("url:{}".format(url))
        return info_to_d(header_info)
    except Exception as e:
        pass#print(e)
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
        pass#print(e)
    return {}

def get_full_text(url,fname, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    with urllib.request.urlopen(url) as r:
        text = r.read().decode("utf-8")
    # remove licensing header and footer
    text = text.split("***\r")[1]
    text = text.split("End of Project Gutenberg's")[0]
    text = text.split("***END")[0]
    text = text.split("*** END")[0]
    # chapter headers...
    text = re.sub("CHAPTER ([IXLV]*|\d+)", "", text)
    text = re.sub("[*]", "", text)
    if len(text) > 10000:
        with open(dest_dir+"/"+fname,'w') as w:
            w.write(text)

def add_to_table(d,c):
    if d:
        query = "INSERT INTO books VALUES('{}', '{}', '{}', '{}')".format(d.get("Title", "").lower(),
                        d.get("Author", "").lower(),
                        d.get("Language", "").lower(),
                        d.get("url", ""))
        #query = query.encode('unicode-escape')
        #query.decode("utf-8")
        #print(query)
        c.execute(str(query))
    else:
        print("asdf wtf")

def query(c, col, row):
    q = "select * from books where {} is '{}'".format(col, row)
    c.execute(q)
    return c.fetchall()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("fname", action="store", help="specify database file")
    parser.add_argument('--makedb', action="store_true", default=False,
                            help="intitialize new database")
    parser.add_argument('--all', '-a', action="store_true", default=False,
                            help="not yet implemented")
    parser.add_argument('-q', action="store", dest="query", nargs=2,
                            help="An sql query to return records and download documents")
    parser.add_argument('--output_dir','-o', action="store", dest="output_dir",
                            help="destination to store documents")
    parser.add_argument('--test', action="store_true", default=False)
    parser.add_argument('--range', '-r', action="store", nargs=2, dest="scan_range")
    args = parser.parse_args()
    # print(args)
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
                conn, c = create_db(args.fname)
            else:
                sys.exit(0)
        else:
            conn, c = create_db(args.fname)
        if args.scan_range:
            for i in range(int(args.scan_range[0]), int(args.scan_range[1])):
                d = get_info(i)
                add_to_table(d, c)
            conn.commit()
    elif args.query:
        conn, c = connect_db(args.fname)
        col = args.query[0]
        row = args.query[1]
        lst = query(c, col, row)
        if input(("{} records found. Save? ".format(str(len(lst))))) == "y":
            for i in lst:
                get_full_text(i[3], "{}_{}.txt".format(i[1], i[0]), "saves")
