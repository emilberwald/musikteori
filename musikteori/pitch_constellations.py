import contextlib
import itertools
from typing import Iterable, Tuple

import cv2
import numpy
import scipy.optimize
import pint

I = pint.UnitRegistry()
I.define("semitone = 360 * degree / 12")
I.define("quadrant = 360 * degree / 4")


@contextlib.contextmanager
def window(name):
    resource = cv2.namedWindow(name)
    try:
        yield resource
    finally:
        cv2.destroyWindow(name)


notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "G", "G#"]

# semitone steps
MAJOR = [2, 2, 1, 2, 2, 2, 1]
NATURAL_MINOR = MAJOR[-2:] + MAJOR[:-2]
HARMONIC_MINOR = NATURAL_MINOR[:-2] + [i + d for i, d in zip(NATURAL_MINOR[-2:], [1, -1])]
ASCENDING_MELODIC_MINOR = NATURAL_MINOR[:-3] + [i + d for i, d in zip(NATURAL_MINOR[-3:], [1, -1, 0])]

SCALES = {
    "major": MAJOR,
    "natural minor": NATURAL_MINOR,
    "harmonic minor": HARMONIC_MINOR,
    "ascending melodic minor": ASCENDING_MELODIC_MINOR,
}


def asarray(*args, dtype=float):
    return numpy.fromiter(args, dtype=dtype)


def pitch_constellation(*semitone_steps, size=(320, 320), offset: pint.Quantity = 1 * I.semitone):
    def from_clockwise(angle: pint.Quantity):
        return (90 * I.degrees - angle.to(I.degrees)).to(I.radians)

    def to_image(img: numpy.ndarray, x: numpy.ndarray):
        width, height = img.shape[1::-1]
        # (0,0) => (0,height)
        return tuple((numpy.fromiter((0, height), float) + numpy.fromiter((x[0], -x[1]), float)).astype(int))

    def gen_lines(*, semitones: Iterable[float], center: numpy.ndarray, radius: float, offset: pint.Quantity):
        for semitone in semitones:
            angle = from_clockwise(semitone * I.semitone + offset)
            yield (center, center + radius * numpy.fromiter((numpy.cos(angle), numpy.sin(angle)), float))

    def gen_hours(*, center: numpy.ndarray, radius: float, offset: pint.Quantity):
        for semitone in range(0, 12):
            angle = from_clockwise(semitone * I.semitone + offset)
            yield (
                center + 0.8 * radius * asarray(numpy.cos(angle), numpy.sin(angle)),
                center + radius * asarray(numpy.cos(angle), numpy.sin(angle)),
            )

    img = numpy.zeros((*size, 3), dtype="uint8")
    img[:] = (255, 255, 255)
    center = numpy.fromiter((s // 2 for s in size), float)
    radius = float(min(size) // 2) * 0.8
    cv2.circle(img=img, center=tuple(numpy.fromiter(center, int)), radius=int(radius), color=(0, 0, 0))
    for (start, end) in gen_lines(
        semitones=(semitone % 12 for semitone in itertools.chain((0,), numpy.cumsum(semitone_steps))),
        center=center,
        radius=radius,
        offset=offset,
    ):
        img_start = to_image(img, start)
        img_end = to_image(img, end)
        cv2.line(img, img_start, img_end, (0, 0, 255))

    def puttext(*, img, text, position, height, angle):
        def cost(font_scale, height, text, font_face, thickness):
            textSize, _ = cv2.getTextSize(text, fontFace=font_face, fontScale=font_scale, thickness=thickness)
            error = textSize[-1] - height
            return error

        font_face = cv2.FONT_HERSHEY_COMPLEX
        thickness = 1
        font_scale = scipy.optimize.bisect(
            cost, 0.0, float(max(img.shape[1::-1])), (height, text, font_face, thickness)
        )

        (width, height), baseline = cv2.getTextSize(text, fontFace=font_face, fontScale=font_scale, thickness=thickness)

        normalized_angle = angle.to(I.quadrant) % (4 * I.quadrant)
        if 0 * I.quadrant <= normalized_angle < 1 * I.quadrant:
            fixed_position = (position[0], position[1])
        elif 1 * I.quadrant <= normalized_angle < 2 * I.quadrant:
            fixed_position = (position[0] - width, position[1])
        elif 2 * I.quadrant <= normalized_angle < 3 * I.quadrant:
            fixed_position = (position[0] - width, position[1] - height)
        elif 3 * I.quadrant <= normalized_angle:
            fixed_position = (position[0], position[1] - height)

        if 2.5 * I.semitone <= normalized_angle <= 3.5 * I.semitone:
            fixed_position = (position[0] - width / 2, position[1])
        if 8.5 * I.semitone <= normalized_angle <= 9.5 * I.semitone:
            fixed_position = (position[0] - width / 2, position[1] - height)

        img_position = to_image(img, fixed_position)

        cv2.putText(
            img=img,
            text=text,
            org=img_position,
            fontFace=font_face,
            fontScale=font_scale,
            color=(0, 0, 0),
            thickness=thickness,
            lineType=cv2.LINE_AA,
        )

    for no, (start, end) in enumerate(gen_hours(center=center, radius=radius, offset=offset)):
        img_start = to_image(img, start)
        img_end = to_image(img, end)
        cv2.line(img, img_start, img_end, (0, 0, 0))
        puttext(
            img=img,
            text=str(no),
            position=end,
            height=min(10, int(radius * 0.2)),
            angle=from_clockwise(no * I.semitone + offset),
        )

    return img


def show_pitch_constellations(**constellations):
    with contextlib.ExitStack() as stack:
        for key, constellation in constellations.items():
            stack.enter_context(window(key))
            cv2.imshow(key, pitch_constellation(*constellation))
        cv2.waitKey(0)


if __name__ == "__main__":
    show_pitch_constellations(**SCALES)
