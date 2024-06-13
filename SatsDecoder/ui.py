#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import base64
import datetime as dt
import errno
import io
import json
import pathlib
import re
import select
import shutil
import socket as sk
import struct
import sys
import threading
import tkinter as tk
import urllib
import urllib.error
import urllib.request
import queue
import webbrowser

from tkinter import ttk, filedialog, messagebox, scrolledtext

import construct
import numpy as np
import PIL
import PIL.Image
import PIL.ImageFile
import PIL.ImageTk

from SatsDecoder import HOMEDIR, RES, systems, utils
from SatsDecoder.version import __version__


PIL.ImageFile.LOAD_TRUNCATED_IMAGES = 1


class NewTabDialog(tk.Toplevel):
    default_config = {
        'ip': '127.0.0.1',
        'port': 8000,
        'connmode': 0,
        'merge mode': 0,
    }

    def __init__(self, master, existing_names):
        super().__init__(master)
        self.transient(master)
        self.focus_set()
        self.wait_visibility()
        self.grab_set()
        self.resizable(width=False, height=False)
        self.title('Select New Decoder')

        self.cfg = self.default_config.copy()
        self.existing_names = existing_names

        self.opt_frame = ttk.Frame(self, padding=(3, 3, 3, 3))
        self.opt_frame.grid(column=0, row=0, sticky=tk.NSEW, padx=2, pady=2)

        ttk.Label(self.opt_frame, text='Protocol:').grid(column=0, row=0, sticky=tk.E, pady=3)
        self.proto = ttk.Combobox(self.opt_frame, state='readonly', values=tuple(systems.PROTOCOLS.keys()))
        self.proto.current(0)
        self.proto.grid(column=1, row=0, sticky=tk.EW, pady=3)

        ttk.Label(self.opt_frame, text='Name:').grid(column=0, row=1, sticky=tk.E, pady=3)
        self.name_v = tk.StringVar(self.opt_frame)
        self.name = ttk.Entry(self.opt_frame, textvariable=self.name_v)
        self.name.grid(column=1, row=1, sticky=tk.EW, pady=3)

        self.update()

        self.btns_frame = ttk.Frame(self.opt_frame)
        self.btns_frame.grid(column=0, row=2, columnspan=2, sticky=tk.EW)
        self.btns_frame.columnconfigure((0, 1), weight=1)

        self.ok_btn = ttk.Button(self.btns_frame, text='Ok', command=self.ok)
        self.ok_btn.grid(column=0, row=0, pady=3)

        self.cancel_btn = ttk.Button(self.btns_frame, text='Cancel', command=self.exit)
        self.cancel_btn.grid(column=1, row=0, pady=3)

        self.update()

    def get_name(self):
        return self.name_v.get()

    def ok(self):
        name = self.get_name()
        if not name:
            messagebox.showerror(message='The "Name" field cannot be empty')
            return
        if name in self.existing_names:
            messagebox.showerror(message='This Name already exists')
            return
        if name in ('+',):  # invalid names
            messagebox.showerror(message='Invalid name')
            return

        self.cfg['proto'] = self.proto.get()
        self.cfg['outdir'] = str(HOMEDIR / name)
        self.exit(1)

    def exit(self, ok=0):
        self.grab_release()
        self.destroy()
        if not ok:
            self.cfg = {}


