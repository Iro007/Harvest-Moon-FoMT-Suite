import sys
import json
import re
from collections import defaultdict


schedule_info = json.load(sys.stdin)


# (declaration, definition)
to_print: dict[str, list[tuple[str, str]]] = defaultdict(list)

KEY_SCHEDULE_INFO = "si"
KEY_SCHEDULE_LIST = "sl"
KEY_SCHEDULE = "sc"
KEY_SCHEDULE_ENTRY = "se"
KEY_PATH_INFO = "pi"
KEY_PATH_POINTS = "pp"

KEYS_IN_ORDER = [
    KEY_SCHEDULE_INFO,
    KEY_SCHEDULE_LIST,
    KEY_SCHEDULE,
    KEY_SCHEDULE_ENTRY,
    KEY_PATH_INFO,
    KEY_PATH_POINTS,
]

RE_TIME = re.compile(r"(?P<hours>\w+):(?P<minutes>\w+)")


def depretty_time(prettied_time: str) -> int:
    m = RE_TIME.match(prettied_time)

    hours = int(m.group("hours"))
    minutes = int(m.group("minutes"))

    return (hours - 6) * 60 + minutes


def emit_path_points_a(points: list[dict], name: str):
    num_points = len(points)

    # PathPointA

    decl = f"extern PathPointA const {name}[{num_points}];"

    lines = []
    lines.append(f"PathPointA const {name}[{num_points}] = {{")

    for point in points:
        fields = []
        fields.append(f"{point['instant']}")

        if "x_coord" in point:
            fields.append(f"{point['x_coord']}")
            fields.append("0")
        else:
            fields.append(f"{point['y_coord']}")
            fields.append("1")

        lines.append(f"    {{ {', '.join(fields)} }},")

    lines.append("};")
    body = "\n".join(lines)

    to_print[KEY_PATH_POINTS].append((decl, body))


def emit_path_points_b(points: list[dict], name: str):
    num_points = len(points)

    # PathPointB

    decl = f"extern PathPointB const {name}[{num_points}];"

    lines = []
    lines.append(f"PathPointB const {name}[{num_points}] = {{")

    for point in points:
        fields = []
        is_y = "0"

        if "x_coord" in point:
            fields.append(f"{point['x_coord']}")
            is_y = "0"
        else:
            fields.append(f"{point['y_coord']}")
            is_y = "1"

        fields.append(f"{point['speed']}")
        fields.append(f"{point['unk_04']}")
        fields.append(f"{point['facing']}")
        fields.append(is_y)

        lines.append(f"    {{ {', '.join(fields)} }},")

    lines.append("};")
    body = "\n".join(lines)

    to_print[KEY_PATH_POINTS].append((decl, body))


def emit_path(path: dict, name: str):
    points_name = f"{name}_Points"
    has_points = path["points"] is not None

    if has_points:
        num_points = len(path["points"])
        point_type_select = 1 if "facing" in path["points"][0] else 0

        # emit points

        if point_type_select == 0:
            emit_path_points_a(path["points"], points_name)
        else:
            emit_path_points_b(path["points"], points_name)

    else:
        num_points = 0
        point_type_select = 0

    # PathInfo

    decl = f"extern PathInfo const {name};"

    lines = []
    lines.append(f"PathInfo const {name} = {{")
    if has_points:
        lines.append(f"    (void const *){points_name}, /* points */")
    else:
        lines.append("    nullptr, /* points */")
    lines.append(f"    {num_points}, /* num_points */")
    lines.append(f"    {path['x_start']}, /* x_start */")
    lines.append(f"    {path['y_start']}, /* y_start */")
    lines.append(f"    {path['location_start']}, /* location_start */")
    lines.append(f"    {path['facing_start']}, /* facing_start */")
    lines.append(f"    {point_type_select}, /* point_type_select */")
    lines.append("};")
    body = "\n".join(lines)

    to_print[KEY_PATH_INFO].append((decl, body))


def emit_schedule(schedule: list[dict], name: str, path_names: list[str]):
    entries_name = f"{name}_Entries"
    num_entries = len(schedule)

    # Schedule

    decl = f"extern Schedule const {name};"

    lines = []
    lines.append(f"Schedule const {name} = {{")
    lines.append(f"    {num_entries}, {entries_name}")
    lines.append("};")
    body = "\n".join(lines)

    to_print[KEY_SCHEDULE].append((decl, body))

    # ScheduleEntry[]

    decl = f"extern ScheduleEntry const {entries_name}[{num_entries}];"

    lines = []
    lines.append(f"ScheduleEntry const {entries_name}[{num_entries}] = {{")

    # paths = []

    for i in range(num_entries):
        entry = schedule[i]

        time = depretty_time(entry["time"])
        path_name = path_names[entry["path"]]

        # path_name = f"{name}_{i}_Path"
        # paths.append((path_name, entry["path"]))

        lines.append(f"    {{ {time}, &{path_name} }}, /* {entry['time']} */")

    lines.append("};")
    body = "\n".join(lines)

    to_print[KEY_SCHEDULE_ENTRY].append((decl, body))

    # SchedulePath

    # for name, path in paths:
    #     emit_path(path, name)


def emit_schedule_info(schedule_info: dict):
    base_name = schedule_info["name"]
    full_name = f"ScheduleInfo_{base_name}"
    schedules_name = f"{base_name}_Schedules"
    num_schedules = len(schedule_info["schedules"])
    select_schedule = schedule_info["select_schedule"]

    # ScheduleInfo

    decl = f"extern ScheduleInfo const {full_name};"

    lines = []
    lines.append(f"ScheduleInfo const {full_name} = {{")
    lines.append(f"    {select_schedule}, {num_schedules}, {schedules_name}")
    lines.append("};")
    body = "\n".join(lines)

    to_print[KEY_SCHEDULE_INFO].append((decl, body))

    # Schedule*[]

    decl = f"extern Schedule const * const {schedules_name}[{num_schedules}];"

    lines = []
    lines.append(f"Schedule const * const {schedules_name}[{num_schedules}] = {{")

    schedules = []

    for i in range(num_schedules):
        schedule = schedule_info["schedules"][i]

        if schedule is not None:
            schedule_name = f"{base_name}_Schedule_{i}"
            schedules.append((schedule_name, schedule))
            lines.append(f"    &{schedule_name},")
        else:
            lines.append("    nullptr,")

    lines.append("};")
    body = "\n".join(lines)

    to_print[KEY_SCHEDULE_LIST].append((decl, body))

    # make path names

    path_names = []

    for i, _ in enumerate(schedule_info["paths"]):
        path_names.append(f"{base_name}_{i}_Path")

    # schedules

    for name, schedule in schedules:
        emit_schedule(schedule, name, path_names)

    # paths

    for i, path in enumerate(schedule_info["paths"]):
        emit_path(path, path_names[i])


emit_schedule_info(schedule_info)

for k in KEYS_IN_ORDER:
    for decl, _ in to_print[k]:
        print(decl)

for k in KEYS_IN_ORDER:
    for _, body in to_print[k]:
        print()
        print(body)

"""
schedule_infos = [schedule_info]
schedules = []
path_lists = []
path_infos = []
paths = []

names = {}


for schedule_info in schedule_infos:
    base_name = schedule_info["name"]
    schedules_name = f"{base_name}_Schedules"

    for i, schedule in enumerate(schedule_info["schedules"]):
        if schedule is not None:
            names[schedule] = f"{base_name}_Schedule_{i}"
            schedules.append(schedule)
"""

# print schedule info

# print schedules

# print schedule lists

# print path infos

# print paths
