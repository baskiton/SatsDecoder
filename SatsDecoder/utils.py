#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import datetime as dt
import enum
import errno
import json
import math
import struct
import sys
import tkinter as tk

from tkinter import ttk, font, messagebox

import construct
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import PIL
import PIL.Image

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ConnMode(enum.IntEnum):
    # !!! only append !!!

    AGWPE_CLI = 0
    TCP_CLI = enum.auto()
    TCP_SRV = enum.auto()
    HEX = enum.auto()
    KISS_FILES = enum.auto()
    SATDUMP_FRM = enum.auto()
    HEX_FILES = enum.auto()
    JSON_FILES = enum.auto()
    KISS_TCP_CLI = enum.auto()


con_mode_names = {
    ConnMode.AGWPE_CLI: 'AGWPE Client',
    ConnMode.TCP_CLI: 'TCP Client',
    ConnMode.TCP_SRV: 'TCP Server',
    ConnMode.HEX: 'HEX values',
    ConnMode.HEX_FILES: 'HEX values from files',
    ConnMode.JSON_FILES: 'JSON files',
    ConnMode.KISS_FILES: 'KISS files',
    ConnMode.KISS_TCP_CLI: 'KISS TCP Client',
    ConnMode.SATDUMP_FRM: 'SatDump frm files',
}
con_mode_names_inv = {v: k for k, v in con_mode_names.items()}


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
        super().__init__(master, columns='x val', selectmode=tk.BROWSE, show='tree')

        self.flags = {}

        f = tk_nametofont('TkDefaultFont', self)
        w = 0
        for k, v in vals.items():
            x = ''
            w0 = 20
            if k != 'table':
                x = self.insert('', tk.END, k, text=k)
                w0 = 40

            for iid, text, _ in v:
                w1 = f.measure(text) + w0
                if w1 > w:
                    w = w1
                self.insert(x, tk.END, iid, text=text)

        self.column('#0', width=w, anchor=tk.E, stretch=tk.NO)
        self.column('x', width=10, stretch=tk.NO)

        self.vsb = AutoScrollbar(self.master, orient=tk.VERTICAL, command=self.yview)
        self.hsb = AutoScrollbar(self.master, orient=tk.HORIZONTAL, command=self.xview)
        self.configure(
            yscrollcommand=self.vsb.set,
            xscrollcommand=self.hsb.set,
        )

    def fill(self, tlm, f_precision, fw_max=10):
        f = tk_nametofont('TkDefaultFont', self)
        for k, v in tlm.items():
            if k.startswith('flags'):
                fw_max = self.fill(v, f_precision, fw_max)
            elif isinstance(v, construct.ListContainer):
                fw_max = self.fill({k: list(v)}, f_precision, fw_max)
            elif isinstance(v, construct.Container):
                fw_max = self.fill({k + '/' + kk: vv for kk, vv in v.items()}, f_precision, fw_max)
            elif not k.startswith('_'):
                if self.exists(k):
                    if isinstance(v, float):
                        s_v = str(round(v, f_precision))
                    elif isinstance(v, list) and isinstance(v[0], float):
                        s_v = str([round(i, f_precision) for i in v])
                    else:
                        s_v = str(v)
                    self.set(k, 'val', s_v)
                    x = f.measure(s_v)
                    if x > fw_max:
                        fw_max = x

        self.column('val', minwidth=fw_max + 10)
        return fw_max