class HistoryFrame(ttk.LabelFrame):
    EVT_SEL = '<<hist.select>>'
    FILTERS = 'tlm', 'img', 'raw', 'frame'

    def __init__(self, master, config):
        super().__init__(master, text='History', padding=(3, 3, 3, 3))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.ctrl_frame = ttk.Frame(self)
        self.ctrl_frame.columnconfigure(0, weight=1)
        self.ctrl_frame.columnconfigure(1, weight=1)
        self.ctrl_frame.grid(sticky=tk.NSEW)

        self.clear_btn = ttk.Button(self.ctrl_frame, text='clear', command=self.clear)
        self.clear_btn.grid(sticky=tk.W, column=0, row=0)

        self.filter_btn = ttk.Menubutton(self.ctrl_frame, text='Filter')
        self.filter_menu = tk.Menu(self.filter_btn, tearoff=0)
        self.filter_btn.configure(menu=self.filter_menu)
        self.filter_btn.grid(sticky=tk.E, column=1, row=0)
        self.filters = {}
        filters = config.get('filter', ';'.join(self.FILTERS)).split(';')
        for filt in self.FILTERS:
            self.filters[filt] = tk.IntVar(self, value=(filt in filters))
            self.filter_menu.add_checkbutton(label=filt, variable=self.filters[filt],
                                             onvalue=1, offvalue=0, command=self.apply_filter)

        self.order = {}
        self.vals = {}
        self.detached_vals = set()
        self.table = ttk.Treeview(self, columns='date type ' + ' '.join(master.decoder.columns),
                                  selectmode='browse', show='tree headings')
        f = utils.tk_nametofont('TkDefaultFont', self.table)
        # self.table.column('#0', anchor='e')
        self.table.column('#0', width=110, stretch=tk.NO)
        self.table.heading('date', text='Date')
        self.table.column('date', stretch=tk.NO, width=f.measure('8888-88-88 88:88:88.888'))
        self.table.heading('type', text='Type')
        self.table.column('type', stretch=tk.NO, width=f.measure('WWW'))

        for c, w in zip(master.decoder.columns, master.decoder.c_width):
            self.table.heading(c, text=c.capitalize())
            # self.table.column(c, width=f.measure(c), stretch=tk.NO)
            self.table.column(c, width=w, stretch=tk.NO)
        self.table.column(self.table['columns'][-1], stretch=tk.YES)

        self.table.bind('<<TreeviewSelect>>', self.item_select)

        # for i in range(3):
        #     self.put('raw', f'rs200s-{i}', '0x%04X' % 0x01ac, b'raw string \0\1\2\3\4')
        # self.put('raw', f'rs200s-{i}', '0x%04X' % 0xfff1, b'hello world\n\rnew line\nand\ttab')

        self.table.grid(sticky=tk.NSEW, pady=3)

        self.vsb = utils.AutoScrollbar(self, orient='vertical', command=self.table.yview)
        self.vsb.grid(sticky=tk.NSEW, pady=3, column=1, row=1)

        self.table.configure(yscrollcommand=self.vsb.set)

    def clear(self):
        self.table.delete(*self.table.get_children())
        self.order.clear()
        self.vals.clear()
        self.detached_vals.clear()
        if self.master.decoder.ir:
            self.master.decoder.ir.clear()
        self.master.event_generate(self.EVT_SEL, when='tail')

    def apply_filter(self):
        to_move = set()
        for i, parent, tag in self.detached_vals.copy():
            if self.filters[tag].get():
                self.detached_vals.discard(i)
                to_move.add(i)

        for parent in self.table.get_children():
            for i in self.table.get_children(parent):
                tag = self.table.item(i)['values'][1]
                if not self.filters[tag].get():
                    self.detached_vals.add((i, parent, tag))
                    self.table.detach(i)

        for parent, order in self.order.items():
            for idx, i in enumerate(order):
                if i in to_move:
                    self.table.move(i, parent, idx)

    def item_select(self, evt=None):
        self.master.event_generate(self.EVT_SEL, when='tail', x=evt.x, y=evt.y)

    def get_selected(self):
        r = self.table.selection()
        if r:
            i = utils.Dict(self.table.item(r[0]))
            if i:
                i['iid'] = r[0]
            return i

    def put(self, tag, name, *args, date=None):
        ins = 1
        vals = args[:len(self.master.decoder.columns)]
        if tag == 'img':
            *_, img = args
            if not date:
                date = img.date
            if img.renamed:
                self.vals.pop(img.renamed, 0)
                img.rename_done()
                iid = self.vals.pop(date, None)
                if iid is not None:
                    self.vals.pop(iid, None)
                    self.table.detach(iid)
                    self.table.selection_set(iid)
                    self.table.see(iid)
            if img.fn in self.vals:
                return
            self.vals[img.fn] = 1

        # elif tag == 'tlm' and date and date in self.vals:
        #     ins = 0
        #     iid = self.vals[date]

        if not date:
            date = dt.datetime.utcnow()

        if ins:
            try:
                parent_iid = self.table.item(name) and name
            except tk.TclError:
                parent_iid = self.table.insert('', 'end', name, text=name)

            iid = self.table.insert(parent_iid, 'end', tags=(tag,),
                                    values=[date, tag, *vals])
            self.vals[date] = iid
            self.order.setdefault(parent_iid, []).append(iid)

        self.vals[iid] = args[len(self.master.decoder.columns):]
        if self.filters[tag].get():
            self.table.selection_set(iid)
            self.table.see(iid)
        else:
            self.detached_vals.add((iid, parent_iid, tag))
            self.table.detach(iid)
            self.table.update()


class CanvasFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.active_img = self.active_pil_img = self.active_pil_img_modified = None
        self.cnv_img_id = tk.ALL
        self._imgtk = 0

        self.info_frame = ttk.Frame(self)
        self.info_frame.grid(row=0, sticky=tk.NSEW, pady=3)

        self.image_starter = ttk.Label(self.info_frame, text='STARTER', foreground='red')
        self.image_starter.grid(column=0, row=0, sticky=tk.E, padx=1.5)

        self.image_soi = ttk.Label(self.info_frame, text='SOI', foreground='red')
        self.image_soi.grid(column=1, row=0, sticky=tk.E, padx=1.5)

        ttk.Separator(self.info_frame, orient='vertical').grid(column=2, row=0, sticky=tk.NS, padx=3)

        self.image_offset_l = ttk.Label(self.info_frame, text='Base offset:')
        self.image_offset_l.grid(column=3, row=0, sticky=tk.E, padx=0)

        self.image_offset_v = tk.IntVar(self.info_frame, 0)
        self.image_offset = ttk.Entry(self.info_frame, textvariable=self.image_offset_v, width=7,
                                      validate='all', validatecommand=lambda: False)
        self.image_offset.grid(column=4, row=0, sticky=tk.W, padx=0)

        ttk.Separator(self.info_frame, orient='vertical').grid(column=5, row=0, sticky=tk.NS, padx=3)

        self.first_data_off_l = tk.Label(self.info_frame, text='First data offset:')
        self.first_data_off_l.grid(column=6, row=0, sticky=tk.E, padx=0)

        self.first_data_off_v = tk.IntVar(self.info_frame, 0)
        self.first_data_off = ttk.Entry(self.info_frame, textvariable=self.first_data_off_v, width=7,
                                        validate='all', validatecommand=lambda: False)
        self.first_data_off.grid(column=7, row=0, sticky=tk.W, padx=0)

        self.strip_btn = ttk.Button(self.info_frame, text='Strip', command=self.strip_file, state=tk.DISABLED)
        self.strip_btn.grid(column=8, row=0, sticky=tk.W, padx=3)

        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.grid(column=0, row=1, sticky=tk.NSEW, pady=3)
        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)

        self.canvas_sz = 0, 0
        self.canvas = tk.Canvas(self.canvas_frame)
        self.canvas.grid(column=0, row=0, sticky=tk.NSEW)

        self.vsb = utils.AutoScrollbar(self.canvas_frame, orient='vertical', command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky=tk.NS)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.hsb = utils.AutoScrollbar(self.canvas_frame, orient='horizontal', command=self.canvas.xview)
        self.hsb.grid(row=1, column=0, sticky=tk.EW)
        self.canvas.configure(xscrollcommand=self.hsb.set)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        self.tail_frame = ttk.Frame(self)
        self.tail_frame.grid(row=2, sticky=tk.NSEW, pady=3)
        self.tail_frame.columnconfigure(3, weight=1)

        self.demosaic_btn = ttk.Button(self.tail_frame, text='Demosaicing', command=self.demosaicing, state=tk.DISABLED)
        self.demosaic_btn.grid(sticky=tk.SW, row=0, column=0, padx=1.5)

        self.save_btn = ttk.Button(self.tail_frame, text='Save as', command=self.save_as)
        self.save_btn.grid(sticky=tk.SW, row=0, column=1, padx=1.5)

        ttk.Separator(self.tail_frame, orient='vertical').grid(sticky=tk.NS, row=0, column=2, padx=3)

        self.image_name_l = ttk.Label(self.tail_frame)
        self.image_name_l.grid(sticky=tk.SW, row=0, column=3)

    def fill_canvas(self, img, force=0):
        if not (force or (self.active_img and self.active_img.fn == img.fn)):
            return 1

        self.active_img = img
        self.image_name_l.config(text=img.fn.name)
        self.image_starter.config(foreground=img.has_starter and 'green' or 'red')
        self.image_soi.config(foreground=img.has_soi and 'green' or 'red')
        self.image_offset_v.set(img.base_offset)
        self.first_data_off_v.set(img.first_data_offset)
        self.strip_btn.config(state=img.first_data_offset and tk.NORMAL or tk.DISABLED)
        self.demosaic_btn.config(state=img.mosaic and tk.NORMAL or tk.DISABLED)
        self.active_pil_img_modified = 0

        try:
            with img.lock:
                f = img.open()
                if img.mode == 'file':
                    i = PIL.Image.open(f)
                elif img.mode == 'bytes':
                    kw = img.mode_kw
                    f.seek(0, 0)
                    i = PIL.Image.frombytes(
                        kw['mode'],
                        kw['size'],
                        f.read(),
                        kw['decoder_name'],
                        *kw['args'],
                    )
            self.draw_image(i)

        except PIL.UnidentifiedImageError:
            self.canvas.delete(tk.ALL)
        except:
            pass

    def strip_file(self):
        if self.active_img:
            # TODO
            self.active_img.rebase_offset()

            self.fill_canvas(self.active_img, 1)

    def demosaicing(self):
        if not self.active_pil_img:
            return

        method, mode = self.active_img.mosaic.split(';')
        if method == 'bayer':
            data = np.array(self.active_pil_img.getdata(), np.uint8)
            self.draw_image(PIL.Image.fromarray(utils.bayer2rgb(data, mode, *self.active_pil_img.size), 'RGB'))

        self.demosaic_btn.config(state=tk.DISABLED)
        self.active_pil_img_modified = 1

    def save_as(self):
        fn = pathlib.Path(self.active_img.fn)
        ofn = filedialog.asksaveasfilename(
            defaultextension=fn.suffix, confirmoverwrite=True,
            filetypes=[('Auto', [f'*{fn.suffix}']), ('Images', ['*.png', '*.jpg']), ('All files', '*.*')],
            initialdir=fn.parent, initialfile=fn.name)
        if ofn:
            if self.active_pil_img_modified or fn.suffix != pathlib.Path(ofn).suffix:
                self.active_pil_img.save(ofn)
            else:
                shutil.copyfile(fn, ofn)

    def draw_image(self, i):
        del self._imgtk
        _imgtk = PIL.ImageTk.PhotoImage(i)
        to_del, self.cnv_img_id = self.cnv_img_id, self.canvas.create_image(0, 0, anchor=tk.NW, image=_imgtk)
        self.canvas.delete(to_del)
        self._imgtk = _imgtk

        if i.size != self.canvas_sz:
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        if self.active_pil_img:
            self.active_pil_img.close()
        self.active_pil_img = i


