import re
import requests
import unidecode, unicodedata
import pandas as pd
from bs4 import BeautifulSoup

class NBAcard:
    def __init__(self, player_name, start_year, end_year, keywords):
        self.name = player_name
        self.start_year = start_year
        self.end_year = end_year
        self.keywords = keywords

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
    
    def _get_player_info(self):
        suffix = self._get_player_suffix(self.name).replace('/', '%2F')
        selector = "per_game"
        content = requests.get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url={suffix}&div=div_{selector}').content
        soup = BeautifulSoup(content, "lxml")
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        return df

    def _get_champ_year(self):
        champ_year = []
        selector = "playoffs_per_game"
        suffix = self._get_player_suffix(self.name).replace('/', '%2F')
        content = requests.get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url={suffix}&div=div_{selector}').content
        soup = BeautifulSoup(content, "lxml")
        for year in soup.select("th.left"):
            if year.select_one("span"):
                champ_year.append(year.text)
        return champ_year

    def _get_player_suffix(self, name):
        normalized_name = unidecode.unidecode(unicodedata.normalize('NFD', self.name).encode('ascii', 'ignore').decode("utf-8"))
        initial = normalized_name.split(' ')[1][0].lower()
        suffix = '/players/'+initial+'/'+self._create_suffix(self.name)+'01.html'
        player_r = requests.get(f'https://www.basketball-reference.com{suffix}')
        while player_r.status_code==200:
            player_soup = BeautifulSoup(player_r.content, "lxml")
            h1 = player_soup.find('h1', attrs={'itemprop': 'name'})
            if h1:
                page_name = h1.find('span').text
                if ((unidecode.unidecode(page_name)).lower() == normalized_name.lower()):
                    return suffix
                else:
                    suffix = suffix[:-6] + str(int(suffix[-6])+1) + suffix[-5:]
                    player_r = get(f'https://www.basketball-reference.com{suffix}')
        return None
    
    def _create_suffix(self, name):
        normalized_name = unicodedata.normalize('NFD', self.name.replace(".","")).encode('ascii', 'ignore').decode("utf-8")
        first = unidecode.unidecode(normalized_name[:2].lower())
        lasts = normalized_name.split(' ')[1:]
        names = ''.join(lasts)
        second = ""
        if len(names) <= 5:
            second += names[:].lower()
        else:
            second += names[:5].lower()
        return second+first
    
    def make_player_df(self):
        df = self._get_player_info()
        df = df.head(df[df["Season"] == "Career"].index[0])
        champ_year = self._get_champ_year()
        year_price = self._get_card_price(self.start_year, self.end_year, self.keywords)
        df["champion"] = df["Season"].apply(lambda x:x in champ_year)
        df["card_price"] = df["Season"].apply(lambda x: year_price[int(x.split("-")[0])])
        df["fantasy_p"] = df["PTS"]+(df["TRB"]*1.2)+(df["AST"]*1.5)+(df["BLK"]*3)+(df["STL"]*3)-(df["TOV"]*1)
        df = df[["Season", "Tm", "champion", "PTS", "fantasy_p", "card_price"]]
        df.to_csv("card_price.csv", index=False)
        return df

if __name__ == "__main__":
    nbacard = NBAcard("LeBron James",2003, 2021, "lebron rc topps chrome refractor psa")
    print(nbacard.make_player_df())