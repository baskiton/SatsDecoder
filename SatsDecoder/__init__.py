#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import pathlib


HOMEDIR = pathlib.Path('~/SatsDecoder').expanduser().absolute()
CONFIG = HOMEDIR / 'config.ini'
RES = pathlib.Path(__file__).parent.parent / 'res'