class DataViewFrame(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text='Data View', padding=(3, 3, 3, 3))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.viewers = []

        self.control_text_frame = ttk.Frame(self)
        self.control_text_frame.rowconfigure(0, weight=1)
        self.viewers.append(self.control_text_frame)
        self.view_select_v = tk.StringVar(self.control_text_frame, 'RAW')
        self.view_select_raw = ttk.Radiobutton(self.control_text_frame, value='RAW', text='RAW',
                                               variable=self.view_select_v, command=self.change_text_mode)
        self.view_select_raw.grid(row=0, column=0)
        self.view_select_ascii = ttk.Radiobutton(self.control_text_frame, value='ASCII', text='ASCII',
                                                 variable=self.view_select_v, command=self.change_text_mode)
        self.view_select_ascii.grid(row=0, column=1)
        self.copy_btn = ttk.Button(self.control_text_frame, text='Copy', command=self.do_copy)
        self.copy_btn.grid(row=0, column=2)

        self.text_raw = b''
        self.text = scrolledtext.ScrolledText(self, state='disabled')
        self.viewers.append(self.text)

        self.tlm = utils.TlmCommonFrame(self, master.decoder.tlm_table)
        self.viewers.append(self.tlm)

        self.cnv = CanvasFrame(self)
        self.viewers.append(self.cnv)

    def clear(self, skip_iai=0):
        for i in self.viewers:
            i.grid_forget()
        if not skip_iai:
            self.cnv.active_img = None

    def change_text_mode(self):
        self.set_raw(self.text_raw)

    def do_copy(self):
        mode = self.view_select_v.get()
        data = self.text_raw

        if isinstance(data, bytes):
            if mode == 'RAW':
                data = utils.bytes2hex(data)
            else:   # ASCII
                data = data.decode('ascii', 'replace')

        self.clipboard_clear()
        self.clipboard_append(data)

    def set_raw(self, data, tag='raw'):
        self.text_raw = data
        mode = self.view_select_v.get()

        if isinstance(data, bytes):
            if mode == 'RAW':
                data = utils.bytes2hex(data)
            else:   # ASCII
                data = data.decode('ascii', 'replace').replace('\0', '\u25A1')

        self.clear()

        self.text['state'] = 'normal'
        self.text.delete('1.0', 'end')
        self.text.insert('end', data)
        self.text['state'] = 'disabled'

        self.text.grid(column=0, row=0, sticky=tk.NSEW)
        self.control_text_frame.grid(column=0, row=1, sticky=tk.E)
        st = (tag == 'raw') and tk.NORMAL or tk.DISABLED
        self.view_select_raw.configure(state=st)
        self.view_select_ascii.configure(state=st)

    def set_tlm(self, tlm, fname):
        self.clear()

        self.tlm.fill(tlm, fname)
        self.tlm.grid(column=0, row=0, sticky=tk.NSEW)

    def set_img(self, img, select=0):
        if not self.cnv.fill_canvas(img, select):
            self.clear(1)
            self.cnv.grid(column=0, row=0, sticky=tk.NSEW)


