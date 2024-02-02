import sys
import tkinter as tk

from tkinter import ttk, font


class Dict(dict):
    def __getattr__(self, name):
        return super().__getattr__(name) if name.startswith('__') else self[name]

    def __setattr__(self, name, value):
        if name.startswith('__'):
            super().__setattr__(name, value)
        else:
            self[name] = value

    def __delattr__(self, name):
        if name.startswith('__'):
            super().__delattr__(name)
        else:
            del self[name]


class AutoScrollbar(ttk.Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        super().set(lo, hi)


class TlmCommonTable(ttk.Treeview):
    def __init__(self, master, vals):
        super().__init__(master, columns='x val', selectmode='browse', show='tree')

        self.column('#0', anchor='e', stretch=tk.NO)
        self.column('x', width=10, stretch=tk.NO)
        self.flags = {}

        for k, v in vals.items():
            x = ''
            if k != 'table':
                x = self.insert('', 'end', k, text=k)

            for iid, text in v:
                self.insert(x, 'end', iid, text=text)

        self.vsb = AutoScrollbar(self.master, orient='vertical', command=self.yview)
        self.configure(yscrollcommand=self.vsb.set)
        self.hsb = AutoScrollbar(self.master, orient='horizontal', command=self.xview)
        self.configure(xscrollcommand=self.hsb.set)

    def fill(self, tlm, fw_max=10):
        f = font.nametofont('TkDefaultFont', self)
        for k, v in tlm.items():
            if k.startswith('flags'):
                fw_max = self.fill(v, fw_max)
            elif not k.startswith('_'):
                self.set(k, 'val', str(v))
                x = f.measure(str(v))
                if x > fw_max:
                    fw_max = x

        self.column('val', minwidth=fw_max + 10)
        return fw_max


class TlmCommonFrame(ttk.Frame):
    def __init__(self, master, vals):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.tlm_tables = {}

        for k, v in vals.items():
            self.tlm_tables[k] = TlmCommonTable(self, v)

        self.tlm_name_l = ttk.Label(self)
        self.tlm_name_l.grid(row=3, column=0, sticky=tk.EW, pady=3)

    def fill(self, tlm, filename):
        table = self.tlm_tables[tlm.name]
        table.fill(tlm)

        for i in self.tlm_tables.values():
            i.grid_forget()
            i.vsb.grid_forget()
            i.hsb.grid_forget()

        table.grid(column=0, row=0, sticky=tk.NSEW)
        table.vsb.grid(column=1, row=0, sticky=tk.NSEW)
        table.hsb.grid(column=0, row=1, sticky=tk.NSEW)

        self.tlm_name_l.config(text=filename)


def bytes2hex(data):
    return data.hex(*((' ',) if sys.version_info >= (3, 8, 0) else ()))


seqs_map = {
    '\x72\x73\x32\x30\x73': 'aHR0cHM6Ly91cGxvYWQud2lraW1lZGlhLm9yZy93aWtpcGVkaWEvY29tbW9u'
                            'cy90aHVtYi80LzRhL0N1YmVTYXRfR2Vvc2Nhbi1FZGVsdmVpc19lbWJsZW0u'
                            'anBnLyVzcHgtQ3ViZVNhdF9HZW9zY2FuLUVkZWx2ZWlzX2VtYmxlbS5qcGc=',
    '\x72\x73\x31\x35\x73': 'aHR0cHM6Ly9zcHV0bml4LnJ1L3RwbC9pbWcvbG9nby16b3JraXkuanBnPyVz',
}
