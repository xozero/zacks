import pickle
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup


def get(symbol):
    try:
        header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}
        url = 'https://www.zacks.com/stock/research/%s/all-news/zacks' % symbol

        r = requests.get(url, headers=header)
        soup = BeautifulSoup(r.text, 'html.parser')

        rank = soup.select_one('.rank_view')
        if not rank:
            return "", ""
        rank = rank.text.strip()[:5]
        # Still rank empty..
        if not rank:
            return "", ""

        listitem = soup.select_one(".listitempage .listitem .byline time")
        # We have a rank, but no news. That's ok. (Note: Probably won't happen..)
        if not listitem:
            return rank, ""
        listitem = listitem.string
        listitem = listitem[13:].strip()

        datetime_object = datetime.strptime(listitem, '%B %d,%Y')
        return rank, datetime_object
    except Exception as ex:
        print('ERR', symbol, ex)
        return "", ""


def get_all_first_pass():
    symbols = get_all_base_symbols()

    new_symbols_full = []
    new_symbols = []
    for symbol in symbols:
        rank, dt = get(symbol)
        if rank != "":
            new_symbols.append(symbol)
            new_symbols_full.append((symbol, rank, dt))

        # Barely any overhead.. lets do it.
        with open('symbols_new.txt', 'w+') as f:
            f.writelines('\n'.join(new_symbols))
        with open('symbols_new.pickle', 'wb+') as f:
            pickle.dump(new_symbols_full, f)

        time.sleep(2.)

    with open('symbols_new.txt', 'w+') as f:
        f.writelines('\n'.join(new_symbols))
    with open('symbols_new.pickle', 'wb+') as f:
        pickle.dump(new_symbols_full, f)


def get_all_second_pass():
    symbols = get_all_new_symbols()

    new_symbols_full = []
    for symbol in symbols:
        rank, dt = get(symbol)
        if rank != "":
            new_symbols_full.append((symbol, rank, dt))

        # Barely any overhead.. lets do it.
        with open('symbols_new2.pickle', 'wb+') as f:
            pickle.dump(new_symbols_full, f)

        time.sleep(2.)

    with open('symbols_new2.pickle', 'wb+') as f:
        pickle.dump(new_symbols_full, f)


def get_all_base_symbols():
    with open('nasdaqlisted.txt', 'r') as f:
        symbols = f.readlines()
    with open('otherlisted.txt', 'r') as f:
        symbols.extend(f.readlines())
    symbols = [x.strip() for x in symbols]
    return symbols


def get_all_new_symbols():
    with open('symbols_new.txt', 'r') as f:
        symbols = f.readlines()
    symbols = [x.strip() for x in symbols]
    return symbols


if __name__ == '__main__':
    get_all_second_pass()
