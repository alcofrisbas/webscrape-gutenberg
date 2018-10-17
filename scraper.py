import urllib
# import nltk

BASE_URL = "[a][b]"

def scrape_num(n):
    url = BASE_URL.replace("[a]", str(n))
    url = url.replace("[b]", str(n))
    print(url)
    return None

if __name__ == "__main__":
    scrape_num(7138)

