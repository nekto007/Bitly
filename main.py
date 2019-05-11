import requests
import argparse
import json
import os
from dotenv import load_dotenv
load_dotenv()


def create_short_link(token, long_url):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json"
    }
    data = {"long_url": long_url}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.ok:
        return response.json()["link"]


def get_count_click(token, bitlink_url):
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary?unit=month&units=-1".format(bitlink_url)
    headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()["total_clicks"]


def is_bitlink(token, site_link):
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}".format(site_link)
    headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.ok



def main():
    parser = argparse.ArgumentParser(
        description='Программа показывает количество кликов по сокращеннй ссылке и так же создает короткую ссылку.'
    )
    parser.add_argument('url', help='Адрес сайта')
    site_link = parser.parse_args().url
    bitlink = is_bitlink(os.getenv("auth_token"), site_link)
    if bitlink:
        count_click = get_count_click(os.getenv("auth_token"), site_link)
        if count_click:
            print("Количество кликов за месяц: {}".format(count_click))
        else:
            print(None)
    else:
        short_link = create_short_link(os.getenv("auth_token"), site_link)
        if short_link:
            print("Короткий URL: {}".format(short_link))
        else:
            print("Введена некорректная ссылка")


if __name__ == "__main__":
    main()
