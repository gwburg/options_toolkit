from tkinter import *
from tkinter import messagebox


class OptionChain:
    def __init__(self, master=None):

        self.master = master
        self.chain_dict = {}

        self.scrollbar = Scrollbar(master=self.master)
        self.canvas = Canvas(self.master, width=250, height=600, yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=2, column=0, columnspan=3)
        self.scrollbar.grid(row=2, column=4, sticky='n' + 's')
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbound_to_mousewheel)

    def populate(self, calls, puts, stock_price):
        self.chain_dict = {}

        ic = ip = 0
        lc, lp = len(calls), len(puts)
        cx_i, cx_d, cy, cy_d, mid = 40, 85, 7, 23, 0

        while ic < lc and ip < lp:
            call = calls[ic]
            put = puts[ip]

            c_bg, p_bg = ('green', 'red') if call.strike < stock_price else ('red', 'green')
            if call.strike > stock_price and mid == 0:
                mid = cy

            if put.strike < call.strike or ic >= lc:
                self._add_option(None, put, x=cx_i, y=cy, d=cx_d, ccolor=c_bg, pcolor=p_bg)
                self.chain_dict[put.symbol] = put

                ip += 1
            elif call.strike < put.strike or ip >= lp:
                self._add_option(call, None, x=cx_i, y=cy, d=cx_d, ccolor=c_bg, pcolor=p_bg)
                self.chain_dict[call.symbol] = call

                ic += 1
            else:
                self._add_option(call, put, x=cx_i, y=cy, d=cx_d, ccolor=c_bg, pcolor=p_bg)
                self.chain_dict[put.symbol] = put
                self.chain_dict[call.symbol] = call

                ic += 1
                ip += 1
            cy += cy_d
        self.canvas.config(scrollregion=(0, 0, 250, cy + 10))
        self.canvas.yview_moveto(mid / cy - 0.07)

    def _add_option(self, call, put, **kwargs):
        ccolor = 'black' if 'ccolor' not in kwargs else kwargs['ccolor']
        pcolor = 'black' if 'pcolor' not in kwargs else kwargs['pcolor']

        try:
            x = kwargs['x']
            y = kwargs['y']
            d = kwargs['d']
        except KeyError:
            return

        cprice = '--' if call is None else '{:.2f}'.format(call.price)
        csym = None if call is None else call.symbol
        pprice = '--' if put is None else '{:.2f}'.format(put.price)
        psym = None if put is None else put.symbol
        strike = '{:.2f}'.format(call.strike) if call is not None else '{:.2f}'.format(put.strike)

        self.canvas.create_text(x, y, text=cprice, fill=ccolor, tags=csym)
        self.canvas.create_text(x+d, y, text=strike)
        self.canvas.create_text(x+2*d, y, text=pprice, fill=pcolor, tags=psym)

    def clear(self):
        self.canvas.delete('all')

    def _contains(self, o):
        return o in self.chain_dict

    def click_tags(self):
        return self.canvas.gettags('current')

    def option_from_tag(self, tag):
        if self._contains(tag):
            return self.chain_dict[tag]
        return None

    def _bound_to_mousewheel(self, event):
        self.master.bind_all('<Button-4>', self._on_mousewheel)
        self.master.bind_all('<Button-5>', self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.master.unbind_all('<Button-4>')
        self.master.unbind_all('<Button-5>')

    def _on_mousewheel(self, event):
        d = -2 if event.num == 4 else 2
        self.canvas.yview_scroll(d, 'units')