class TlmPlotFrame(ttk.Frame):
    def __init__(self, master, vals):
        super().__init__(master)
        self.valid = 1

        if not any(sub[0] == 'Time' for sub in vals['table'] if sub):
            self.valid = 0
            return

        self.table = [] # (iid, title, plot, gid)
        gid = 0

        for iid, title, plot in vals['table']:
            if plot == 0:   # don't draw
                continue
            if plot == 1:   # new group
                gid += 1
            # else use previous group
            self.table.append((iid, title, plot, gid))

        self.time_data = {}

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self)
        self.canvas.grid(column=0, row=0, sticky=tk.NSEW)

        self.vsb = AutoScrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky=tk.NS)
        # self.hsb = AutoScrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        # self.hsb.grid(row=1, column=0, sticky=tk.EW)
        self.canvas.configure(
            yscrollcommand=self.vsb.set,
            # xscrollcommand=self.hsb.set,
            scrollregion=self.canvas.bbox(tk.ALL),
        )

        self.plot_frame = ttk.Frame(self.canvas)
        dpi = 100
        single_plot_height = 2
        groups_cnt = gid
        fig_height = single_plot_height * groups_cnt
        self.h_pix = int(fig_height * dpi)
        self.plot_frame.configure(height=self.h_pix)
        self.plot_frame.grid_propagate(False)
        self.plot_window = self.canvas.create_window((0, 0), window=self.plot_frame, anchor=tk.NW)
        self.plot_frame.columnconfigure(0, weight=1)
        self.plot_frame.rowconfigure(0, weight=1)
        self.plot_frame.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        self.fig, self.ax = plt.subplots(
            groups_cnt, 1,
            sharex=True,
            figsize=(10, fig_height),
            dpi=dpi,
            constrained_layout=True,
        )
        if hasattr(self.fig, 'set_layout_engine'):
            self.fig.set_layout_engine('constrained', h_pad=0.1, w_pad=0.1)
        else:
            self.fig.set_constrained_layout(True)
            self.fig.set_constrained_layout_pads(h_pad=0.1, w_pad=0.1)

        self.lines = {}         # gid: list of lines
        self.scatters = {}      # gid: list of scatters
        self.last_points = {}   # gid: list of last_points

        colors = 'bgrcmy'
        color_i = 0
        markers = 'ov^<>sP*+xD'
        marker_i = 0
        self.legend_params = dict(loc='best', fontsize=8)

        groups_data = {}
        for i in self.table:
            groups_data.setdefault(i[3], []).append(i)

        for idx, gid in enumerate(sorted(groups_data.keys())):
            ii = groups_data[gid]
            ax = self.ax[idx]

            self.lines[gid] = []
            self.scatters[gid] = []
            self.last_points[gid] = []

            for iid, title, _, _ in ii:
                color = colors[color_i % len(colors)]
                color_i += 1
                marker = markers[marker_i % len(markers)]
                marker_i += 1

                line, = ax.plot([], [], color=color, linewidth=0.75)
                self.lines[gid].append(line)

                scatter = ax.scatter([], [], color=color, s=15, zorder=5, marker=marker, label=title)
                self.scatters[gid].append(scatter)

                last_point = ax.scatter([], [], color=color, s=30, zorder=6, marker=marker)
                self.last_points[gid].append(last_point)

            ax.set_title(ii[0][1])
            ax.grid(True)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S\n%Y-%m-%d'))
            ax.tick_params(axis='both', labelsize=8)
            ax.legend(**self.legend_params)

        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.plot_widget = self.plot_canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0, sticky=tk.NSEW)

        for i in (self.plot_widget, self.canvas):
            for e in ('<MouseWheel>', '<Button-4>', '<Button-5>'):
                i.bind(e, self._on_mousewheel)

    def _on_mousewheel(self, evt=None):
        n = 0
        if hasattr(evt, 'num') and evt.num in (4, 5):
            # Linux: Button-4 (up > -1), Button-5 (down > 1)
            n = evt.num * 2 - 9

        elif hasattr(evt, 'delta') and evt.delta:
            # Windows/macOS: positive delta = up
            n = -int(math.copysign(1, evt.delta))

        self.canvas.yview_scroll(n, 'units')
        return 'break'

    def _on_frame_configure(self, evt=None):
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    def _on_canvas_configure(self, evt=None):
        self.canvas.itemconfig(
            self.plot_window,
            width=evt.width,
            height=self.plot_frame.winfo_reqheight(),
        )

    def clear(self):
        self.time_data.clear()
        for gid in self.lines:
            for i in self.lines[gid]:
                i.set_data([], [])
            for i in self.scatters[gid]:
                i.set_offsets(np.empty((0, 2)))
            for i in self.last_points[gid]:
                i.set_offsets(np.empty((0, 2)))
        for ax in self.ax:
            ax.relim()
            ax.autoscale_view()
        for ax in self.ax:
            ax.legend(**self.legend_params)
        self.plot_canvas.draw_idle()

    def fill(self, tlm):
        t = tlm.get('Time')
        if not t:
            return

        params = {}
        for i in self.table:
            iid = i[0]
            params[iid] = tlm[iid]

        self.time_data[t] = params
        sorted_times = list(sorted(self.time_data))

        for gid in self.lines:
            for i, (iid, _, _, _) in enumerate(i for i in self.table if i[3] == gid):
                sorted_data = [self.time_data[t][iid] for t in sorted_times]

                self.lines[gid][i].set_data(sorted_times, sorted_data)
                self.scatters[gid][i].set_offsets(list(zip(sorted_times, sorted_data)))
                self.last_points[gid][i].set_offsets([(t, params[iid])])

        for i, gid in enumerate(sorted(self.lines.keys())):
            self.ax[i].relim()
            self.ax[i].autoscale_view()
            self.ax[i].legend(**self.legend_params)

        self.plot_canvas.draw_idle()

    def fill_full(self, tlms):
        for tlm in tlms:
            t = tlm.get('Time')
            if not t:
                continue

            params = {}
            for i in self.table:
                iid = i[0]
                params[iid] = tlm[iid]

            self.time_data[t] = params

        sorted_times = list(sorted(self.time_data))

        for gid in self.lines:
            for i, (iid, _, _, _) in enumerate(i for i in self.table if i[3] == gid):
                sorted_data = [self.time_data[t][iid] for t in sorted_times]

                self.lines[gid][i].set_data(sorted_times, sorted_data)
                self.scatters[gid][i].set_offsets(list(zip(sorted_times, sorted_data)))
                self.last_points[gid][i].set_offsets([(sorted_times[-1], sorted_data[-1])])

        for i, gid in enumerate(sorted(self.lines.keys())):
            self.ax[i].relim()
            self.ax[i].autoscale_view()
            self.ax[i].legend(**self.legend_params)

        self.plot_canvas.draw_idle()


