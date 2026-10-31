import re


class ROM:
    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    def u8(self, offset_or_addr: int) -> int:
        offset = offset_or_addr & 0x1FFFFFF
        return self.data[offset]

    def u16(self, offset_or_addr: int) -> int:
        offset = offset_or_addr & 0x1FFFFFF
        return int.from_bytes(self.data[offset : offset + 2], byteorder="little")

    def u32(self, offset_or_addr: int) -> int:
        offset = offset_or_addr & 0x1FFFFFF
        return int.from_bytes(self.data[offset : offset + 4], byteorder="little")


RE_NAME_DECOMPOSE = re.compile(r"(?P<name>\w+).*")


def name_without_type_stuff(typed: str) -> str:
    m = RE_NAME_DECOMPOSE.match(typed)
    return m.group("name")


class DataInfo:
    addr: int
    size: int
    kind: str
    name: str

    def __init__(self, addr: int, size: int, kind: str, name: str | None):
        self.addr = addr
        self.size = size
        self.kind = kind
        self.name = (
            name
            if name is not None
            else f"{name_without_type_stuff(kind)}_Unk_{addr:08X}"
        )


RE_KIND_ARRAY = re.compile(r"(?P<inner>.+)\[(?P<size>\w+)\]")
RE_KIND_POINTER = re.compile(r"(?P<inner>.+)\*")


class ROMAnalyzer:
    rom: ROM
    data_dict: dict[int, DataInfo]
    type_sizes: dict[str, int]

    def __init__(self, rom: ROM):
        self.rom = rom
        self.data_dict = {}
        self.type_sizes = {}

    def register_type(self, name: str, size: int):
        self.type_sizes[name] = size

    def register_types(self, type_sizes: dict[str, int]):
        for name in type_sizes:
            self.type_sizes[name] = type_sizes[name]

    def sizeof(self, kind: str):
        m = RE_KIND_ARRAY.match(kind)

        if m is not None:
            inner = m.group("inner")
            size = int(m.group("size"), base=0)
            return self.sizeof(inner) * size

        m = RE_KIND_POINTER.match(kind)

        if m is not None:
            return 4

        return self.type_sizes[kind]

    def is_leaf_type(type_name: str) -> bool:
        return "*" not in type_name and "[" not in type_name

    def walk_data_rec(self, root_info: DataInfo, leaf_handler):
        addr = root_info.addr

        m = RE_KIND_ARRAY.match(root_info.kind)

        if m is not None:
            inner = m.group("inner")
            size = int(m.group("size"), base=0)
            element_size = self.sizeof(inner)

            for i in range(size):
                element = DataInfo(addr + i * element_size, element_size, inner, None)
                self.walk_data_rec(element, leaf_handler)

        m = RE_KIND_POINTER.match(root_info.kind)

        if m is not None:
            inner = m.group("inner")
            target_addr = self.rom.u32(addr)

            if target_addr != 0:
                target_size = self.sizeof(inner)
                target = DataInfo(target_addr, target_size, inner, None)

                if ROMAnalyzer.is_leaf_type(inner):
                    leaf_handler(target)

                self.walk_data_rec(target, leaf_handler)

        leaf_handler(root_info)
