#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import sys
import tkinter as tk

from tkinter import ttk, font, messagebox

import numpy as np


class Dict(dict):
    def __getattr__(self, name):
        if name.startswith('__') or name not in self:
            return super().__getattr__(name)
        return self[name]

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

        self.flags = {}

        f = tk_nametofont('TkDefaultFont', self)
        w = 0
        for k, v in vals.items():
            x = ''
            w0 = 20
            if k != 'table':
                x = self.insert('', 'end', k, text=k)
                w0 = 40

            for iid, text in v:
                w1 = f.measure(text) + w0
                if w1 > w:
                    w = w1
                self.insert(x, 'end', iid, text=text)

        self.column('#0', width=w, anchor='e', stretch=tk.NO)
        self.column('x', width=10, stretch=tk.NO)

        self.vsb = AutoScrollbar(self.master, orient='vertical', command=self.yview)
        self.configure(yscrollcommand=self.vsb.set)
        self.hsb = AutoScrollbar(self.master, orient='horizontal', command=self.xview)
        self.configure(xscrollcommand=self.hsb.set)

    def fill(self, tlm, fw_max=10):
        f = tk_nametofont('TkDefaultFont', self)
        for k, v in tlm.items():
            if k.startswith('flags'):
                fw_max = self.fill(v, fw_max)
            elif not k.startswith('_'):
                if self.exists(k):
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
        table = self.tlm_tables[tlm._name]
        table.fill(tlm)

        for i in self.tlm_tables.values():
            i.grid_forget()
            i.vsb.grid_forget()
            i.hsb.grid_forget()

        table.grid(column=0, row=0, sticky=tk.NSEW)
        table.vsb.grid(column=1, row=0, sticky=tk.NSEW)
        table.hsb.grid(column=0, row=1, sticky=tk.NSEW)

        self.tlm_name_l.config(text=filename)


class DynamicNotebook(ttk.Notebook):
    """
    A ttk Notebook with close buttons on each tab and `new` button to create tabs,
    also reorder tabs by drag & drop
    From: https://stackoverflow.com/a/39459376
          https://stackoverflow.com/a/71861284
          https://stackoverflow.com/a/69224344

    """

    __initialized = 0

    def __init__(self, master, new_tab_fn, **kw):
        if not self.__initialized:
            self.__initialize_style()
            self.__inititialized = 1

        kw['style'] = 'DynamicNotebook'
        ttk.Notebook.__init__(self, master, **kw)
        self._create_new_tab = new_tab_fn

        self._active = None

        self.add(ttk.Frame(), text='+')

        self.bind('<ButtonPress-1>', self._press_action, '+')
        self.bind('<ButtonPress-2>', self._press_action, '+')
        self.bind('<ButtonRelease-1>', self._release_action)
        self.bind('<ButtonRelease-2>', self._release_action)
        self.bind('<<NotebookTabChanged>>', self._tab_action)
        self.bind('<B1-Motion>', self._reorder)

    def add(self, child, **kw):
        idx = len(self.tabs())
        if idx:
            return self.insert(idx - 1, child, **kw)
        return super().add(child, **kw)

    def _press_action(self, evt=None):
        """Called when the button is pressed over the close button"""

        _id = self.identify(evt.x, evt.y)
        if _id and len(self.tabs()) == 1 and evt.num == 1:
            self._tab_action()

        elif (evt.num == 2 and _id) or 'close' in _id:
            index = self.index('@%d,%d' % (evt.x, evt.y))
            self.state(['pressed'])
            self._active = index
            return 'break'


    def _release_action(self, evt=None):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        _id = self.identify(evt.x, evt.y)
        if not ((evt.num == 2 and _id) or 'close' in _id):
            # user moved the mouse off of the close button
            self.state(['!pressed'])
            return

        clo_idx = self.index('@%d,%d' % (evt.x, evt.y))
        if (clo_idx != len(self.tabs()) - 1
                and self._active == clo_idx
                and messagebox.askyesno('Close tab?', 'Are you sure you want to close the tab?')):
            cur_idx = self.tabs().index(self._last_selected)
            if clo_idx == cur_idx and cur_idx == len(self.tabs()) - 2:
                if cur_idx:
                    cur_idx -= 1
                self.select(cur_idx)
            self.forget(clo_idx)
            self.event_generate('<<NotebookTabClosed>>')

        self.state(['!pressed'])
        self._active = None

    def _tab_action(self, evt=None):
        self._last_selected = self.select()
        if self._last_selected == self.tabs()[-1]:
            index = len(self.tabs()) - 1
            x = self._create_new_tab()
            if not x:
                return
            frame, name = x
            self.insert(index, frame, text=name)
            self.select(index)

    def _reorder(self, evt=None):
        try:
            self.insert(self.index(f'@{evt.x},{evt.y}'), child=self.select())
        except tk.TclError:
            pass

    @classmethod
    def __initialize_style(cls):
        style = ttk.Style()
        cls._images = (
            # normal
            tk.PhotoImage(data='R0lGODlhCAAIAMIAAAAAADs7O4+Pj9nZ2QAAAAAAAAAAAAAAACH5BAEKAAQALAAAAAAIAAgAAAMV'
                               'GDBEA0qNJyGw7AmxmuaZhWEU5kEJADs='),
            # pressed
            tk.PhotoImage(data='R0lGODlhCAAIAMIAAAAAADs7O4+Pj9nZ2QAAAAAAAAAAAAAAACH5BAEKAAMALAAAAAAIAAgAAAMU'
                               'GCAzAkqJJyGwjMqml7MYRmEclAAAOw=='),
            # active
            # tk.PhotoImage(data='R0lGODlhCAAIAMIAAAAAAP/SAP/bNNnZ2QAAAAAAAAAAAAAAACH5BAEKAAQALAAAAAAIAAgAAAMV'
            #                    'GDBEA0qNJyGw7AmxmuaZhWEU5kEJADs='),
        )

        style.element_create('close', 'image', cls._images[0],
                             ('active', 'pressed', '!disabled', cls._images[1]),
                             # ('active', '!disabled', self.images[2]),
                             border=8, sticky='')
        style.layout('DynamicNotebook', [('DynamicNotebook.client', dict(sticky=tk.NSEW))])
        style.layout('DynamicNotebook.Tab', [
            ('DynamicNotebook.tab', dict(
                sticky=tk.NSEW, children=[
                    ('DynamicNotebook.padding', dict(side=tk.TOP, sticky=tk.NSEW, children=[
                        ('DynamicNotebook.focus', dict(side=tk.TOP, sticky=tk.NSEW, children=[
                            ('DynamicNotebook.label', dict(side=tk.LEFT, sticky='')),
                            ('DynamicNotebook.close', dict(side=tk.LEFT, sticky='')),
                        ]))
                    ]))
                ]
            ))
        ])