class TlmCommonFrame(ttk.Frame):
    def __init__(self, master, tlm_table):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.tlm_table = tlm_table
        self.tlm_tables = {}
        self.plot_frames = {}
        self.last_tlm = None

        self.info_frm = ttk.Frame(self)
        self.info_frm.columnconfigure(0, weight=1)
        self.info_frm.grid(row=3, column=0, sticky=tk.EW, pady=3)

        self.tlm_name_l = ttk.Label(self.info_frm)
        self.tlm_name_l.grid(row=0, column=0, sticky=tk.EW, pady=3)

        ttk.Separator(self.info_frm, orient=tk.VERTICAL).grid(row=0, column=1, sticky=tk.NS, pady=3, padx=3)

        self.mode = 0
        self.switch_mode_b = ttk.Button(self.info_frm, text='Chart', command=self.switch_mode)
        self.switch_mode_b.grid(row=0, column=2, sticky=tk.E, pady=3, padx=3)

        ttk.Label(self.info_frm, text='Float precision:').grid(row=0, column=3, sticky=tk.E, pady=3)
        self.float_precision_v = tk.IntVar(self, 10)
        self.float_precision = ttk.Spinbox(self.info_frm, from_=0, to=100, width=3,
                                           textvariable=self.float_precision_v, command=self.float_review)
        self.float_precision.grid(row=0, column=4, sticky=tk.E, pady=3)

    def clear(self):
        self.child_forget(self.last_tlm._name if self.last_tlm else '')
        for i in self.plot_frames.values():
            i.clear()

    def child_forget(self, tlm_name):
        if tlm_name:
            i = self.plot_frames.get(tlm_name)
            if i and i.valid:
                i.grid_forget()
            i = self.tlm_tables.get(tlm_name)
            if i:
                i.grid_forget()
                i.vsb.grid_forget()
                i.hsb.grid_forget()

    def show_table(self, tlm):
        table = self.tlm_tables.get(tlm._name)
        if not table:
            table = TlmCommonTable(self, self.tlm_table[tlm._name])
            self.tlm_tables[tlm._name] = table

        table.fill(tlm, self.float_precision_v.get())
        table.grid(column=0, row=0, sticky=tk.NSEW)
        table.vsb.grid(column=1, row=0, sticky=tk.NSEW)
        table.hsb.grid(column=0, row=1, sticky=tk.NSEW)

    def get_plot(self, tlm_name):
        plot = self.plot_frames.get(tlm_name)
        if not plot:
            plot = TlmPlotFrame(self, self.tlm_table[tlm_name])
            self.plot_frames[tlm_name] = plot
        return plot

    def fill_plot(self, tlm, fully=()):
        names = {}
        for i in fully:
            names.setdefault(i._name, []).append(i)

        for name, tlms in names.items():
            plot = self.get_plot(name)
            if plot.valid:
                plot.fill_full(tlms)

        plot = self.get_plot(tlm._name)
        if plot.valid:
            plot.fill(tlm)

    def show_plot(self, tlm_name):
        plot = self.get_plot(tlm_name)
        if plot.valid:
            plot.grid(column=0, row=0, sticky=tk.NSEW)

    def fill(self, tlm, filename, fully=()):
        try:
            old_tlm_name = self.last_tlm._name
        except AttributeError:
            old_tlm_name = ''

        self.child_forget(old_tlm_name)
        if fully:
            self.fill_plot(tlm, fully)
        if self.mode:
            if not fully:
                self.fill_plot(tlm)
            self.show_plot(tlm._name)
        else:
            self.show_table(tlm)

        self.last_tlm = tlm
        self.tlm_name_l.config(text=filename and filename.name)

    def float_review(self):
        table = self.tlm_tables[self.last_tlm._name]
        table.fill(self.last_tlm, self.float_precision_v.get())

    def switch_mode(self):
        self.mode ^= 1
        self.switch_mode_b.config(text='Tlm' if self.mode else 'Chart')

        self.child_forget(self.last_tlm._name)
        if self.mode:
            self.show_plot(self.last_tlm._name)
        else:
            self.show_table(self.last_tlm)


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


