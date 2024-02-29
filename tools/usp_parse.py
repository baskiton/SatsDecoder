import itertools
import pathlib
import sys
import xml.etree.ElementTree as ET


class Device:
    def __init__(self, model, desc):
        self.model = model
        self.desc = desc or model
        self.packets = []

    def add_packet(self, packet):
        self.packets.append(packet)

    def generate(self):
        pass


class Packet:
    def __init__(self, name, desc, id, len, type):
        self.name = name.strip().replace(' ', '_').replace('.', '_')
        self.desc = desc or name
        self.id = id
        self.len = len
        self.fields = []
        self.type = type

    def add_field(self, field):
        self.fields.append(field)

    def _gen_pad(self, n, sz):
        if sz == 1:
            x = 'construct.Flag'
        else:
            x = f'construct.BitsInteger({sz})'
        return f'    \'_pad{n}\' / {x},'

    def generate(self):
        main_lines = [
            f'{self.name} = construct.Struct(',
            f'    \'_name\' / construct.Computed({self.name!r}),',
            f'    \'name\' / construct.Computed({self.name!r}),',
            f'    \'desc\' / construct.Computed({self.desc!r}),',
        ]
        flags = []

        in_flag = 0
        off_expected = 0
        pad_num = 0

        tlm_table = {'table': [], 'flags': []}
        self.fields.sort(key=(lambda x: x.off))
        for f in self.fields:
            line = f.generate()
            tab = f.name, f.desc
            pad = ''
            pad_len = f.off - off_expected
            if pad_len:
                pad = self._gen_pad(pad_num, pad_len)
                pad_num += 1

            if f.is_flag or (pad and f.len % 8):
                if not in_flag:
                    main_lines.append(f'    \'flags{len(flags)}\' / {self.name}_flags{len(flags)},')
                    in_flag = 1
                    flags.append([f'{self.name}_flags{len(flags)} = construct.BitStruct('])
                if pad:
                    flags[-1].append(pad)
                flags[-1].append(line)
                if not tab[0].startswith('_'):
                    tlm_table['flags'].append(tab)

            else:
                if in_flag:
                    in_flag = 0
                    if pad:
                        flags[-1].append(pad)
                        pad = ''
                    flags[-1].append(')')
                if pad:
                    main_lines.append(pad)
                main_lines.append(line)
                if not tab[0].startswith('_'):
                    tlm_table['table'].append(tab)

            off_expected += f.len + pad_len

        if in_flag:
            in_flag = 0
            flags[-1].append(')')

        main_lines.append(')')


        self.ID = f'{self.name.upper()} = 0x{self.id:04X}'
        self.FLAGS = [*itertools.chain.from_iterable(flags)]
        self.MAIN = main_lines
        self.MAPPED = f'    {self.name.upper()}: {self.name!r} / {self.name},'
        self.TLM_TABLE = [
            f'        {self.name!r}: {{',
            f'            \'table\': (',
            f'                (\'name\', \'Name\'),',
            f'                (\'desc\', \'Description\'),',
            *(f'                ({i[0]!r}, {i[1]!r}),' for i in tlm_table['table']),
            f'            ),',
        ]
        x = tlm_table['flags']
        if x:
            self.TLM_TABLE += [
                f'            \'flags\': (',
                *(f'                ({i[0]!r}, {i[1]!r}),' for i in x),
                f'            ),',
            ]
        self.TLM_TABLE.append(f'        }},')


