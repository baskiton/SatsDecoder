import argparse
import configparser
import sys

from SatsDecoder import CONFIG, HOMEDIR, PROTOCOLS, ui
from SatsDecoder.version import __version__


if __name__ == '__main__':
    cp = configparser.ConfigParser()
    d = {'main': {},
         'info': {'version': __version__}}
    for proto in PROTOCOLS:
        d[proto] = {'ip': '127.0.0.1',
                    'port': '8000',
                    'merge mode': 'off',
                    'outdir': str(HOMEDIR / proto)}
    cp.read_dict(d)
    cp.read(CONFIG)

    app = ui.App(cp)
    app.mainloop()

    with CONFIG.open('w') as cf:
        cp.write(cf)