def recvall(conn, n):
    ret = bytearray()
    while len(ret) < n:
        try:
            x = conn.recv(n - len(ret))
            if not x:
                return b''
        except OSError as e:
            if e.errno in (errno.EAGAIN, errno.EWOULDBLOCK, sys.platform == 'win32' and errno.WSAEWOULDBLOCK):
                continue
            raise
        ret.extend(x)
    return bytes(ret)


def nonblocking_message(type_, title=None, message=None, detail=None, parent=None):
    if type_ == messagebox.ERROR:
        img = '::tk::icons::error'
    elif type_ == messagebox.WARNING:
        img = '::tk::icons::warning'
    elif type_ == messagebox.INFO:
        img = '::tk::icons::information'
    else:
        raise ValueError(f'Invalid message type: {type_}')

    top = tk.Toplevel(parent)
    top.transient(parent)
    top.focus_set()
    top.wait_visibility()
    top.grab_set()
    top.resizable(width=False, height=False)
    top.title(title or type_.capitalize())

    frame = ttk.Frame(top, padding=(10, 6, 10, 6))
    frame.grid(column=0, row=0, sticky=tk.NSEW)

    ttk.Label(frame, image=img, justify=tk.LEFT).grid(column=0, row=0)
    ttk.Label(frame, text=message or '', font='TkCaptionFont').grid(column=1, row=0)
    if detail:
        ttk.Label(frame, text=detail).grid(columnspan=2, column=0, row=1)

    ok_btn = ttk.Button(frame, text='Ok', command=lambda: (top.grab_release(), top.destroy()))
    ok_btn.grid(columnspan=2, column=0, row=2)

    top.update()


def bytes2hex(data):
    return data.hex(*((' ',) if sys.version_info >= (3, 8, 0) else ()))


