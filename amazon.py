import requests
from bs4 import BeautifulSoup

def get_review(pages):

    # headers = {
    #     'authority': 'www.amazon.com',
    #     'cache-control': 'max-age=0',
    #     'rtt': '100',
    #     'downlink': '9.2',
    #     'ect': '4g',
    #     'sec-ch-ua': '^\\^',
    #     'sec-ch-ua-mobile': '?0',
    #     'upgrade-insecure-requests': '1',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #     'sec-fetch-site': 'same-origin',
    #     'sec-fetch-mode': 'navigate',
    #     'sec-fetch-user': '?1',
    #     'sec-fetch-dest': 'document',
    #     'accept-language': 'en-US,en;q=0.9',
    #     'cookie': 'session-id=140-4142375-4005405; i18n-prefs=USD; sp-cdn=^\\^L5Z9:IN^\\^; ubid-main=133-1703036-0414721; s_fid=15ACC4BA280D4F14-038C9A8E5E877985; regStatus=pre-register; aws-target-data=^%^7B^%^22support^%^22^%^3A^%^221^%^22^%^7D; aws-target-visitor-id=1623992980699-29478.31_0; lc-main=en_US; session-id-time=2082787201l; session-token=3C7FE5erzwisM4Q9VFUHzXSA/eMeK109XvSk3qGH0QACt4108/s0lKTOpDVQTEBs90M2tWq4niv7M6Qb/uP3k9iBEKg1xKTsaibq9ACUJiyvDiduYSi6Lo1A5rR3BFtb0hKq5YaiuVdgb0SctM4i6hzPr5w4P3scMT7tePHGZFUKSnw7eYAlsAD5i14Zhu7U; csm-hit=adb:adblk_no&t:1624715411612&tb:3Z2570B9GG7KJPY3JW0K+s-3Z2570B9GG7KJPY3JW0K^|1624715411612',
    # }

    headers = {
    'authority': 'www.amazon.in',
    'cache-control': 'max-age=0',
    'rtt': '150',
    'downlink': '4.45',
    'ect': '4g',
    'sec-ch-ua': '^\\^',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'session-id=259-9354980-7389332; ubid-acbin=262-5210811-6696624; x-acbin=^\\^H96cjwvh2U2nBOS2d2cQFAniSWfSWHpdf1j86BrKKH0gm49zrhYu1x^@n5J?Hbq4J^\\^; at-acbin=Atza^|IwEBIBtjzvsRWG0wQIptTR8HB6tu2yZG_OWvt0vp1xikvnmUYc15AMp7jJOiKay0pmK9U5ROjBdjapzr7qfxj3-0Ow_IjWbxPGtsELz_geqNV3n1GRFb8bJqIqkR-aNyKPLLRjzNj7kP4Nk9s_WXnEwO8kAHTyU-0JA4wEZZ57JY04-1-a18XQvTrqp4dCWgJLMSTHCb9-lQ-MvkimMDwkfsWpTE; sess-at-acbin=^\\^FG7jGqiiSUoGkyQJC69Hs1R5+9Ks0iKp3w7oCkp41II=^\\^; sst-acbin=Sst1^|PQESQdvpHfcu8u68cWT9iWXDCX6g_DV22Uanl7kaBl-cvpuyTvWBeSdyZHIgeMqU7l3E99cf9_qcwDiv8p9pS1IT8qe0ZfRhZJRgKZ5mAadOfyXls3HuXgNmeT1PHZS_cS728HxjZccDOJsjTQBxV9nFKcBl18b4ujbrFch9WUASSRUuDZX-6fBj-Z-gCACTrhxdmZ18yxoHBAz7JQCxmAoIJwapg49wft3T60V5mQasOQZkDLgNAJQfRhyaXWD0WeDjzyOY3HHR9ZcqWUafbCz6GCnS3bh88PUFGQI0wc5A77A; i18n-prefs=INR; lc-acbin=en_IN; csd-key=eyJ3YXNtVGVzdGVkIjp0cnVlLCJ3YXNtQ29tcGF0aWJsZSI6dHJ1ZSwid2ViQ3J5cHRvVGVzdGVkIjpmYWxzZSwidiI6MSwia2lkIjoiNWE4ZWVlIiwia2V5IjoiakpJMXgzSk1uT3hkUGxraWl4TEY3OWp1THM3eEczTURrdEwyMkZ1TUZXWWFqODRXQW1VY2RFcnhrdklXN0NJcFdDRGhOcjd4Ly9VdERUZm1kcS9QY1FxeUd2TVgzNmsvUnVGcjNtcVRWQmlXL09sQ0g0TjdzT25QQldmeEN1NC94a1F2cDBDU1pBL2dkYUxNQ0M2UnZibmhYdU1zeTIzZjVJWkYxcjZCZEpIZzdtaTBzTzA0dmpDV2NNbmdibWVkQW5uUGNDaUhJRjJuQUNUL3ZBV2EvR25wR1FSMHF0UVV5MTUzZkc3amVBaUFEOFR4U0F3OXozc2xYWDRVcnVIUGZkcFZJaHpnRDAwd3QvM3hpcDZRRHp2bnlFQnUrWVZOYXpPcFRlNlhYZEJ6U2JsdFE4WGswUXBLdjMzcUVtdk4zYTZQclE2S0hlZTdqQ3o4SUxrMTdBPT0ifQ==; visitCount=66; session-token=^\\^j+yMJtbagTgPFtS9l0KldxNceVC8QOUmxEwPHXEu7QnNicqTQN4bUX4ozb+4KI5yezLif5kDHrTP3RX9RZ5Uz1nDZ46z3nROMCXM6rh1jB9CQ8vUYLfScHBu5XfBzVpkagTejvraDygrsqs/Q07FRPywHFvXeEsAPrUi7yHl/OVJxQBs2rycTTJEG020xZ7Clo5vWnlWOq2bGG4RYBSkNg==^\\^; session-id-time=2082758401l; csm-hit=tb:70PR38AQZTK7ER95BFX5+s-B2YY64S8NCR3VDDN3K7R^|1624958652179&t:1624958652179&adb:adblk_yes',
    }


    resp = requests.get(pages, headers=headers)

    soup = BeautifulSoup(resp.text, "html.parser") # html.parser, lxml

    # 10 divs
    reviews = soup.find_all("div", {"class": "a-section review aok-relative"})

    def get_review_body(soup_obj: BeautifulSoup) -> str:
        try:
            review_body = soup_obj.find('span', 
                {"class": "a-size-base review-text review-text-content"}
            ).get_text().strip()
            return review_body
        except Exception as e:
            return 'no_body'
            print(e)

    records = [get_review_body(rev) for rev in reviews]
    return records[1:]