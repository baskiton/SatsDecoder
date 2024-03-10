#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import configparser

from SatsDecoder import CONFIG, ui
from SatsDecoder.version import __version__


if __name__ == '__main__':
    cp = configparser.ConfigParser()
    d = {'main': {},
         'info': {'version': __version__}}
    cp.read_dict(d)
    cp.read(CONFIG)

    app = ui.App(cp)
    app.mainloop()

    with CONFIG.open('w') as cf:
        cp.write(cf)
