from globals import *
from tkinter import *
import option_plots as oplts


# TODO: add menu showing selected options
#       make options removable
#       choose between building multi-option position or looking at singles
#       add clear button to remove all options
class OptionInfo:
    def __init__(self, master):

        self.master = master
        self.current_option = None
        self.selected_options = []
        self.strikes = []
        self.values = []

        self.plot = Canvas(self.master, width=600, height=600, borderwidth=1, relief='solid')
        self.plot.grid(row=2, column=5, columnspan=4)

        # TODO: generalize
        self.strike = Label(self.master)
        self.strike.grid(row=0, column=5)
        self.lastPrice = Label(self.master)
        self.lastPrice.grid(row=0, column=6)
        self.bid = Label(self.master)
        self.bid.grid(row=0, column=7)
        self.ask = Label(self.master)
        self.ask.grid(row=0, column=8)
        self.percentChange = Label(self.master)
        self.percentChange.grid(row=1, column=5)
        self.volume = Label(self.master)
        self.volume.grid(row=1, column=6)
        self.openInterest = Label(self.master)
        self.openInterest.grid(row=1, column=7)
        self.impliedVolatility = Label(self.master)
        self.impliedVolatility.grid(row=1, column=8)

    def add_option(self, option):
        self.current_option = option
        self._insert_option(option)
        self.update_info()

    def _insert_option(self, option):
        if not self.selected_options:
            self.selected_options.append(option)
        else:
            index = 0
            for i, o in enumerate(self.selected_options):
                if o.strike > option.strike:
                    index = i
                    break
                elif i == len(self.selected_options) - 1:
                    index = i + 1
                    break
            self.selected_options.insert(index, option)

    def update_info(self):
        self.show_option_info()
        self.update_plot_points()
        self.option_plot()

    def chain_plot(self, calls, puts, yvar):
        plot = oplts.all_strikes_plot(self.master, calls, puts, yvar, logscale=True)
        self.update_plot(plot)

    def option_plot(self):
        plot = oplts.option_plot(self.master, self.strikes, self.values)
        self.update_plot(plot)

    def update_plot_points(self):
        strike = self.current_option.strike
        price = self.current_option.price
        delta = 0.1
        otype = self.current_option.type
        if not self.strikes:
            self.strikes.append(strike * (1 - delta))
            self.strikes.append(strike)
            self.strikes.append(strike * (1 + delta))

            self.values = [0] * len(self.strikes)
            self.values[1] = -price
            itm = strike * delta - price
            otm = -price
            self.values[0], self.values[2] = (otm, itm) if otype == 'C' else (itm, otm)

        else:
            for i, x in enumerate(self.strikes):
                if i == 0:
                    continue
                if x == strike:
                    break
                # TODO: should be some way of combining these two
                elif x > strike:
                    y_new = self._polate(self.strikes[i-1], self.values[i-1], self.strikes[i], self.values[i], strike)
                    if i == 1:
                        self.values[0] = self._polate(self.strikes[i-1], self.values[i-1], self.strikes[i],
                                                      self.values[i], strike*(1-delta))
                        self.strikes[0] = strike*(1-delta)
                    self.strikes.insert(i, strike)
                    self.values.insert(i, y_new)
                    break
                elif x == self.strikes[-2]:
                    y_new = self._polate(self.strikes[i], self.values[i], self.strikes[i+1], self.values[i+1], strike)
                    self.values[-1] = self._polate(self.strikes[i], self.values[i], self.strikes[i+1],
                                                   self.values[i+1], strike*(1+delta))
                    self.strikes[-1] = strike*(1+delta)
                    self.strikes.insert(i+1, strike)
                    self.values.insert(i+1, y_new)
                    break

            self._add_y_value(strike, price)

    def _add_y_value(self, strike, price):
        for i, y in enumerate(self.values):
            itm = (self.current_option.type == 'C' and self.strikes[i] > strike) or \
                  (self.current_option.type == 'P' and self.strikes[i] < strike)
            if itm:
                self.values[i] += abs(strike - self.strikes[i]) - price
            else:
                self.values[i] += -price

    @staticmethod
    def _polate(x1, y1, x2, y2, x_new):
        slope = (y2-y1)/(x2-x1)
        return y2 - slope * (x2-x_new)

    # TODO: make better/more elegant
    def show_option_info(self):
        if self.current_option:
            self.strike.config(text=ITEM_LABELS['strike'] + ': ' + str(self.current_option.strike))
            self.lastPrice.config(text=ITEM_LABELS['lastPrice'] + ': ' + str(self.current_option.price))
            self.bid.config(text=ITEM_LABELS['bid'] + ': ' + str(self.current_option.bid))
            self.ask.config(text=ITEM_LABELS['ask'] + ': ' + str(self.current_option.ask))
            self.percentChange.config(text=ITEM_LABELS['percentChange'] + ': ' +
                                      '{:+.0f}%'.format(self.current_option.percent_change))
            self.volume.config(text=ITEM_LABELS['volume'] + ': ' + '{:.0f}'.format(self.current_option.volume))
            self.openInterest.config(text=ITEM_LABELS['openInterest'] + ': ' +
                                     '{:.0f}'.format(self.current_option.open_interest))
            self.impliedVolatility.config(text=ITEM_LABELS['impliedVolatility'] + ': ' +
                                          '{:.0%}'.format(self.current_option.iv))

    def update_plot(self, plot):
        temp = self.plot
        self.plot = plot
        self.plot.grid(row=2, column=5, columnspan=4)
        temp.destroy()

    def clear(self):
        self.current_option = None
        self.selected_options = []
        self.strikes = []
        self.values = []
