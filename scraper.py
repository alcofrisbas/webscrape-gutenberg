import urllib.request
import sys
# import nltk

BASE_URL = "https://www.gutenberg.org/files/[a]/[b].txt"

def scrape_num(n):
    url = BASE_URL.replace("[a]", str(n))
    url = url.replace("[b]", str(n))
    print(url)
    with urllib.request.urlopen(url) as r:
        text = r.read().decode("utf-8")

    return(text)

if __name__ == "__main__":
    args = sys.argv[1:]
    t = scrape_num(args[0])
    print(len(t))
    print(t.split("\n")[0])
