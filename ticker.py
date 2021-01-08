import yfinance as yf
import datetime
from option import Option


# TODO: COMMENT EVERYTHING
class Ticker:
    def __init__(self, symbol):
        self.ticker = yf.Ticker(symbol)
        # TODO: better way of handling this?
        #       check Raymond Hettinger context manager
        self._option_dates_wrong = self.ticker.options
        self.option_dates = self._fix_dates()

        self.stock_price = self.ticker.history().iat[-1, 3]

        self.calls = []
        self.puts = []

    def update_stock_price(self):
        self.stock_price = self.ticker.history().iat[-1, 3]

    # TODO: find better way to convert panda to list of Option objects
    def get_option_chain(self, date):
        date = self._subtract_day(date)
        self.calls = []
        self.puts = []
        if date in self._option_dates_wrong:
            _calls = self.ticker.option_chain(date).calls.to_dict(orient='records')
            _puts = self.ticker.option_chain(date).puts.to_dict(orient='records')

            for c in _calls:
                self.calls.append(Option(c))
            for p in _puts:
                self.puts.append(Option(p))
            return self.calls, self.puts
        else:
            return ()

    def _fix_dates(self):
        fixed_option_dates = []
        for option_date in self._option_dates_wrong:
            y, m, d = option_date.split('-')
            date = datetime.date(int(y), int(m), int(d))
            date += datetime.timedelta(days=1)
            fixed_option_dates.append('{}-{:02}-{:02}'.format(date.year, date.month, date.day))
        return tuple(fixed_option_dates)

    @staticmethod
    def _subtract_day(date):
        y, m, d = date.split('-')
        new_date = datetime.date(int(y), int(m), int(d))
        new_date -= datetime.timedelta(days=1)
        return '{}-{:02}-{:02}'.format(new_date.year, new_date.month, new_date.day)
