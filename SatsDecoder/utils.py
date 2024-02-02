import sys


class Dict(dict):
    def __getattr__(self, name):
        return super().__getattr__(name) if name.startswith('__') else self[name]

    def __setattr__(self, name, value):
        if name.startswith('__'):
            super().__setattr__(name, value)
        else:
            self[name] = value

    def __delattr__(self, name):
        if name.startswith('__'):
            super().__delattr__(name)
        else:
            del self[name]


def bytes2hex(data):
    return data.hex(*((' ',) if sys.version_info >= (3, 8, 0) else ()))


seqs_map = {
    '\x72\x73\x32\x30\x73': 'aHR0cHM6Ly91cGxvYWQud2lraW1lZGlhLm9yZy93aWtpcGVkaWEvY29tbW9u'
                            'cy90aHVtYi80LzRhL0N1YmVTYXRfR2Vvc2Nhbi1FZGVsdmVpc19lbWJsZW0u'
                            'anBnLyVzcHgtQ3ViZVNhdF9HZW9zY2FuLUVkZWx2ZWlzX2VtYmxlbS5qcGc=',
    '\x72\x73\x31\x35\x73': 'aHR0cHM6Ly9zcHV0bml4LnJ1L3RwbC9pbWcvbG9nby16b3JraXkuanBnPyVz',
}
