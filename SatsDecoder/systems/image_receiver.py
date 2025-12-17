#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import math
import pathlib
import shutil
import sys
import threading


class Image:
    BASE_OFFSET = 0     # old 4     # old 16384     # old 32768

    def __init__(self, fn, date=0):
        self.fn = fn
        self.renamed = 0
        self.f = None
        self.packets = 0
        self.date = date
        self.base_offset = self.BASE_OFFSET
        self.first_data_offset = math.inf
        self.has_starter = self.has_soi = 0
        self.mosaic = 0
        self.lock = threading.Lock()
        self.mode = 'file'
        self.mode_kw = {}
        self.open()

    def open(self):
        if not self.f or self.f.closed:
            if self.fn.is_file():
                mode = 'r+b'
            else:
                mode = 'w+b'
                try:
                    self.fn.unlink()
                except IsADirectoryError:
                    self.fn.rmdir()
                except FileNotFoundError:
                    pass
            self.f = open(self.fn, mode)

        return self.f

    def rename(self, new_filename):
        self.close()
        old = self.fn
        new_filename = self.fn.with_name(new_filename)
        for i in range(2):
            try:
                self.fn.rename(new_filename)
                break
            except PermissionError as e:
                if not (sys.platform == 'win32' and e.winerror == 32):
                    raise
                shutil.copyfile(old, new_filename)
                break
            except FileExistsError:
                try:
                    new_filename.unlink()
                except IsADirectoryError:
                    new_filename.rmdir()
                except FileNotFoundError:
                    pass
        self.fn = new_filename
        self.renamed = old

    def rename_done(self):
        self.renamed = 0

    def flush(self):
        if self.f:
            self.f.flush()

    def close(self):
        if self.f:
            self.f.close()
            self.f = None

    def push_data(self, off, data):
        f = self.open()
        f.seek(off)
        f.write(data)
        # f.flush()

    def rebase_offset(self, off=None):
        with self.lock:
            if off is None:
                if math.isinf(self.first_data_offset):
                    return
                off = self.first_data_offset
            if not off:
                return

            off = int(off)
            self.base_offset = off
            self.first_data_offset = 0
            f = self.open()
            f.seek(off)
            data = f.read()
            f.seek(0)
            f.write(data)
            f.truncate()
            f.flush()

    def shift_image(self, n):
        f = self.open()
        data = f.read()
        f.seek(0)
        f.truncate()
        f.seek(n)
        f.write(data)
        f.flush()


class ImageReceiver:
    def __init__(self, outdir, suff=None):
        self.suff = suff
        self.outdir = pathlib.Path(outdir).expanduser().absolute()
        self.outdir.mkdir(parents=True, exist_ok=True)
        self.images = {}
        self.merge_mode = 0
        self.current_fid = ''
        self.last_date = 0

    @property
    def cur_img(self):
        return self.images.get(self.current_fid)

    def get_image(self, force_new=0, **kwargs):
        fid = self.current_fid
        if force_new or not fid:
            fid = self.generate_fid(**kwargs)
        return self.images.get(fid) or self.new_file(fid)

    def rename_image(self, old, new):
        img = self.get_image()
        img.rename(new)
        self.images.pop(old, 0)
        self.images[new] = img
        self.current_fid = new

    def set_outdir(self, outdir):
        self.outdir = pathlib.Path(outdir).expanduser().absolute()
        self.outdir.mkdir(parents=True, exist_ok=True)

    def set_merge_mode(self, val):
        self.merge_mode = val

    def generate_fid(self, *args, **kwargs):
        raise NotImplementedError

    def force_new(self, *args, **kwargs):
        self.current_fid = ''
        return self.new_file(self.generate_fid(*args, **kwargs))

    def new_file(self, fid):
        fn = self.outdir / fid
        if self.suff:
            fn = fn.with_suffix(self.suff)

        # img = self.images.get(fid)
        # if img:
        #     img.close()

        img = Image(fn, self.last_date)
        self.images[fid] = img
        return img

    def push_data(self, data, **kw):
        raise NotImplementedError

    def clear(self):
        for i in self.images.values():
            i.close()
        self.current_fid = ''
