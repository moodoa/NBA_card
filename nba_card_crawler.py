import re
import requests
from bs4 import BeautifulSoup

class NBAcard:
    def _get_card_price(self, start_year, end_year, keywords):
        headers = {
        "Cookie": Your_Cookie
        }
        keywords = keywords.replace(" ", "+")
        all_year_card_price = {}
        pattern = r"PSA (\d+)"
        for year in range(start_year, end_year, 1):
            text = requests.get(f"https://www.pwccmarketplace.com/market-price-research?q={keywords}&year_min={year}&year_max={year+1}&items_per_page=100", headers=headers).text
            soup = BeautifulSoup(text, "lxml")
            all_cards = soup.select_one("table.table").select("tr")
            card_price = []
            for idx in range(1, len(all_cards)):
                wanted = True
                title = all_cards[idx].select_one("td.card-title").string
                price = float(all_cards[idx].select_one("td.item-price").string.split("$")[1].strip().replace(",", ""))
                for bgs in ["BGS", "bgs"]:
                    if bgs in title:
                        wanted = False
                for rank in re.findall(pattern, title):
                    if int(rank) < 10:
                        wanted = False
                if wanted:
                    card_price.append(price)
            all_year_card_price[year] = round(sum(card_price)/len(card_price), 2)
        return all_year_card_price
    