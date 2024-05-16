#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

from SatsDecoder.systems import common

__all__ = 'RawProtocol',

proto_name = 'raw'


class RawProtocol(common.Protocol):
    columns = ()
    c_width = ()

    def recognize(self, bb):
        if bb:
            yield 'raw', 'unknown', bb
