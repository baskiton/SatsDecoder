#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import configparser

from SatsDecoder import CONFIG, HOMEDIR, ui
from SatsDecoder.systems import PROTOCOLS
from SatsDecoder.version import __version__


if __name__ == '__main__':
    cp = configparser.ConfigParser()
    d = {'main': {},
         'info': {'version': __version__}}
    for proto in PROTOCOLS:
        d[proto] = {'ip': '127.0.0.1',
                    'port': '8000',
                    'connmode': '0',
                    'merge mode': 'off',
                    'outdir': str(HOMEDIR / proto)}
    cp.read_dict(d)
    cp.read(CONFIG)

    app = ui.App(cp)
    app.mainloop()

    with CONFIG.open('w') as cf:
        cp.write(cf)