def tk_nametofont(name, root=None):
    """
    Override `tk.font.nametofont`
    in python<3.10 `root` keyword is not exist
    """
    return font.Font(name=name, exists=True, root=root)


def bayer2rgb(data, mode):
    in_dtype = data.dtype
    h, w = data.shape
    ow, oh = w // 2, h // 2
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
        raise ValueError('Invalid mode')

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


_GPS_BORN = dt.datetime(1980, 1, 6) + dt.timedelta(seconds=19)

def gps_to_utc(week, sec):
    """
    https://hpiers.obspm.fr/eop-pc/index.php?index=TAI-UTC_tab&lang=en
    """

    x = _GPS_BORN + dt.timedelta(weeks=week)
    # leaked seconds
    if x < dt.datetime(year=1981, month=7, day=1):
        sec -= 19
    elif x < dt.datetime(year=1982, month=7, day=1):
        sec -= 20
    elif x < dt.datetime(year=1983, month=7, day=1):
        sec -= 21
    elif x < dt.datetime(year=1985, month=7, day=1):
        sec -= 22
    elif x < dt.datetime(year=1988, month=1, day=1):
        sec -= 23
    elif x < dt.datetime(year=1990, month=1, day=1):
        sec -= 24
    elif x < dt.datetime(year=1991, month=1, day=1):
        sec -= 25
    elif x < dt.datetime(year=1992, month=7, day=1):
        sec -= 26
    elif x < dt.datetime(year=1993, month=7, day=1):
        sec -= 27
    elif x < dt.datetime(year=1994, month=7, day=1):
        sec -= 28
    elif x < dt.datetime(year=1996, month=1, day=1):
        sec -= 29
    elif x < dt.datetime(year=1997, month=7, day=1):
        sec -= 30
    elif x < dt.datetime(year=1999, month=1, day=1):
        sec -= 31
    elif x < dt.datetime(year=2006, month=1, day=1):
        sec -= 32
    elif x < dt.datetime(year=2009, month=1, day=1):
        sec -= 33
    elif x < dt.datetime(year=2012, month=7, day=1):
        sec -= 34
    elif x < dt.datetime(year=2015, month=7, day=1):
        sec -= 35
    elif x < dt.datetime(year=2017, month=1, day=1):
        sec -= 36
    else:
        sec -= 37

    return x + dt.timedelta(seconds=sec)


# KISS basic info: https://www.ax25.net/kiss.aspx
# The basic implementation is taken from the kiss module from gr-satellites
KISS_FEND = b'\xc0'
KISS_FESC = b'\xdb'
KISS_TFEND = b'\xdc'
KISS_TFESC = b'\xdd'
KISS_CMD_DATA = 0, 16
KISS_CMD_TS = 9

kiss_epoch = dt.datetime(1970, 1, 1)


def kiss_unescape(frame):
    frame = frame.replace(KISS_FESC + KISS_TFEND, KISS_FEND)
    frame = frame.replace(KISS_FESC + KISS_TFESC, KISS_FESC)
    return frame


def kiss_read(fp):
    with fp.open('rb') as kf:
        frames = kf.read().split(KISS_FEND)
        if frames[0]:
            raise ValueError('no frame start: %s' % frames[0])

        t = None
        for fr in frames[1:]:
            if not fr:
                continue
            if fr[0] == KISS_CMD_TS:
                # timestamp
                ts, = struct.unpack('>Q', kiss_unescape(fr[1:]))
                t = kiss_epoch + dt.timedelta(seconds=ts / 1000)
            elif fr[0] in KISS_CMD_DATA:
                # data frame
                yield kiss_unescape(fr[1:]), t
            else:
                # TODO: unknown, what to do?
                pass


def kiss_read_stream(conn):
    # await beginning
    while 1:
        c = recvall(conn, 1)
        if not c:
            return
        if c == KISS_FEND:
            break

    # read control byte
    c = recvall(conn, 1)
    if c == KISS_FEND:
        c = recvall(conn, 1)
    if not c:
        return
    c = ord(c)

    if c == KISS_CMD_TS:
        ts, = struct.unpack('>Q', kiss_unescape(recvall(conn, 8)))
        t = kiss_epoch + dt.timedelta(seconds=ts / 1000)
        recvall(conn, 1)
        return t

    elif c in KISS_CMD_DATA:
        buf = bytearray()
        while 1:
            c = recvall(conn, 1)
            if not c:
                return
            if c == KISS_FEND:
                break
            buf.extend(c)
        return kiss_unescape(bytes(buf))


