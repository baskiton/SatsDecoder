import base64
import datetime as dt
import io
import json
import pathlib
import re
import socket as sk
import threading
import tkinter as tk
import urllib
import urllib.error
import urllib.request
import queue
import webbrowser

from tkinter import ttk, filedialog, messagebox

import PIL
import PIL.Image
import PIL.ImageFile
import PIL.ImageTk

from SatsDecoder import AGWPE_CON, PROTOCOLS, RES, systems, utils
from SatsDecoder.version import __version__


PIL.ImageFile.LOAD_TRUNCATED_IMAGES = 1


class HistoryFrame(ttk.LabelFrame):
    EVT_SEL = '<<hist.select>>'

    def __init__(self, master):
        super().__init__(master, text='History', padding=(3, 3, 3, 3))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.clear_btn = ttk.Button(self, text='clear', command=self.clear)
        self.clear_btn.grid(sticky=tk.NW)

        self.vals = {}
        self.table = ttk.Treeview(self, columns='date type ' + ' '.join(master.decoder.columns),
                                  selectmode='browse', show='tree headings')
        # self.table.column('#0', anchor='e')
        self.table.column('#0', width=80, stretch=tk.NO)
        self.table.heading('date', text='Date')
        self.table.column('date', stretch=tk.NO)
        self.table.heading('type', text='Type')
        self.table.column('type', stretch=tk.NO, width=40)

        for c, w in zip(master.decoder.columns, master.decoder.c_width):
            self.table.heading(c, text=c.capitalize())
            self.table.column(c, width=w, stretch=tk.NO)
        self.table.column(self.table['columns'][-1], stretch=tk.YES)

        self.table.bind('<<TreeviewSelect>>', self.item_select)

        # for i in range(3):
        #     self.put('raw', f'rs200s-{i}', '0x%04X' % 0x01ac, b'raw string \0\1\2\3\4')
        # self.put('ascii', f'rs200s-{i}', '0x%04X' % 0xfff1, 'hello world')

        self.table.grid(sticky=tk.NSEW, pady=3)

        self.vsb = ttk.Scrollbar(self, orient='vertical', command=self.table.yview)
        self.vsb.grid(sticky=tk.NSEW, pady=3, column=1, row=1)

        self.table.configure(yscrollcommand=self.vsb.set)

    def clear(self):
        self.table.delete(*self.table.get_children())
        self.vals.clear()
        self.master.decoder.ir.clear(1)

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
        vals = args[:len(self.master.decoder.columns)]
        if tag == 'img':
            *_, ir, fname = args
            if fname in self.vals:
                return
            self.vals[fname] = args[len(self.master.decoder.columns):]

        iid = self.table.insert('', 'end', text=name, tags=(tag,),
                                values=[date or dt.datetime.utcnow(), tag, *vals])
        self.vals[iid] = args[len(self.master.decoder.columns):]
        self.table.selection_set(iid)


class CanvasFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.rowconfigure(1, weight=1)
        self.active_fname = None
        self.active_ir = None

        self.image_starter = ttk.Label(self, text='STARTER', foreground='red')
        self.image_starter.grid(column=0, row=0, sticky=tk.E, padx=0)

        self.image_soi = ttk.Label(self, text='SOI', foreground='red')
        self.image_soi.grid(column=1, row=0, sticky=tk.E, padx=0)

        self.image_offset_l = ttk.Label(self, text='Base offset:')
        self.image_offset_l.grid(column=2, row=0, sticky=tk.E, padx=0)

        self.image_offset_v = tk.IntVar(self, 0)
        self.image_offset = ttk.Entry(self, textvariable=self.image_offset_v, width=7,
                                      validate='all', validatecommand=lambda: False)
        self.image_offset.grid(column=3, row=0, sticky=tk.W, padx=0)

        self.sep = ttk.Separator(self, orient='vertical')
        self.sep.grid(column=4, row=0, sticky=tk.NS)

        self.first_data_off_l = tk.Label(self, text='First data offset:')
        self.first_data_off_l.grid(column=5, row=0, sticky=tk.E, padx=0)

        self.first_data_off_v = tk.IntVar(self, 0)
        self.first_data_off = ttk.Entry(self, textvariable=self.first_data_off_v, width=7,
                                        validate='all', validatecommand=lambda: False)
        self.first_data_off.grid(column=6, row=0, sticky=tk.W, padx=0)

        self.strip_btn = ttk.Button(self, text='Strip', command=self.strip_file, state=tk.DISABLED)
        self.strip_btn.grid(column=7, row=0, sticky=tk.W, padx=0)

        self.canvas_sz = 420, 420
        self.canvas = tk.Canvas(self, width=self.canvas_sz[0], height=self.canvas_sz[1])
        self.canvas.grid(columnspan=8, sticky=tk.NSEW, pady=3)

        self.image_name_l = ttk.Label(self)
        self.image_name_l.grid(columnspan=8, sticky=tk.SW, pady=3)

    def fill_canvas(self, ir, fname, force=0):
        if not force and self.active_fname != fname:
            return 1

        self.active_fname = fname
        self.active_ir = ir
        img = ir.cur_img

        self.image_name_l.config(text=fname.name)

        self.image_starter.config(foreground=img.has_starter and 'green' or 'red')
        self.image_soi.config(foreground=img.has_soi and 'green' or 'red')
        self.image_offset_v.set(img.base_offset)
        self.first_data_off_v.set(img.first_data_offset)
        self.strip_btn.config(state=img.first_data_offset and tk.NORMAL or tk.DISABLED)

        i = None
        try:
            i = PIL.Image.open(fname)
            if i.size != self.canvas_sz:
                self.canvas.config(width=i.width, height=i.height)
                self.canvas_sz = i.size
                self.canvas.update()
                # self.master.minsize(self.winfo_width(), self.winfo_height())
            self._imgtk = PIL.ImageTk.PhotoImage(i)
            self.canvas.delete(tk.ALL)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self._imgtk)

        except PIL.UnidentifiedImageError:
            self.canvas.delete(tk.ALL)
        except:
            pass

        if i:
            i.close()

    def strip_file(self):
        if self.active_ir and self.active_ir.cur_img:
            # TODO
            self.active_ir.cur_img.rebase_offset()

            self.fill_canvas(self.active_ir, self.active_fname, 1)


class DataViewFrame(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text='Data View', padding=(3, 3, 3, 3))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.viewers = []

        self.text = tk.Text(self, state='disabled')
        self.viewers.append(self.text)

        self.tlm = master.decoder.tlm_view(self)
        self.viewers.append(self.tlm)

        self.img = CanvasFrame(self)
        self.viewers.append(self.img)

    def clear(self, skip_ian=0):
        for i in self.viewers:
            i.grid_forget()
        if not skip_ian:
            self.img.active_fname = self.active_ir = None

    def set_text(self, text):
        self.clear()

        self.text['state'] = 'normal'
        self.text.delete('1.0', 'end')
        self.text.insert('end', text)
        self.text['state'] = 'disabled'

        self.text.grid(column=0, row=0, sticky=tk.NSEW)

    def set_raw(self, data):
        if isinstance(data, bytes):
            data = utils.bytes2hex(data)
        self.set_text(data)

    def set_tlm(self, tlm, fname):
        self.clear()

        self.tlm.fill(tlm, fname)
        self.tlm.grid(column=0, row=0, sticky=tk.NSEW)

    def set_img(self, ir, fname, select=0):
        if not self.img.fill_canvas(ir, fname, select):
            self.clear(1)
            self.img.grid(column=0, row=0, sticky=tk.NSEW)


