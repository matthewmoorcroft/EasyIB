import requests


class REST:
    def __init__(self, url="https://localhost:5000", ssl=False) -> None:

        self.url = url + "/v1/api/"
        self.ssl = ssl
        self.id = self.get_accountid()

    def get_accountid(self) -> str:
        response = requests.get(self.url + "portfolio/accounts", verify=self.ssl)
        return response.json()[0]["accountId"]

    def get_cash(self) -> float:
        response = requests.get(
            self.url + "portfolio/" + self.id + "/ledger",
            verify=self.ssl,
        )
        return response.json()["USD"]["cashbalance"]

    def get_netvalue(self) -> float:
        response = requests.get(
            self.url + "portfolio/" + self.id + "/ledger",
            verify=self.ssl,
        )
        return response.json()["USD"]["netliquidationvalue"]

    def get_conid(self, symbol: str) -> int:
        query = {"symbols": symbol}
        response = requests.get(
            self.url + "trsrv/stocks", params=query, verify=self.ssl
        )
        dic = response.json()
        return dic[symbol][0]["contracts"][0]["conid"]

    def get_portfolio(self) -> dict:
        response = requests.get(
            self.url + "portfolio/" + self.id + "/positions/0",
            verify=self.ssl,
        )
        dic = {}
        for item in response.json():
            dic.update({item["contractDesc"]: item["position"]})
        dic.update({"USD": self.get_cash()}) # Cash balance
        return dic

    def reply_yes(self, id: str) -> dict:
        answer = {"confirmed": True}
        response = requests.post(
            self.url + "iserver/reply/" + id,
            json=answer,
            verify=self.ssl,
        )
        return response.json()[0]

    def submit_order(self, request: dict, reply_yes=True) -> dict:
        response = requests.post(
            self.url + "iserver/account/" + self.id + "/orders",
            json=request,
            verify=self.ssl,
        )
        dic = response.json()[0]
        if reply_yes:
            while "order_id" not in dic.keys():
                print("Answering yes to ...")
                print(dic["message"])
                dic = self.reply_yes(dic["id"])
        return dic

    def get_order(self, orderId: str) -> dict:
        response = requests.get(
            self.url + "iserver/account/order/status/" + str(orderId), verify=self.ssl
        )
        return response.json()

    def get_live_orders(self) -> dict:
        response = requests.get(self.url + "iserver/account/orders", verify=self.ssl)
        return response.json()

    def cancel_order(self, orderId: str) -> dict:
        response = requests.delete(
            self.url + "iserver/account/" + self.id + "/order/" + str(orderId),
            verify=self.ssl,
        )
        return response.json()

    def ping_server(self) -> dict:
        response = requests.post(self.url + "tickle", verify=self.ssl)
        return response.json()

    def get_auth_status(self) -> dict:
        response = requests.post(self.url + "iserver/auth/status", verify=self.ssl)
        return response.json()

    def re_authenticate(self) -> None:
        response = requests.post(self.url + "iserver/reauthenticate", verify=self.ssl)
        print("Reauthenticating ...")

    def log_out(self) -> None:
        response = requests.post(self.url + "logout", verify=self.ssl)

    def get_bars(self, symbol: str, period="1w", bar="1d", outsideRth=False) -> dict:
        query = {
            "conid": self.get_conid(symbol),
            "period": period,
            "bar": bar,
            "outsideRth": outsideRth,
        }
        response = requests.get(
            self.url + "iserver/marketdata/history", params=query, verify=self.ssl
        )
        return response.json()


if __name__ == "__main__":

    api = REST()

    # print(api.reply_yes("a37bcc93-736b-441b-88a3-ee291d5dbcbd"))
    request = {
        "orders": [
            {
                "conid": api.get_conid("AAPL"),
                "orderType": "MKT",
                "side": "BUY",
                "quantity": 5,
                "tif": "GTC",
            }
        ]
    }
    # print(api.submit_order(request))
    print(api.get_portfolio())
    # print(api.re_authenticate())
    # print(api.get_auth_status())
    # print(api.get_order(2027388848))
    # print(api.get_bars("TSLA"))
    # print(api.get_conid("AAPL"))
    # print(api.cancel_order(2027388848))