class Field:
    def __init__(self, name, desc, type, off, len, byteorder):
        if 'reserv' in name.lower():
            name = '_' + name
        if type == 'file':
            type = 'data'
        self.name = name.strip().replace(' ', '_').replace('.', '_')
        self.desc = desc or name
        self.type = type
        self.off = off
        self.len = len
        self.byteorder = byteorder
        self.is_flag = 0
        self.is_time = (type == 'time_t') or ('time' in name.lower() and type.endswith('int') and len in (32, 64))

    def generate(self):
        bo = self.byteorder == 'BE' and 'b' or 'l'
        nam = self.name
        # if nam.lower().startswith('reserv'):
        #     nam = '_' + self.name
        ty = self.type[0]
        if ty == 'u':
            si = 'u'
        elif ty in 'it':
            si = 's'
        else:
            si = ''

        # tys = ''
        if self.type == 'string':
            if self.len:
                tys = f'construct.PaddedString({self.len}, \'utf-8\')'
            else:
                tys = f'construct.GreedyString(\'utf-8\')'
        elif self.type == 'data':
            if self.len:
                tys = f'construct.Bytes({self.len})'
            else:
                tys = 'construct.GreedyBytes'
        elif nam[0] == '_' or self.type == 'bit' or self.len % 8:
            self.is_flag = 1
            if self.len == 1:
                tys = 'construct.Flag'
            else:
                tys = f'construct.BitsInteger({self.len})'
        elif si:
            tys = f'construct.Int{self.len}{si}{bo}'
            if self.is_time:
                tys = f'common.UNIXTimestampAdapter({tys})'
        elif ty == 'f':
            tys = f'construct.Float{self.len}{bo}'

        return f'    {self.name!r} / {tys},  # {self.desc}'


types = set()
ptypes = set()


def parse_file(fp):
    tree = ET.parse(fp, ET.XMLParser(encoding='utf-8'))
    ns = {'': 'unican_device_schema'}

    dev_model = tree.find('./DevModel', ns).text
    dev_desc = tree.find('./DevDesc', ns).text
    d = Device(dev_model, dev_desc)

    for pack in tree.findall('./Packet', ns):
        pack_id = pack.find('PacId', ns).text
        pack_id = int(pack_id, pack_id.startswith('0x') and 16 or 10)
        pack_name = pack.find('PacName', ns).text
        pack_desc = pack.find('PacDesc', ns).text
        pack_type = pack.find('PacType', ns).text
        data_len = int(pack.find('DataLen', ns).text)
        p = Packet(pack_name, pack_desc, pack_id, data_len, pack_type)
        d.add_packet(p)
        ptypes.add(pack_type)

        for field in pack.findall('Field', ns):
            f_type = field.find('FldType', ns).text
            f_name = field.find('FldName', ns).text
            f_desc = field.find('FldDesc', ns).text
            f_off = int(field.find('FldOffset', ns).text)
            f_len = int(field.find('FldLen', ns).text)
            f_bo = field.find('FldByteOrder', ns).text
            f = Field(f_name or f_desc, f_desc, f_type, f_off, f_len, f_bo)
            p.add_field(f)
            types.add((f_type, f_len))

        p.generate()

    return d


if __name__ == '__main__':
    dn = 'resources/devices/'
    out_fn = 'usp2.py'

    packets = []
    for fn in pathlib.Path(dn).iterdir():
        try:
            d = parse_file(fn)
            for p in d.packets:
                packets.append(p)
        except Exception as e:
            print(f'Err in {fn}', file=sys.stderr)
            raise

    packets.sort(key=lambda x: x.id)
    hdrs = ['import construct',
            '',
            'from SatsDecoder.systems import common',
            '']
    ids = []
    mains = []
    maps = ['tlm_map = {']
    tlm_table = ['',
                 'class UspProtocol:',
                 '    tlm_table = {']
    for p in packets:
        ids.append(p.ID)
        mains += p.FLAGS + p.MAIN
        mains.append('')
        maps.append(p.MAPPED)
        tlm_table += p.TLM_TABLE
    ids.append('')
    maps += ['}', '']
    tlm_table += ['    }', '']

    with open(out_fn, 'w+') as f:
        for ls in hdrs, ids, mains, maps, tlm_table:
            for l in ls:
                f.write(l)
                f.write('\n')