def _json_get_t(v):
    x = v.get('unixtime')
    if x:
        return dt.datetime.fromtimestamp(int(x), dt.timezone.utc)

    x = v.get('unixtimemill')
    if x:
        return dt.datetime.fromtimestamp(int(x) // 1000, dt.timezone.utc)

    x = v.get('datetime')
    if x:
        return dt.datetime.fromisoformat(x).astimezone(dt.timezone.utc)


def json_read(fp):
    for i, v in json.load(fp.open('rb')).items():
        yield bytes.fromhex(v.get('raw') or v.get('data')), _json_get_t(v)


seqs_map = {
    '\x72\x73\x32\x30\x73': 'aHR0cHM6Ly91cGxvYWQud2lraW1lZGlhLm9yZy93aWtpcGVkaWEvY29tbW9u'
                            'cy90aHVtYi80LzRhL0N1YmVTYXRfR2Vvc2Nhbi1FZGVsdmVpc19lbWJsZW0u'
                            'anBnLyVzcHgtQ3ViZVNhdF9HZW9zY2FuLUVkZWx2ZWlzX2VtYmxlbS5qcGc=',
    '\x72\x73\x31\x35\x73': 'aHR0cHM6Ly9zcHV0bml4LnJ1L3RwbC9pbWcvbG9nby16b3JraXkuanBnPyVz',
    '\x72\x73\x34\x30\x73': 'aHR0cHM6Ly9zcGFjZXBpLnNwYWNlL3VwbG9hZHMvRW1ibGVtYV9rdWJzYXRh'
                            'X1VtX0tBX2NmNzhiMDE0YTguanBnPyVz',
}

TCP_HDR_FMT = struct.Struct('!qI')
AGWPE_CON = b'\x00\x00\x00\x00k\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
AGWPE_HDR_FMT = struct.Struct('BxxxBxBx10s10sIxxxx')
SELF_SIGN = '### SatsDecoder ###'


def fits_hdr_read(f):
    f.seek(0)
    hdr = {}

    while 1:
        line = f.read(80)
        if not line:
            raise OSError('Truncated FITS file')
        kw = line[:8].strip()
        if kw == b'END':
            break
        val = line[8:].strip()
        if val.startswith(b'='):
            val = val[1:].strip()
        # if not hdr and (not _accept(kw) or val != b"T"):
        # if not hdr and val != b'T':
        #     raise SyntaxError('Not a FITS file')
        hdr[kw.decode('ascii')] = val.decode('ascii')

    return hdr


_bpp8 = {
    'L',
    'P',
    'RGB',
    'RGBA',
    'CMYK',
    'YCbCr',
    'LAB',
    'HSV',
}
def img_to_8bit(im):
    if im.mode in _bpp8:
        return im

    x = np.asarray(im)
    cmax = 2 ** (x.dtype.itemsize * 8)
    x = x.astype(np.float64)
    x = 255 * (x / cmax)

    return PIL.Image.fromarray(x.astype(np.uint8))


_fits_fmt = {
    '8': np.uint8,
    '16': np.int16,
    '32': np.int32,
    '-32': np.float32,
    '-64': np.float64,
}
def fits_fix(f):
    hdrs = fits_hdr_read(f)
    fmt = _fits_fmt[hdrs['BITPIX']]

    img = PIL.Image.open(f)
    data = np.asarray(img, fmt)
    data = data.view(data.dtype.newbyteorder('>')).astype(np.float64) + float(hdrs['BZERO'])

    if fmt == np.int16:
        fmt = np.uint16
    elif fmt == np.int32:
        fmt = np.uint32

    return PIL.Image.fromarray(data.astype(fmt))