class DecoderFrame(ttk.Frame):
    decoders = {
        'geoscan': systems.GeoscanProtocol,
        'usp': systems.UspProtocol,
    }

    def __init__(self, master, config, proto, name=None):
        super().__init__(master)
        self.config = config
        self.proto = proto
        self.name = name or proto
        self.sk = 0
        self.decoder = self.decoders[proto](self.config.get(proto, 'outdir'))

        self.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(1, weight=1)
        # self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ctrl frame
        self.ctrl_frame = ttk.LabelFrame(self, text='Options', padding=(3, 3, 3, 3))
        self.ctrl_frame.grid(column=0, row=0, sticky=tk.NSEW, padx=2, pady=2)
        self.ctrl_frame.columnconfigure(1, weight=1)
        self.ctrl_frame.columnconfigure(4, weight=1)

        self.out_dir_v = tk.StringVar(self.ctrl_frame, self.config.get(proto, 'outdir'))
        self.out_dir_e = ttk.Entry(self.ctrl_frame, textvariable=self.out_dir_v, state=tk.NORMAL)
        self.out_dir_e.grid(column=0, columnspan=4, row=0, sticky=tk.EW, pady=3)

        self.out_dir_btn = ttk.Button(self.ctrl_frame, text='Out Dir', command=self.set_out_dir)
        self.out_dir_btn.grid(column=4, row=0, sticky=tk.EW, pady=3, padx=3)

        self.server_v = tk.StringVar(self.ctrl_frame, self.config.get(proto, 'ip'))
        self.port_v = tk.StringVar(self.ctrl_frame, self.config.get(proto, 'port'))

        ttk.Label(self.ctrl_frame, text='Server:').grid(column=0, row=1, sticky=tk.E, pady=3)
        self.server_e = ttk.Entry(self.ctrl_frame, textvariable=self.server_v)
        self.server_e.grid(column=1, row=1, sticky=tk.EW, pady=3)

        ttk.Label(self.ctrl_frame, text='Port:').grid(column=2, row=1, sticky=tk.E, pady=3)
        self.port_e = ttk.Entry(self.ctrl_frame, textvariable=self.port_v, width=7)
        self.port_e.grid(column=3, row=1, sticky=tk.EW, pady=3)

        self.con_btn = ttk.Button(self.ctrl_frame, text='Connect', command=self.con)
        self.con_btn.grid(column=4, row=1, sticky=tk.EW, pady=3, padx=3)

        self.merge_mode_v = tk.IntVar(self.ctrl_frame, self.config.getboolean(proto, 'merge mode'))
        self.merge_mode_ckb = ttk.Checkbutton(self.ctrl_frame, text='Merge mode',
                                              variable=self.merge_mode_v, command=self.set_merge_mode)
        self.merge_mode_ckb.grid(column=2, columnspan=2, row=2, sticky=tk.EW, pady=3)

        self.new_btn = ttk.Button(self.ctrl_frame, text='New image', command=self.new_img)
        self.new_btn.grid(column=4, row=2, sticky=tk.EW, pady=3, padx=3)

        # history frame
        self.history_frame = HistoryFrame(self)
        self.history_frame.grid(column=0, row=1, sticky=tk.NSEW, padx=2, pady=2)
        self.bind(self.history_frame.EVT_SEL, self.fill_data)

        # data view frame
        self.dv_frame = DataViewFrame(self)
        self.dv_frame.grid(column=1, row=0, rowspan=2, sticky=tk.NSEW, padx=2, pady=2)

    def fill_data(self, evt=None):
        x = self.history_frame.get_selected()
        if not x:
            self.dv_frame.clear()
            return

        tag = x.tags[0]
        vals = self.history_frame.vals[x.iid]

        if tag == 'tlm':
            self.dv_frame.set_tlm(vals[-2], vals[-1])
        elif tag == 'ascii':
            self.dv_frame.set_text(vals[-1])
        elif tag == 'img':
            self.dv_frame.set_img(vals[-2], vals[-1], 1)
        else:   # raw, etc
            self.dv_frame.set_raw(vals[-1])

    def set_out_dir(self):
        d = filedialog.askdirectory()
        if d:
            self.out_dir_v.set(d)

    def con(self):
        self.stop() if self.sk else self._start()

    def set_merge_mode(self):
        self.decoder.ir.set_merge_mode(self.merge_mode_v.get())

    def new_img(self):
        fn = self.decoder.ir.force_new().fn
        self.dv_frame.set_img(self.decoder.ir, fn, 1)
        self.history_frame.put('img', self.proto, self.decoder.ir, fn)

    def stop(self):
        if self.sk:
            s = self.sk
            self.sk = 0
            s.close()

        self.con_btn.config(text='Connect')
        self.server_e.config(state=tk.NORMAL)
        self.port_e.config(state=tk.NORMAL)
        self.out_dir_e.config(state=tk.NORMAL)
        self.out_dir_btn.config(state=tk.NORMAL)
        self.update()

    def _start(self):
        try:
            s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
            s.connect((self.server_v.get(), int(self.port_v.get())))
            s.settimeout(0.1)

            self.sk = s
            self.sk.send(AGWPE_CON)

        except (ConnectionError, OSError) as e:
            messagebox.showerror(message='%s: %s' % (self.name, e.strerror))

        except Exception as e:
            messagebox.showerror(message='%s: %s' % (self.name, e.args))

        else:
            self.con_btn.config(text='Disconnect')
            self.server_e.config(state=tk.DISABLED)
            self.port_e.config(state=tk.DISABLED)
            self.out_dir_e.config(state=tk.DISABLED)
            self.out_dir_btn.config(state=tk.DISABLED)
            self.update()

            self.decoder.ir.set_outdir(self.out_dir_v.get())
            self.decoder.ir.set_merge_mode(self.merge_mode_v.get())
            try:
                self._receive()
            except Exception as e:
                messagebox.showerror(message='%s: %s' % (self.name, e))
                self.stop()
                raise e

    def _receive(self):
        while self.sk:
            try:
                frame = self.sk.recv(4096)
            except (sk.timeout, TimeoutError):
                continue
            finally:
                self.update()

            if not frame:
                messagebox.showwarning(message='%s: Connection lost' % self.name)
                self.stop()
                return

            data = frame[37:]
            for i in self.decoder.recognize(data):
                args = i
                ty, name, *_, packet = i
                date = 0

                if ty == 'img':
                    ir_ret, fname = packet
                    self.dv_frame.set_img(self.decoder.ir, fname)
                    args = args[:-1] + (self.decoder.ir, fname)

                elif ty == 'tlm':
                    packet, tlm = packet
                    name = ('%s_%s_%s.txt' % (name, self.proto, tlm.Time)).replace(
                        ' ', '_').replace(':', '-')
                    fp = pathlib.Path(self.out_dir_v.get()) / name
                    # self.dv_frame.set_tlm(tlm, fp)
                    args = args[:-1] + (tlm, fp)
                    date = tlm.Time

                    with fp.open('w') as f:
                        f.write(utils.bytes2hex(data))
                        f.write('\n\n')
                        f.write(str(packet))

                # elif ty == 'ascii':
                #     self.dv_frame.set_text(packet)

                # else:   # raw, etc
                #     self.dv_frame.set_raw(packet)

                self.history_frame.put(*args, date=date)


