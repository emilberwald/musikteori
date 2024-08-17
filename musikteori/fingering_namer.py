# https://ianring.com/musictheory/scales/finder/

import argparse
import io
import itertools
import pathlib
import textwrap
from typing import Sequence
import json
import importlib.resources


def format_columns_auto(text, max_line_count, max_line_length, paragraph_mark):
    paragraphs = [paragraph.splitlines() for paragraph in text.split(paragraph_mark)]
    paragraphs = [paragraph for paragraph in paragraphs if paragraph]

    # Determine the maximum length of a line in the text
    chunk_height = max(len(paragraph) for paragraph in paragraphs) + 1
    chunk_width = max(len(line) for paragraph in paragraphs for line in paragraph) + 1

    # page properties
    nof_colbands = max_line_length // chunk_width
    nof_rowbands = max_line_count // chunk_height

    merged_rows = ""
    while paragraphs:
        page = [[" "] * (max_line_length) for _ in range(max_line_count)]
        for colband in range(nof_colbands):
            pagecol_offset = colband * chunk_width
            for rowband in range(nof_rowbands):
                if not paragraphs:
                    break
                pagerow_offset = rowband * chunk_height
                paragraph = paragraphs.pop(0)
                for chunkrow, chunkrow_line in enumerate(paragraph):
                    pagerow_ix = pagerow_offset + chunkrow
                    page[pagerow_ix][pagecol_offset : pagecol_offset + chunk_width] = list(chunkrow_line)

        # Join each line of the page and then join the lines to form the final string
        merged_rows += "\n".join("".join(line) for line in page) + "\f"

    return merged_rows.rstrip("\f")


def scale_id_to_semitones(scale_id):
    semitones = []
    position = 0

    while scale_id:
        if scale_id & 1:
            semitones.append(position)
        scale_id >>= 1
        position += 1

    return semitones


def semitones_to_scale_id(semitones: Sequence[int]):
    scale_id = 0
    for semitone in semitones:
        scale_id |= 1 << semitone
    return scale_id


def get_transition_representation(
    source_semitones: Sequence[int], target_semitones: Sequence[int], *, movement_max: int
):
    source_text = get_representation(source_semitones)
    target_text = get_representation(target_semitones)
    transitions = list(source_text)
    target_list = list(target_text)
    if len(transitions) < len(target_list):
        transitions.extend("-" * (len(target_list) - len(transitions)))
    for ix, char in enumerate(source_text):
        if char.isdigit():
            # find where it should go
            if (tix := find_destination(target_list, ix)) is not None:
                target_list[tix] = "X"
                action = tix - ix
                if abs(action) > movement_max:
                    return None
                if action > 0:
                    if action <= 2:
                        for delta in range(action):
                            transitions[ix + delta] = "\\"
                    elif action <= 9:
                        transitions[ix] = "\\"
                        transitions[ix + 1] = str(abs(action))
                    else:
                        raise ValueError(f"{source_text}, {transitions}, {target_list}")
                elif action == 0:
                    transitions[ix] = "|"
                elif action < 0:
                    if abs(action) <= 2:
                        for delta in range(0, action, -1):
                            transitions[ix + delta] = "/"
                    elif abs(action) <= 9:
                        transitions[ix - 1] = str(abs(action))
                        transitions[ix] = "/"
                    else:
                        raise ValueError(f"{source_text}, {transitions}, {target_list}")

                else:
                    raise ValueError(f"{source_text}, {transitions}, {target_list}")
            else:
                transitions[ix] = "-"
    return [source_text, "".join(transitions).rstrip("-"), target_text]


def find_destination(target_list, ix):
    for tix, tchar in enumerate(target_list):
        if tchar.isdigit():
            return tix
    return None


def get_representation(semitones: Sequence):
    representation = ""
    for position in range(12):
        if position in semitones:
            representation += f"{position}-"
        else:
            representation += "-"
    return representation.strip("-")


def generate_scales(nof_fingers: int, include_open_string: bool = True):
    semitones = range(1, 12) if include_open_string else range(12)
    combinations = list(itertools.combinations(semitones, nof_fingers))

    for combo in combinations:
        yield (0,) + combo


def generate_text(source_text, transitions, target_text, scale_name, *, max_name_length):
    scale_lines = [
        line.ljust(max_name_length)
        for line in ([""] * 3 + [line for line in textwrap.wrap(scale_name, width=max_name_length, max_lines=3)])
    ][-3:]

    return "\n".join(
        [
            f"{scale_lines[0]} " + source_text + " ",
            f"{scale_lines[1]} " + transitions + " ",
            f"{scale_lines[2]} " + target_text + " ",
        ]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--fingers", default=4, type=int, help="The number of fingers")
    parser.add_argument(
        "--output-root", default=pathlib.Path().cwd(), type=pathlib.Path, help="Parent folder to the output file"
    )
    parser.add_argument(
        "--movement-max",
        default=2,
        type=int,
        help="The max number of semitones a finger can move to include the scale.",
    )
    parser.add_argument(
        "--line-length",
        default=152,
        type=int,
        help="The number of characters per line. (defaults: Courier New 8pt in landscape mode)",
    )
    parser.add_argument(
        "--line-count",
        default=52,
        type=int,
        help="The number of lines per page. (defaults: Courier New 8pt in landscape mode)",
    )
    args = parser.parse_args()

    with importlib.resources.open_text(__package__, "scales.json", encoding="utf-8") as f:
        scales = json.load(f)
    with importlib.resources.open_text(__package__, "dozenal.json", encoding="utf-8") as f:
        dozenal = json.load(f)
    scale_names = dict()
    for key, value in scales.items():
        value: str
        if value.isascii():
            scale_names[key] = value
        else:
            scale_names[key] = dozenal[key]

    max_name_length = 0
    for scale_key, scale_name in scale_names.items():
        scale_key: str
        if scale_key.isdigit():
            for word in scale_name.split():
                max_name_length = max(max_name_length, len(word))

    unformatted_text = ""
    # ¶ did not seem to be visualized as I intended
    paragraph_mark = "\n\n"
    for scale_semitones in generate_scales(args.fingers, True):
        if (
            transition_representaiton := get_transition_representation(
                [0, 2, 4, 6, 8], scale_semitones, movement_max=args.movement_max
            )
        ) is not None:
            source_text, transitions, target_text = transition_representaiton
            scale_id = semitones_to_scale_id(scale_semitones)
            scale_name = scale_names[str(scale_id)]
            unformatted_text += f"{paragraph_mark}{generate_text(source_text, transitions, target_text, scale_name, max_name_length = max_name_length)}"

    formatted_text = format_columns_auto(unformatted_text, args.line_count, args.line_length, paragraph_mark)
    formatted_output_path: pathlib.Path = args.output_root / f"fingerings-{args.fingers}.txt"
    formatted_output_path.write_text(formatted_text, encoding="utf-8")
