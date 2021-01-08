from globals import *
from utilities import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
import matplotlib.ticker as mpl_ticker
from matplotlib.figure import Figure
''' have to use figure instead of pyplot because pyplot also makes
    a mainloop, etc which interferes with tkinter mainloop'''


# TODO: COMMENT EVERYTHING
#       make plot interactive -- this will probably take some doing
#       may be better to work on other things first
def all_strikes_plot(master, calls, puts, item, logscale=False):
    call_items = extract_options_chain_item(calls, item)
    put_items = extract_options_chain_item(puts, item)

    call_strikes = extract_options_chain_item(calls, 'strike')
    put_strikes = extract_options_chain_item(puts, 'strike')

    fig = Figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_position([0.15, 0.1, 0.82, 0.85])

    ax.plot(call_strikes, call_items, label='Calls')
    ax.plot(put_strikes, put_items, label="Puts")

    ax.set_xlabel('Strike')
    if item in ITEM_LABELS:
        ax.set_ylabel(ITEM_LABELS[item])
    if logscale:
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(mpl_ticker.FuncFormatter(lambda y, _: '{:.2f}'.format(y)))
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=master)
    return canvas.get_tk_widget()


# TODO: make fancier plot
#       add current stock price marker
#       add break even stock price marker
#       other stuff probably
def option_plot(master, xs, ys):
    fig = Figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_position([0.15, 0.1, 0.82, 0.85])
    ax.plot(xs, ys, 'b')

    canvas = FigureCanvasTkAgg(fig, master=master)
    return canvas.get_tk_widget()