class DecoderFrame(ttk.Frame):
    STOP_EVT = '<<STOP>>'

    def __init__(self, master, config, name):
        super().__init__(master)

        x = NewTabDialog.default_config.copy()
        x.update(config)

        self.config = config = x
        self.proto = config.get('proto', name)
        self.name = name
        self.sk = self.thr = self.frame_off = 0
        self.decoder = systems.PROTOCOLS[self.proto](config.get('outdir'))

        self.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(1, weight=1)
        # self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ctrl frame
        self.ctrl_frame = ttk.LabelFrame(self, text='%s' % self.proto.upper(), padding=(3, 3, 3, 3))
        self.ctrl_frame.grid(column=0, row=0, sticky=tk.NSEW, padx=2, pady=2)
        self.ctrl_frame.columnconfigure(1, weight=1)
        self.ctrl_frame.columnconfigure(4, weight=1)

        self.out_dir_v = tk.StringVar(self.ctrl_frame, config.get('outdir'))
        self.out_dir_e = ttk.Entry(self.ctrl_frame, textvariable=self.out_dir_v, state=tk.NORMAL)
        self.out_dir_e.grid(column=0, columnspan=4, row=0, sticky=tk.EW, pady=3)

        self.out_dir_btn = ttk.Button(self.ctrl_frame, text='Out Dir', command=self.choose_out_dir)
        self.out_dir_btn.grid(column=4, row=0, sticky=tk.EW, pady=3, padx=3)

        self.server_v = tk.StringVar(self.ctrl_frame, config.get('ip'))
        self.port_v = tk.StringVar(self.ctrl_frame, config.get('port'))

        ttk.Label(self.ctrl_frame, text='Address:').grid(column=0, row=1, sticky=tk.E, pady=3)
        self.server_e = ttk.Entry(self.ctrl_frame, textvariable=self.server_v)
        self.server_e.grid(column=1, row=1, sticky=tk.EW, pady=3)

        ttk.Label(self.ctrl_frame, text='Port:').grid(column=2, row=1, sticky=tk.E, pady=3)
        self.port_e = ttk.Entry(self.ctrl_frame, textvariable=self.port_v, width=7)
        self.port_e.grid(column=3, row=1, sticky=tk.EW, pady=3)

        self.con_btn = ttk.Button(self.ctrl_frame, text='Connect', command=self.con)
        self.con_btn.grid(column=4, row=1, sticky=tk.EW, pady=3, padx=3)

        ttk.Label(self.ctrl_frame, text='Conn:').grid(column=0, row=2, sticky=tk.E, pady=3)
        self.conn_mode = ttk.Combobox(self.ctrl_frame, values=tuple(utils.con_mode_names.values()), state='readonly')
        self.conn_mode.bind('<<ComboboxSelected>>', self.named_conn_btn)
        try:
            self.conn_mode.current(int(config.get('connmode')))
        except tk.TclError:
            self.conn_mode.current(0)
        self.named_conn_btn()
        self.conn_mode.grid(column=1, row=2, sticky=tk.EW, pady=3)

        self.merge_mode_v = tk.IntVar(self.ctrl_frame, int(config.get('merge mode')))
        self.merge_mode_ckb = ttk.Checkbutton(self.ctrl_frame, text='Merge mode',
                                              variable=self.merge_mode_v, command=self.set_merge_mode)
        self.merge_mode_ckb.grid(column=2, columnspan=2, row=2, sticky=tk.EW, pady=3)

        self.new_btn = ttk.Button(self.ctrl_frame, text='New image', command=self.new_img)
        self.new_btn.grid(column=4, row=2, sticky=tk.EW, pady=3, padx=3)

        # history frame
        self.history_frame = HistoryFrame(self, config)
        self.history_frame.grid(column=0, row=1, sticky=tk.NSEW, padx=2, pady=2)
        self.bind(self.history_frame.EVT_SEL, self.fill_data)
        self.bind(self.STOP_EVT, self.stop)

        # data view frame
        self.dv_frame = DataViewFrame(self)
        self.dv_frame.grid(column=1, row=0, rowspan=2, sticky=tk.NSEW, padx=2, pady=2)

    def openfiles(self):
        path = HOMEDIR
        files = filedialog.askopenfilenames(title='Choose packets', initialdir=path, filetypes=(("TLM file", "*.txt"), ("All files", "*.*")))
        for f in files:
            file = open(f, 'r')
            line = file.readline().strip()
            x = bytes.fromhex(line)
            self.feed(x)
            file.close()

    def named_conn_btn(self, _=None, **kw):
        m = utils.ConnMode(self.conn_mode.current())
        d = {
            utils.ConnMode.AGWPE_CLI: ('Connect', 'Disconnect'),
            utils.ConnMode.TCP_CLI: ('Connect', 'Disconnect'),
            utils.ConnMode.TCP_SRV: ('Start', 'Stop'),
            utils.ConnMode.HEX: ('Run', 'Stop'),
            utils.ConnMode.HEX_TXT: ('Load packets', 'Stop'),
        }
        self.con_btn.config(text=d[m]['d' in kw])

    def fill_data(self, evt=None):
        x = self.history_frame.get_selected()
        if not (x and x.tags):
            self.dv_frame.clear()
            return

        tag = x.tags[0]
        vals = self.history_frame.vals[x.iid]

        if tag == 'tlm':
            self.dv_frame.set_tlm(vals[-2], vals[-1])
        elif tag == 'img':
            self.dv_frame.set_img(vals[-1], 1)
        else:   # raw, etc
            self.dv_frame.set_raw(vals[-1], tag)

    def choose_out_dir(self):
        d = filedialog.askdirectory()
        if d:
            self.out_dir_v.set(d)
            self.set_out_dir(d)

    def con(self):
        self.set_merge_mode()
        self.set_out_dir()

        m = utils.ConnMode(self.conn_mode.current())
        if m == utils.ConnMode.HEX:
            self._hex_values()
        elif m == utils.ConnMode.HEX_TXT:
            self.openfiles()
        else:
            self.stop() if self.sk else self._start()


    def set_merge_mode(self):
        if self.decoder.ir:
            self.decoder.ir.set_merge_mode(self.merge_mode_v.get())

    def set_out_dir(self, d=None):
        if self.decoder.ir:
            self.decoder.ir.set_outdir(d or self.out_dir_v.get())

    def new_img(self):
        if self.decoder.ir:
            *_, img = args = self.decoder.create_new_image()
            self.dv_frame.set_img(img, 1)
            self.history_frame.put('img', self.proto, *args)

    def stop(self, _=None):
        if self.sk:
            s = self.sk
            self.sk = 0
            s.close()

        if self.thr and self.thr.is_alive():
            self.thr.join(0)
            self.thr = 0
        self.named_conn_btn()
        self.server_e.config(state=tk.NORMAL)
        self.port_e.config(state=tk.NORMAL)
        self.out_dir_e.config(state=tk.NORMAL)
        self.out_dir_btn.config(state=tk.NORMAL)
        self.conn_mode.config(state='readonly')

    def _hex_values(self):
        ask_hex = tk.Toplevel(self)
        ask_hex.transient(self)
        ask_hex.focus_set()
        ask_hex.wait_visibility()
        ask_hex.grab_set()
        ask_hex.title('HEX')

        def _finish(ok=0):
            if ok:
                for line in text_e.get(1.0, 'end').splitlines():
                    try:
                        x = bytes.fromhex(line)
                    except ValueError:
                        continue
                    if x and self.feed(x):
                        break

            ask_hex.grab_release()
            ask_hex.destroy()

        frame = ttk.Frame(ask_hex)
        frame.grid(column=0, row=0, sticky=tk.NSEW)

        text_e = tk.Text(frame)
        text_e.grid(column=0, row=0, sticky=tk.NSEW)

        btns_frame = ttk.Frame(frame, padding=(3, 3, 3, 3))
        btns_frame.grid(columnspan=2, sticky=tk.EW)
        btns_frame.columnconfigure((0, 1), weight=1)

        ok_btn = ttk.Button(btns_frame, text='Ok', command=lambda: _finish(1))
        ok_btn.grid(column=0, row=0)

        cancel_btn = ttk.Button(btns_frame, text='Cancel', command=_finish)
        cancel_btn.grid(column=1, row=0)

        ask_hex.update()

    def _start(self):
        curr_mode = utils.ConnMode(self.conn_mode.current())
        self.is_server = curr_mode == utils.ConnMode.TCP_SRV
        self.is_agwpe_cli = curr_mode == utils.ConnMode.AGWPE_CLI
        try:
            self.frame_off = 0
            s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
            if self.is_server:
                s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
                s.bind((self.server_v.get(), int(self.port_v.get())))
                s.listen()

            else:
                s.connect((self.server_v.get(), int(self.port_v.get())))
                if self.is_agwpe_cli:
                    self.frame_off = 1
                    s.send(utils.AGWPE_CON)

            s.setblocking(0)
            self.sk = s

        except (ConnectionError, OSError) as e:
            messagebox.showerror(message='%s: %s' % (self.name, e.strerror))

        except Exception as e:
            messagebox.showerror(message='%s: %s' % (self.name, e.args))

        else:
            self.named_conn_btn(d=1)
            self.server_e.config(state=tk.DISABLED)
            self.port_e.config(state=tk.DISABLED)
            self.out_dir_e.config(state=tk.DISABLED)
            self.out_dir_btn.config(state=tk.DISABLED)
            self.conn_mode.config(state=tk.DISABLED)

            self.thr = threading.Thread(target=self.is_server and self._server or self._client, daemon=1)
            self.thr.start()

    def _server(self):
        srv_fd = self.sk.fileno()
        r = {srv_fd: self.sk}

        while self.sk:
            ss = set(select.select(r, [], [], 0.1)[0])
            if srv_fd in ss:
                ss.discard(srv_fd)
                try:
                    conn, addr = self.sk.accept()
                    conn.setblocking(0)
                    r[conn.fileno()] = conn
                except AttributeError:
                    break

            for s in ss:
                if self._receive(r[s]):
                    r.pop(s).close()

        r.pop(srv_fd, 0)
        for conn in r.values():
            conn.close()

        if self.sk:
            self.event_generate(self.STOP_EVT, when='tail')

    def _client(self):
        r = {self.sk}

        while self.sk:
            if select.select(r, [], [], 0.1)[0] and self._receive(self.sk):
                break

        if self.sk:
            self.event_generate(self.STOP_EVT, when='tail')

    @staticmethod
    def _recvall(conn, n):
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

    def _receive(self, conn):
        try:
            if self.is_agwpe_cli:
                frame = conn.recv(utils.AGWPE_HDR_FMT.size)
                if len(frame) != utils.AGWPE_HDR_FMT.size:
                    frame = 0
                else:
                    port, kind, pid, c_from, c_to, dlen = utils.AGWPE_HDR_FMT.unpack_from(frame)
                    frame = conn.recv(dlen)
            else:
                frame = self._recvall(conn, 4)
                if len(frame) != 4:
                    frame = 0
                else:
                    frame_sz, = struct.unpack('!I', frame)
                    frame = self._recvall(conn, frame_sz)
        except AttributeError:
            return 1
        except OSError as e:
            if e.errno in (errno.EAGAIN, errno.EWOULDBLOCK, sys.platform == 'win32' and errno.WSAEWOULDBLOCK):
                return
            if e.errno not in (errno.EBADF, sys.platform == 'win32' and errno.WSAEBADF) and conn.fileno() != -1:
                messagebox.showerror(message='%s: %s (%s)' % (self.name, e, conn))
            return 1

        if not frame:
            if not self.is_server:
                messagebox.showwarning(message='%s: Connection lost' % self.name)
            return 1

        return self.feed(frame)

    def feed(self, frame):
        try:
            data = frame[self.frame_off:]
            for i in self.decoder.recognize(data):
                args = i
                ty, name, *_, packet = i
                if '\0' in name:
                    # TODO: log it, '`null` in name not allowed'
                    continue
                date = 0

                if ty == 'img':
                    ir_ret, img = packet
                    self.dv_frame.set_img(img)
                    args = args[:-1] + (img,)
                    date = img.date

                elif ty == 'tlm':
                    packet, tlm = packet
                    date = getattr(tlm, 'Time', dt.datetime.utcnow())
                    name = ('%s_%s_%s_%s.txt' % (name, self.proto, tlm._name, date)).replace(
                        ' ', '_').replace(':', '-')
                    fp = pathlib.Path(self.out_dir_v.get()) / name
                    args = args[:-1] + (tlm, fp)

                    fp.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        with fp.open('w') as f:
                            f.write(utils.bytes2hex(data))
                            f.write('\n\n')
                            f.write(str(packet))
                    except ValueError:
                        # TODO: log it. invalid name
                        continue

                self.history_frame.put(*args, date=date)

        except construct.ConstructError:
            # TODO: log it
            pass

        except Exception as e:
            messagebox.showerror(message='feed %s: %s' % (self.name, e))
            return 1


