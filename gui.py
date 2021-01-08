from tkinter import *
from tkinter import messagebox
import ticker as t
from option_chain import OptionChain
from option_info import OptionInfo

# LONG-TERM TODO: preselect types of positions and auto pick options
#                give info on types of positions


# TODO: COMMENT EVERYTHING
#       Sort options by exp date (done) OR by strike (not done)
#       Highlight or underline selected/selectable options
class OptionGUI(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.ticker = None

        self.ticker_entry = Entry(self.master, width=9)
        self.ticker_string = StringVar()
        self.ticker_string.set('XYZ')
        self.ticker_entry['textvariable'] = self.ticker_string
        self.ticker_entry.bind('<Key-Return>', self.get_ticker)
        self.ticker_entry.grid(row=0, column=0, pady=10)

        self.selected_date = StringVar(value="option exp dates")
        self.selected_date.trace('w', self.fill_option_chain)
        self.date_choices = ['YYYY-MM-DD']
        self.date_menu = OptionMenu(self.master, self.selected_date, self.date_choices)
        self.date_menu.grid(row=0, column=1, columnspan=2, pady=10)

        # TODO: change to OptionMenu with option info items that are then plotted similar to price vs strike
        #       maybe keep price vs strike but add additional plot from selected item with right y-axis
        self.calls_label = Label(self.master, text='Call Price', width=10)
        self.strikes_label = Label(self.master, text='Strike', width=10)
        self.puts_label = Label(self.master, text='Put Price', width=10)
        self.calls_label.grid(row=1, column=0)
        self.strikes_label.grid(row=1, column=1)
        self.puts_label.grid(row=1, column=2)

        self.chain = OptionChain(self.master)
        self.chain.canvas.bind('<Button-1>', self._show_option_info)

        self.option_info = OptionInfo(self.master)

    def get_ticker(self, event):
        symbol = self.ticker_string.get()
        try:
            ticker = t.Ticker(symbol)
        except IndexError:
            messagebox.showerror(title="Error!", message="Invalid symbol '{}'".format(symbol))
        else:
            self.ticker = ticker
            self.fill_date_menu()

    def fill_date_menu(self):
        if not self.ticker:
            return

        self.ticker_string.set(self.ticker_string.get().upper())
        menu = self.date_menu['menu']
        menu.delete(0, 'end')
        for date in self.ticker.option_dates:
            menu.add_command(label=date, command=lambda value=date: self.selected_date.set(value))
        self.selected_date.set("{} exp dates".format(self.ticker_string.get()))

    def fill_option_chain(self, *args):
        if not self.ticker or self.selected_date.get().lower().islower():
            return
        self.chain.clear()

        try:
            self.ticker.get_option_chain(self.selected_date.get())
        except KeyError:
            messagebox.showerror(title="Error!", message="Could not get option chain")
            return
        self.chain.populate(self.ticker.calls, self.ticker.puts, self.ticker.stock_price)
        self.option_info.chain_plot(self.ticker.calls, self.ticker.puts, 'price')

    def _show_option_info(self, event):
        for tag in self.chain.click_tags():
            o = self.chain.option_from_tag(tag)
            if o:
                self.option_info.add_option(o)
                break


root = Tk()
test_app = OptionGUI(master=root)
test_app.mainloop()
