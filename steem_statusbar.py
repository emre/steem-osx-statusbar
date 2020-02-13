import rumps
import requests

VERSION = "0.0.2"


ABOUT_TEXT = "Version: %s. \n\nPrice is fetched from Coinmarketcap API with a" \
             " five minutes interval. \n\nFor bug reports or feature requests " \
             "see https://github.com/emre/steem-osx-statusbar. \n\n" \
             "Icon set: https://www.iconfinder.com/icons/4518815/steem_icon" % (
                 VERSION
             )


class SteemStatusBarApp(rumps.App):

    @rumps.clicked("About")
    def about(self, _):
        rumps.alert(ABOUT_TEXT)

    @rumps.clicked('Change update interval')
    def changeit(self, _):
        response = rumps.Window('Enter new interval (In seconds)').run()
        if response.clicked:
            try:
                rumps.timer.__dict__["*timers"][0].interval = int(response.text)
                rumps.alert("Interval set as %s seconds." % response.text)
            except ValueError:
                rumps.alert("Invalid value")

    @rumps.timer(5)
    def update_info(self, _):
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=s"
            "teem%2Csteem-dollars&vs_currencies=usd&include_24hr_change=true"
        ).json()

        sbd_price_usd = r["steem-dollars"]["usd"]
        sbd_price_up = r["steem-dollars"]["usd_24h_change"] > 0

        steem_price_usd = r["steem"]["usd"]
        steem_price_up = r["steem"]["usd_24h_change"] > 0

        self.title = "Steem: $%s %s  - SBD: $%s %s " % (
            round(float(steem_price_usd), 2),
            "🆙" if steem_price_up else "",
            round(float(sbd_price_usd), 2),
            "🆙" if sbd_price_up else "",
        )


if __name__ == "__main__":
    steem_status_bar_app = SteemStatusBarApp("...")
    steem_status_bar_app.run()