class App(ttk.Frame):
    def __init__(self, config):
        super().__init__()
        self.ico = PIL.Image.open(RES / 'icon.png')
        self.master.iconphoto(False, PIL.ImageTk.PhotoImage(self.ico))

        self.config = config

        if config.has_option('main', 'pos'):
            self.master.geometry(config.get('main', 'pos'))

        self.master.protocol("WM_DELETE_WINDOW", self.exit)
        self.master.option_add('*tearOff', tk.FALSE)
        self.master.title(f'Satellites decoder v{__version__}')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.master.bind('<Control-Q>', self.exit)
        self.master.bind('<Control-q>', self.exit)
        self.master.bind('<F1>', self.about)

        self.check_update_v = tk.IntVar(self, int(config.get('main', 'check_update')))
        if self.check_update_v.get():
            threading.Thread(target=self.check_updates, args=(self, 0, 0)).start()

        # Notebook frame
        # self.notebook = ttk.Notebook(self)
        self.notebook = utils.DynamicNotebook(self, self.create_new_tab)
        self.notebook.grid(column=0, row=0, sticky=tk.NSEW)
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)

        self.tabs = {}

        x = dict(config.items())
        for s in config.default_section, 'main', 'info':
            x.pop(s)

        for name, cfg in x.items():
            try:
                f = DecoderFrame(self.notebook, cfg, name)
            except KeyError:
                # messagebox.showwarning(message='Unknown proto: `%s`. Skip and delete' % cfg.get('proto'))
                self.config.remove_section(name)
                continue

            self.notebook.add(f, text=name)
            self.tabs[f.name] = f

        self.notebook.select(0)
        self.notebook.bind('<<NotebookTabClosed>>', self.close_tab)

        #####
        self.update()
        self.master.minsize(600, 400)

    def close_tab(self, evt=None):
        tabs = {str(df): (n, df) for n, df in self.tabs.items()}
        dels = set(tabs) - set(self.notebook.tabs())
        for i in dels:
            n, df = tabs[i]
            self.close_df(n, df)
            self.tabs.pop(n, 0)
            self.config.remove_section(n)

    def create_new_tab(self):
        w = NewTabDialog(self, self.tabs)
        self.wait_window(w)

        if not w.cfg:
            return

        f = DecoderFrame(self.notebook, w.cfg, w.get_name())
        self.tabs[f.name] = f
        return f, f.name

    def exit(self, evt=None):
        for name, df in self.tabs.items():
            self.close_df(name, df)

        self.config.set('main', 'pos', self.master.winfo_geometry())
        self.config.set('main', 'check_update', str(self.check_update_v.get()))
        self.config.set('info', 'version', __version__)
        self.quit()

    def close_df(self, name, df):
        df.stop()
        if not self.config.has_section(name):
            self.config.add_section(name)

        self.config.set(name, 'proto', df.proto)
        self.config.set(name, 'ip', df.server_v.get())
        self.config.set(name, 'port', df.port_v.get())
        self.config.set(name, 'outdir', df.out_dir_v.get())
        self.config.set(name, 'merge mode', str(df.merge_mode_v.get()))
        self.config.set(name, 'connmode', str(df.conn_mode.current()))
        self.config.set(name, 'filter', str(';'.join(k for k, v in df.history_frame.filters.items() if v.get())))

    def about(self, evt=None):
        seq = queue.Queue(5)
        img = img_l = None

        def sequence_check(evt=None):
            nonlocal seq

            if not evt.char:
                return

            if seq.full():
                seq.get()
            seq.put(evt.char.lower())

            s = ''.join(seq.queue)
            if s in utils.seqs_map:
                def foo(ss):
                    nonlocal img, img_l

                    u = base64.b64decode(utils.seqs_map[ss]).decode()
                    w_width = pad_frame.winfo_width() - 2
                    raw_pic = urllib.request.urlopen(u % w_width).read()
                    img = PIL.Image.open(io.BytesIO(raw_pic))
                    if img.width > w_width:
                        mag = img.width / w_width
                        img = img.resize((w_width, int(img.height / mag)))
                    img = PIL.ImageTk.PhotoImage(img)

                    for i in pad_frame.winfo_children():
                        i.destroy()
                    ok_btn.config(text='73!')
                    if img_l:
                        img_l.destroy()
                    img_l = ttk.Label(pad_frame, image=img, justify='center')
                    img_l.grid()

                    about.update()

                threading.Thread(target=foo, args=(s,)).start()

        about = tk.Toplevel(self)
        about.transient(self)
        about.focus_set()
        about.wait_visibility()
        about.grab_set()
        about.resizable(width=False, height=False)
        about.title('About')
        about.bind('<KeyPress>', sequence_check)

        frame = ttk.Frame(about, padding=(10, 6, 10, 6))
        frame.grid(column=0, row=0, sticky=tk.NSEW)

        ttk.Label(frame, text=f'SatsDecoder v{__version__}').grid(columnspan=2)
        ttk.Label(frame, text='GPL-3.0, MIT licenses\nCopyright (c) 2024 Alexander Baskikh\n', justify='center').grid(columnspan=2, rowspan=3)

        links = (
            ('GitHub page:', 'https://github.com/baskiton/SatsDecoder'),
            ('Geoscan page:', 'https://geoscan.space/'),
            ('Sputnix page:', 'https://sputnix.ru/'),
            ('Amateurs chat:', 'https://t.me/amateursat'),
        )

        ttk.Label(frame, text=links[0][0]).grid(column=0, row=4, sticky=tk.E)
        x = ttk.Label(frame, text=links[0][1], foreground='blue', cursor='hand2')
        x.bind('<Button-1>', lambda e: webbrowser.open(links[0][1]))
        x.grid(column=1, row=4, sticky=tk.W)

        ttk.Label(frame, text=links[1][0]).grid(column=0, row=5, sticky=tk.E)
        x = ttk.Label(frame, text=links[1][1], foreground='blue', cursor='hand2')
        x.bind('<Button-1>', lambda e: webbrowser.open(links[1][1]))
        x.grid(column=1, row=5, sticky=tk.W)

        ttk.Label(frame, text=links[2][0]).grid(column=0, row=6, sticky=tk.E)
        x = ttk.Label(frame, text=links[2][1], foreground='blue', cursor='hand2')
        x.bind('<Button-1>', lambda e: webbrowser.open(links[2][1]))
        x.grid(column=1, row=6, sticky=tk.W)

        ttk.Label(frame, text=links[3][0]).grid(column=0, row=7, sticky=tk.E)
        x = ttk.Label(frame, text=links[3][1], foreground='blue', cursor='hand2')
        x.bind('<Button-1>', lambda e: webbrowser.open(links[3][1]))
        x.grid(column=1, row=7, sticky=tk.W)

        about.update()
        pad_frame = ttk.Frame(frame, height=x.winfo_height(), padding=(0, 6, 0, 6))
        pad_frame.grid(columnspan=2, sticky=tk.EW)

        btns_frame = ttk.Frame(frame)
        btns_frame.grid(columnspan=2, sticky=tk.EW)
        btns_frame.columnconfigure((0, 1), weight=1)

        upd_btn = ttk.Button(btns_frame, text='Check updates',
                             command=lambda: threading.Thread(target=self.check_updates, args=(about, btns_frame, 1)).start())
        upd_btn.grid(column=0, row=0)

        ok_btn = ttk.Button(btns_frame, text='Ok', command=lambda: (about.grab_release(), about.destroy()))
        ok_btn.grid(column=1, row=0)

        check_update_ckb = ttk.Checkbutton(frame, text='Check updates on startup', variable=self.check_update_v)
        check_update_ckb.grid(columnspan=2)

        about.update()

    @staticmethod
    def check_updates(parent, label_frame, showerror):
        m = re.match(r'([\d.]+).*', __version__)
        if m:
            v = tuple(map(int, m.group(1).split('.')))
        else:
            if showerror:
                messagebox.showerror(message=f'Invalid version, can\'t be compared: {__version__}')
            return

        try:
            with urllib.request.urlopen(urllib.request.Request(
                    'https://api.github.com/repos/baskiton/SatsDecoder/releases/latest',
                    headers={'accept': 'application/vnd.github+json'})) as r:
                resp = json.load(r)
        except urllib.error.URLError as e:
            if showerror:
                messagebox.showerror(message=str(e))
            return

        if v < tuple(map(int, resp['tag_name'].split('.'))):
            fg = 'green'
            msg = resp['tag_name']
            if not label_frame:
                if messagebox.askyesno(message=f'New version found: {msg}\nFollow to download link?', parent=parent):
                    webbrowser.open('https://github.com/baskiton/SatsDecoder/releases/latest')
                return
        else:
            fg = 'red'
            msg = 'not found'

        if label_frame:
            for i in label_frame.winfo_children():
                if isinstance(i, ttk.Label):
                    i.config(text=f'New version: {msg}', foreground=fg)
                    break
            else:
                ttk.Label(label_frame, text=f'New version: {msg}', foreground=fg, justify='center').grid(columnspan=2)
            parent.update()
