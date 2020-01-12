import rumps
import requests

VERSION = "0.0.1"

ABOUT_TEXT = "Version: %s. \n\nPrice is fetched from Coinmarketcap API with a" \
             " 60 seconds interval. \n\nFor bug reports or feature requests " \
             "see https://github.com/emre/steem-osx-statusbar. \n\n" \
             "Icon set: https://www.iconfinder.com/icons/4518815/steem_icon" % (
                 VERSION
             )


class SteemStatusBarApp(rumps.App):

    @rumps.clicked("About")
    def about(self, _):
        rumps.alert(ABOUT_TEXT)

    @rumps.timer(300)
    def update_info(self, _):
        r = requests.get(
            "https://api.coinmarketcap.com/v1/ticker/steem/").json()
        price_usd = r[0]["price_usd"]
        self.title = "Steem price: $%s" % round(float(price_usd), 2)


if __name__ == "__main__":
    SteemStatusBarApp("...").run()