def bytes2hex(data):
    return data.hex(*((' ',) if sys.version_info >= (3, 8, 0) else ()))


def tk_nametofont(name, root=None):
    """
    Override `tk.font.nametofont`
    in python<3.10 `root` keyword is not exist
    """
    return font.Font(name=name, exists=True, root=root)


def bayer2rgb(data, mode, w, h):
    in_dtype = data.dtype
    ow, oh = w // 2, h // 2
    data = data.reshape((h, w))
    layers = (
        data[0::2, 0::2],  # rows 0,2,4,6 columns 0,2,4,6
        data[0::2, 1::2],  # rows 0,2,4,6 columns 1,3,5,7
        data[1::2, 0::2],  # rows 1,3,5,7 columns 0,2,4,6
        data[1::2, 1::2],  # rows 1,3,5,7 columns 1,3,5,7
    )

    if mode == 'rggb':
        r, g0, g1, b = layers
    elif mode == 'gbrg':
        g0, b, r, g1 = layers
    elif mode == 'grbg':
        g0, r, b, g1 = layers
    elif mode == 'bggr':
        b, g0, g1, r = layers
    else:
        raise ValueError('Invali mode')

    zh = np.full((oh, ow), np.nan, np.float32)
    zv = np.full((oh, w), np.nan, np.float32)

    if mode == 'rggb':
        layers = [r, g0, g1, b]
    elif mode == 'gbrg':
        layers = [g0, b, r, g1]
    elif mode == 'grbg':
        layers = [g0, r, b, g1]
    elif mode == 'bggr':
        layers = [b, g0, g1, r]

    x = np.dstack((layers[0], zh)).reshape(layers[0].shape[0], -1)
    layers[0] = np.stack((x, zv), 1).reshape(-1, x.shape[1])

    x = np.dstack((zh, layers[1])).reshape(layers[1].shape[0], -1)
    layers[1] = np.stack((x, zv), 1).reshape(-1, x.shape[1])

    x = np.dstack((layers[2], zh)).reshape(layers[2].shape[0], -1)
    layers[2] = np.stack((zv, x), 1).reshape(-1, x.shape[1])

    x = np.dstack((zh, layers[3])).reshape(layers[3].shape[0], -1)
    layers[3] = np.stack((zv, x), 1).reshape(-1, x.shape[1])

    zh = np.full((1, w), np.nan, np.float32)
    zv = np.full((h + 2, 1), np.nan, np.float32)
    for i, l in enumerate(layers):
        a = np.hstack((zv, np.vstack((zh, l, zh)), zv))
        n = a.ndim
        w = np.lib.stride_tricks.sliding_window_view(a, (3, 3))
        layers[i] = np.nansum(w, axis=(n, n + 1)) / np.count_nonzero(~np.isnan(w), axis=(n, n + 1))

    if mode == 'rggb':
        r, g0, g1, b = layers
    elif mode == 'gbrg':
        g0, b, r, g1 = layers
    elif mode == 'grbg':
        g0, r, b, g1 = layers
    elif mode == 'bggr':
        b, g0, g1, r = layers

    g = g0 // 2 + g1 // 2

    return np.dstack((r, g, b)).astype(in_dtype)


seqs_map = {
    '\x72\x73\x32\x30\x73': 'aHR0cHM6Ly91cGxvYWQud2lraW1lZGlhLm9yZy93aWtpcGVkaWEvY29tbW9u'
                            'cy90aHVtYi80LzRhL0N1YmVTYXRfR2Vvc2Nhbi1FZGVsdmVpc19lbWJsZW0u'
                            'anBnLyVzcHgtQ3ViZVNhdF9HZW9zY2FuLUVkZWx2ZWlzX2VtYmxlbS5qcGc=',
    '\x72\x73\x31\x35\x73': 'aHR0cHM6Ly9zcHV0bml4LnJ1L3RwbC9pbWcvbG9nby16b3JraXkuanBnPyVz',
}
