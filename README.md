# NBA_card
收集球員卡歷史價格與球員表現比對
![alt text](https://i.imgur.com/wx1pKLE.png)

## nba_card_crawler.py

#### make_player_df
* 以 `球員名字(basketball reference 上為主)`、`起始年份`、`結束年份`、`球員卡關鍵字(以空白隔開)`、 為參數爬取 NBA 球員之歷史數據以及球員卡價格。
* Your_Cookie 為個人帳號登入 pwcc marketplace 後所獲取之 cookie。
* 回傳值為 CSV 檔，columns 分別是 1,`Season`、2,`Tm(Team)`、3,`champion(冠軍與否)`、4,`PTS`、5,`fantasy_p(fantasy 分數)`、6,`card_price(該年卡片平均價格)`。
 
#### draw
* 將爬取下來的 `Datafrme` 轉成 `png` 圖檔，並存在本地資料夾中。

## Requirements
python 3

## Usage
```
if __name__ == "__main__":
    nbacard = NBAcard(
        "LeBron James", 2003, 2021, "lebron rc topps chrome refractor psa"
    )
    df = nbacard.make_player_df()
    nbacard.draw(df)

```
## Installation
`pip install -r requriements.txt`
