import json
import datetime
import requests

url = 'https://r.onliner.by/sdapi/pk.api/search/apartments?price[min]=4147&price[max]=40000&currency=usd&order=price%3Adesc&bounds[lb][lat]=53.75149755877639&bounds[lb][long]=27.389637623138107&bounds[rt][lat]=54.044319421616265&bounds[rt][long]=27.735169933679895&page=1&v=0.21774406734133656'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "host": "r.onliner.by",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}
src = requests.get(url, headers=headers).json()


def main():
    pages_count = src['page']['last']
    data_list = []
    for page in range(1, pages_count + 1):
        url = f'https://r.onliner.by/sdapi/pk.api/search/apartments?price[min]=4147&price[max]=40000&currency=usd&order=price%3Adesc&bounds[lb][lat]=53.75149755877639&bounds[lb][long]=27.389637623138107&bounds[rt][lat]=54.044319421616265&bounds[rt][long]=27.735169933679895&page={page}&v=0.21774406734133656'
        data = requests.get(url, headers=headers).json()

        for flat in data['apartments']:
            flat_price_usd = flat['price']['converted']['USD']['amount']
            flat_price_byn = flat['price']['converted']['BYN']['amount']
            flat_rooms = flat['number_of_rooms']
            flat_address = flat['location']['address']
            flat_area = flat['area']['total']
            flat_url = flat['url']

            if float(flat_price_usd) <= 40000 and int(flat_rooms) == 1:
                data_list.append({
                    'price in dollars': flat_price_usd,
                    'price in rubles ': flat_price_byn,
                    'number of rooms': flat_rooms,
                    'address': flat_address,
                    'area ': flat_area,
                    'link to the apartment ': flat_url,
                })

        print(f'[INFO]: Processed {page}/{pages_count}')
    current_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f'data_{current_time}.json', "a") as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
