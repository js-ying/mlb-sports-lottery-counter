from flask import Flask, request
from flask.views import MethodView
import requests
import bs4
import json

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False


class MlbCount(MethodView):
    def post(self):
        if 'dateList' in request.form:
            dateList = request.form['dateList']
        else:
            return "Error: No date provided. Please specify a date."

        dateList = json.loads(dateList)

        bet01dataList = []
        bet01DictDataListObj = {}

        bet03dataList = []
        bet03DictDataListObj = {}

        for date in dateList:
            r = requests.get(
                'https://www.playsport.cc/predictgame.php?action=result&allianceid=1&gametime=' + date)

            if r.status_code == 200:
                soup = bs4.BeautifulSoup(r.text, 'lxml')

                bet01Tags = soup.findAll('td', {'class': 'td-bank-bet01'})
                bet03Tags = soup.findAll('td', {'class': 'td-bank-bet03'})

                for bet01 in bet01Tags:
                    try:
                        bet01dataList.append(
                            ('勝' if bet01.div.get('class') else '') + bet01.div.strong.string +
                            bet01.div.span.strong.string + bet01.div.span.span.string
                        )
                    except:
                        continue

                for bet03 in bet03Tags:
                    try:
                        bet03dataList.append(
                            ('勝' if bet03.div.get('class') else '') +
                            bet03.div.strong.string + bet03.div.span.span.string
                        )
                    except:
                        continue
            else:
                return "Crawl Fail."

        for bet01data in bet01dataList:
            if '勝' in bet01data:
                if bet01data[1:] not in bet01DictDataListObj:
                    bet01DictDataListObj[bet01data[1:]] = 1
                else:
                    bet01DictDataListObj[bet01data[1:]] += 1

        for bet03data in bet03dataList:
            if '勝' in bet03data:
                if bet03data[1:] not in bet03DictDataListObj:
                    bet03DictDataListObj[bet03data[1:]] = 1
                else:
                    bet03DictDataListObj[bet03data[1:]] += 1

        result = {
            "bet01": bet01DictDataListObj,
            "bet03": bet03DictDataListObj
        }

        return result


app.add_url_rule('/mlb-count', view_func=MlbCount.as_view('mlb_count'))

if __name__ == '__main__':
    app.run()
