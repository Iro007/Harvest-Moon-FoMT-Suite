import json
from data_analysis import ROM


def pretty_time(raw_time):
    return f"{6 + raw_time // 60:02}:{raw_time % 60:02}"


def decode_path_point_a(rom: ROM, addr: int):
    # lo = rom.u32(addr)
    hi = rom.u32(addr + 4)

    # bit fields
    is_vertical = 1 & hi

    coord_key = "x_coord" if not is_vertical else "y_coord"

    return {
        "instant": rom.u16(addr),
        coord_key: rom.u16(addr + 2),
    }


def decode_path_point_b(rom: ROM, addr: int):
    # lo = rom.u32(addr)
    hi = rom.u32(addr + 4)

    # bit fields
    facing = 3 & (hi >> 16)
    is_vertical = 1 & (hi >> 18)

    coord_key = "x_coord" if not is_vertical else "y_coord"

    return {
        coord_key: rom.u16(addr),
        "speed": rom.u16(addr + 2),
        "unk_04": rom.u16(addr + 4),
        "facing": facing,
    }


def decode_path(rom: ROM, addr: int):
    points_addr = rom.u32(addr)
    num_points = rom.u16(addr + 4)
    x_start = rom.u16(addr + 6)
    y_start = rom.u16(addr + 8)
    half_0A = rom.u16(addr + 10)

    location_start = 0x3FF & half_0A
    facing_start = 0x3 & (half_0A >> 10)
    point_select = 1 & (half_0A >> 12)

    if points_addr != 0:
        if point_select == 0:
            points = [
                decode_path_point_a(rom, points_addr + i * 8) for i in range(num_points)
            ]
        else:
            points = [
                decode_path_point_b(rom, points_addr + i * 8) for i in range(num_points)
            ]

    else:
        points = None

    return {
        "x_start": x_start,
        "y_start": y_start,
        "location_start": location_start,
        "facing_start": facing_start,
        "points": points,
    }


def visit_schedule_paths(rom: ROM, addr: int, out_path_addrs: set[int]):
    num_entries = rom.u16(addr)
    entries_addr = rom.u32(addr + 4)

    for i in range(num_entries):
        entry_addr = entries_addr + i * 8
        path_addr = rom.u32(entry_addr + 4)

        out_path_addrs.add(path_addr)


def decode_schedule(rom: ROM, addr: int, path_addr_to_id: dict[int, int]):
    num_entries = rom.u16(addr)
    entries_addr = rom.u32(addr + 4)

    entries = []

    for i in range(num_entries):
        entry_addr = entries_addr + i * 8

        time = rom.u16(entry_addr)  # time
        path_addr = rom.u32(entry_addr + 4)

        # path = decode_path(rom, path_addr)

        entries.append({"time": pretty_time(time), "path": path_addr_to_id[path_addr]})

    return entries


def decode_schedule_info(rom: ROM, addr: int):
    select_schedule_func = rom.u32(addr)  # select_schedule_func
    num_schedules = rom.u32(addr + 4)
    schedules_addr = rom.u32(addr + 8)

    path_addrs = set()

    # schedules can share paths, so we want to discover all paths ahead of time
    for i in range(num_schedules):
        schedule_addr = rom.u32(schedules_addr + i * 4)

        if schedule_addr != 0:
            visit_schedule_paths(rom, schedule_addr, path_addrs)

    # sort by addr and build map
    path_addrs = sorted(path_addrs)
    path_addr_to_id = {addr: i for i, addr in enumerate(path_addrs)}

    schedules = []

    for i in range(num_schedules):
        schedule_addr = rom.u32(schedules_addr + i * 4)

        if schedule_addr != 0:
            schedules.append(decode_schedule(rom, schedule_addr, path_addr_to_id))
        else:
            schedules.append(None)

    paths = []

    for path_addr in path_addrs:
        path = decode_path(rom, path_addr)
        paths.append(path)

    return {
        "select_schedule": f"func_{select_schedule_func - 1:08X}",
        "schedules": schedules,
        "paths": paths,
    }


def main(args: list[str]) -> str | None:
    try:
        rom_path = args[1]
        schedule_info_addr = int(args[2], base=0)

    except IndexError:
        return f"Usage: {args[0]} ROM ADDR"

    with open(rom_path, "rb") as f:
        rom = ROM(f.read())

    schedule_info = decode_schedule_info(rom, schedule_info_addr)
    schedule_info["name"] = f"Unk_{schedule_info_addr:08X}"
    print(json.dumps(schedule_info, indent=4))


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
