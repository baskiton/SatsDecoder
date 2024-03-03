import math
import pathlib
import threading


class Image:
    BASE_OFFSET = 0     # old 4     # old 16384     # old 32768

    def __init__(self, fn):
        self.fn = fn
        self.f = None
        self.base_offset = self.BASE_OFFSET
        self.first_data_offset = math.inf
        self.has_starter = self.has_soi = 0
        self.lock = threading.Lock()
        self.open()

    def open(self):
        if not self.f:
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

            self.base_offset = off
            self.first_data_offset = 0
            f = self.open()
            f.seek(off)
            data = f.read()
            f.seek(0)
            f.write(data)
            f.truncate()
            f.flush()


class ImageReceiver:
    def __init__(self, outdir, suff=None):
        self.suff = suff
        self.outdir = pathlib.Path(outdir).expanduser().absolute()
        self.outdir.mkdir(parents=True, exist_ok=True)
        self.images = {}
        self.merge_mode = 0
        self.current_fid = None

    @property
    def cur_img(self):
        return self.images.get(self.current_fid)

    def get_image(self, force_new=0, **kwargs):
        fid = self.current_fid
        if force_new or not fid:
            fid = self.generate_fid(**kwargs)
        return self.images.get(fid) or self.new_file(fid)

    def set_outdir(self, outdir):
        self.outdir = pathlib.Path(outdir).expanduser().absolute()
        self.outdir.mkdir(parents=True, exist_ok=True)

    def set_merge_mode(self, val):
        self.merge_mode = val

    def generate_fid(self, *args, **kwargs):
        raise NotImplementedError

    def force_new(self, *args, **kwargs):
        self.current_fid = 0
        return self.new_file(self.generate_fid(*args, **kwargs))

    def new_file(self, fid):
        fn = self.outdir / fid
        if self.suff:
            fn = fn.with_suffix(self.suff)

        img = self.images.get(fid)
        if img:
            img.close()

        img = Image(fn)
        self.images[fid] = img
        return img

    def push_data(self, data):
        raise NotImplementedError

    def clear(self):
        for i in self.images.values():
            i.close()
        self.current_fid = 0
