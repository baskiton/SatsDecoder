#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import itertools

'''
SONATE-2 telemetry description in xls file:
    https://www.informatik.uni-wuerzburg.de/en/aerospaceinfo/mitarbeiter/kayal/forschungsprojekte/sonate-2/information-for-radio-amateurs/
'''


if __name__ == '__main__':
    apids = {}
    sonate2_map = ['sonate2_map = {']
    with open('sonate2-apids', 'r') as f:
        for line in f.readlines():
            apid, name = line.split(';')
            name = name.strip().lower().replace(' ', '_').replace('-', '_')
            sonate2_map.append(f'    0x{apid}: {name},')
            apids[apid] = name

    sonate2_map.append('}')

    calibs = {}
    strus = {}
    tabs = {}
    off_expected = pad_num = 0
    with open('sonate2-data-def', 'r') as f:
        _apid = ''
        for _line in f.readlines():
            line = _line.strip()
            if not line:
                continue
            apid, param, desc, unit, bits, off, calib = line.split(';')
            off = int(off)
            calib = calib.strip()

            stru = strus.get(apid)
            tab = tabs.get(apid)
            if not stru:
                x = off_expected % 8
                if x:
                    strus.get(_apid).insert(-1, f'    \'_pad{pad_num}\' / construct.BitsInteger({8 - x}),')

                off_expected = pad_num = 0
                stru = ['',
                        f'{apids[apid]} = construct.BitStruct(',
                        f'    \'_name\' / construct.Computed({apids[apid]!r}),',
                        f'    \'name\' / construct.Computed({apids[apid].upper().replace("_", " ")!r}),',
                        ')']
                strus[apid] = stru
                tab = [f'        {apids[apid]!r}: {{',
                       f'            \'table\': (',
                       f'                (\'name\', \'Name\'),',
                       f'            ),',
                       f'        }},']
                tabs[apid] = tab

            _apid = apid
            pad_len = off - off_expected
            off_expected = off + int(bits)
            if pad_len:
                if pad_len == 1:
                    ty = 'construct.Flag'
                elif pad_len < 0:
                    raise ValueError
                else:
                    ty = f'construct.BitsInteger({pad_len})'
                stru.insert(-1, f'    \'_pad{pad_num}\' / {ty},')
                pad_num += 1

            ty = f'construct.BitsInteger({bits})'
            if 'x' in calib:
                ty = f'common.EvalAdapter({calib.replace("^", "**")!r}, {ty})'
            elif '=' in calib:
                d = {}
                for i in calib.split(', '):
                    v, _, k = i.partition('=')
                    d[k] = int(v)
                dd = tuple(set(d.items()))
                i = calibs.get(dd)
                if not i:
                    ename = f'enum_{len(calibs)}'
                    i = f'{ename} = construct.Enum({ty}, **{d!r})', ename
                    calibs[dd] = i
                ty = i[1]
            elif unit in ('s', 'sec') and 'TIME' in desc and not calib:
                if 'UTC' in desc:
                    ty = f'common.UNIXTimestampAdapter({ty})'
                    calib = ''
                elif 'UP' in desc:
                    ty = f'common.TimeDeltaAdapter({ty})'
                    calib = ''

            stru.insert(-1, f'    {param!r} / {ty},{calib and f"  # {calib}"}')
            if unit:
                desc += f', {unit}'
            tab.insert(-2, f'                ({param!r}, {desc!r}),')

    for i, l in enumerate(sonate2_map[1:-1]):
        apid = l[6:9]
        if apid not in strus:
            # sonate2_map[i + 1] = l.replace('    ', '    # ')
            strus[apid] = ['',
                           f'{apids[apid]} = construct.BitStruct(',
                           f'    \'_name\' / construct.Computed({apids[apid]!r}),',
                           f'    \'name\' / construct.Computed({apids[apid].upper().replace("_", " ")!r}),',
                           f'    \'data\' / construct.GreedyBytes,',
                           ')']
            tabs[apid] = [f'        {apids[apid]!r}: {{',
                          f'            \'table\': (',
                          f'                (\'name\', \'Name\'),',
                          f'                (\'data\', \'data\'),',
                          f'            ),',
                          f'        }},']

    out_fn = 'sonate2.py'
    hdrs = ['import construct',
            '',
            'from SatsDecoder.systems import ccsds, common',
            '',
            '__all__ = \'SonateProtocol\',',
            '',
            '\n'.join(map(lambda x: x[0], calibs.values()))]
    tlm_table = ['', '',
                 'class SonateProtocol:',
                 '    columns = \'APID\',',
                 '    c_width = 60,',
                 '',
                 '    tlm_table = {',
                 *itertools.chain.from_iterable(tabs.values()),
                 '    }',
                 ]

    with open(out_fn, 'w+') as f:
        for ls in hdrs, itertools.chain.from_iterable(strus.values()), sonate2_map, tlm_table:
            for l in ls:
                f.write(l)
                f.write('\n')