class App(ttk.Frame):
    def __init__(self, config):
        super().__init__()
        self.ico = PIL.Image.open(RES / 'icon.png')
        self.master.iconphoto(False, PIL.ImageTk.PhotoImage(self.ico))

        self.config = config

        if self.config.has_option('main', 'pos'):
            self.master.geometry(self.config.get('main', 'pos'))

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

        # Notebook frame
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(column=0, row=0, sticky=tk.NSEW)
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)

        self.tabs = {}
        for proto in PROTOCOLS:
            f = DecoderFrame(self.notebook, config, proto)
            self.notebook.add(f, text=proto)
            self.tabs[f.name] = f

        #####
        self.update()
        self.master.minsize(self.winfo_width(), self.winfo_height())

    def exit(self, evt=None):
        for name, df in self.tabs.items():
            if df.sk:
                df.stop()
            self.config.set(name, 'ip', df.server_v.get())
            self.config.set(name, 'port', df.port_v.get())
            self.config.set(name, 'outdir', df.out_dir_v.get())
            self.config.set(name, 'merge mode', str(df.merge_mode_v.get()))

        self.config.set('main', 'pos', self.master.winfo_geometry())
        self.quit()

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
        about.grab_set()
        about.resizable(width=False, height=False)
        about.title('About')
        about.bind('<KeyPress>', sequence_check)

        frame = ttk.Frame(about, padding=(10, 6, 10, 6))
        frame.grid(column=0, row=0, sticky=tk.NSEW)

        ttk.Label(frame, text=f'SatsDecoder v{__version__}').grid(columnspan=2)
        ttk.Label(frame, text='MIT License\nCopyright (c) 2024 Alexander Baskikh\n', justify='center').grid(columnspan=2, rowspan=3)

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
                             command=lambda: threading.Thread(target=self.check_updates, args=(about, btns_frame,)).start())
        upd_btn.grid(column=0, row=0)

        ok_btn = ttk.Button(btns_frame, text='Ok', command=lambda: (about.grab_release(), about.destroy()))
        ok_btn.grid(column=1, row=0)

        about.update()

    @staticmethod
    def check_updates(about, btns_frame):
        m = re.match(r'([\d.]+).*', __version__)
        if m:
            v = tuple(map(int, m.group(1).split('.')))
        else:
            messagebox.showerror(message=f'Invalid version, can\'t be compared: {__version__}')
            return

        try:
            with urllib.request.urlopen(urllib.request.Request(
                    'https://api.github.com/repos/baskiton/SatsDecoder/releases/latest',
                    headers={'accept': 'application/vnd.github+json'})) as r:
                resp = json.load(r)
        except urllib.error.URLError as e:
            messagebox.showerror(message=str(e))
            return

        if v < tuple(map(int, resp['tag_name'].split('.'))):
            fg = 'green'
            msg = resp['tag_name']
        else:
            fg = 'red'
            msg = 'not found'

        for i in btns_frame.winfo_children():
            if isinstance(i, ttk.Label):
                i.config(text=f'New version: {msg}', foreground=fg)
                break
        else:
            ttk.Label(btns_frame, text=f'New version: {msg}', foreground=fg, justify='center').grid(columnspan=2)

        about.update()
