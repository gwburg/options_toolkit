class Option:
    def __init__(self, o):
        self.symbol = o['contractSymbol']
        self.last_trade_date = o['lastTradeDate']
        self.strike = o['strike']
        self.price = o['lastPrice']
        self.bid = o['bid']
        self.ask = o['ask']
        self.price_change = o['change']
        self.percent_change = o['percentChange']
        self.volume = o['volume']
        self.open_interest = o['openInterest']
        self.iv = o['impliedVolatility']
        self.itm = o['inTheMoney']
        self.contract_size = o['contractSize']
        self.currency = o['currency']

        self.type = self._option_type(o)

    @staticmethod
    def _option_type(o):
        sym_done = False
        for c in o['contractSymbol']:
            if c.lower().islower():
                if sym_done:
                    return c.upper()
            else:
                if not sym_done:
                    sym_done = True
