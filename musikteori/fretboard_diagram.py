from itertools import product
import math
from typing import Iterable, Tuple
from fractions import Fraction

import contextlib
import cv2
import numpy


class FrequencyRatio:
    cents_per_octave = 1200
    semitones_per_octave = 12
    holdrian_commas_per_octave = 53

    @staticmethod
    def equal_temperament(step: float, steps_per_octave: float):
        return 2 ** (step / steps_per_octave)

    @staticmethod
    def just_intonation(primes: Iterable[int], exponent_combination: Iterable[int]):
        subset_ratio = 1.0
        for prime, exponent in zip(primes, exponent_combination):
            subset_ratio *= prime**exponent
        return subset_ratio

    @staticmethod
    def just_intonations(primes: Iterable[int], prime_ranges: Iterable[Tuple[int, int]]):
        exponent_ranges = [range(min_exp, max_exp + 1) for min_exp, max_exp in prime_ranges]
        for exponent_combination in product(*exponent_ranges):
            subset_ratio = FrequencyRatio.just_intonation(primes, exponent_combination)
            if 1 <= subset_ratio <= 2:
                yield subset_ratio, exponent_combination

    @staticmethod
    def just_intonations(primes: Iterable[int], prime_ranges: Iterable[Tuple[int, int]], restrictions):
        exponent_ranges = [range(min_exp, max_exp + 1) for min_exp, max_exp in prime_ranges]
        for exponent_combination in product(*exponent_ranges):
            subset_ratio = FrequencyRatio.just_intonation(primes, exponent_combination)
            if 1 <= subset_ratio <= 2 and subset_ratio in restrictions:
                yield subset_ratio, exponent_combination

    @staticmethod
    def float_to_ratio(frequency_ratio):
        ratio = Fraction(frequency_ratio).limit_denominator()
        return ratio.numerator, ratio.denominator

    pythagorean_ratios = [
        1024 / 729,
        256 / 243,
        128 / 81,
        32 / 27,
        16 / 9,
        4 / 3,
        1 / 1,
        3 / 2,
        9 / 8,
        27 / 16,
        81 / 64,
        243 / 128,
        729 / 512,
    ]

    classical_intonation_ratios = [
        1 / 1,
        16 / 15,
        10 / 9,
        9 / 8,
        6 / 5,
        5 / 4,
        4 / 3,
        45 / 32,
        25 / 18,
        64 / 45,
        36 / 25,
        3 / 2,
        8 / 5,
        5 / 3,
        9 / 5,
        16 / 9,
        15 / 8,
        2 / 1,
    ]


@contextlib.contextmanager
def window(name):
    resource = cv2.namedWindow(name, cv2.WINDOW_GUI_EXPANDED)
    try:
        yield resource
    finally:
        cv2.destroyWindow(name)


def add_text_with_centroid(image, text, centroid, font_height_px, direction=1):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    thickness_px = 1
    text_color = (0, 0, 0)
    line_type = cv2.LINE_AA

    font_scale = cv2.getFontScaleFromHeight(fontFace=font_face, pixelHeight=font_height_px, thickness=thickness_px)
    text_size, _ = cv2.getTextSize(text, font_face, font_scale, thickness_px)

    # Calculate text position based on centroid coordinates
    text_x = centroid[0] - text_size[0] // 2
    text_y = centroid[1] + text_size[1] // 2

    bounding_box = (text_x, text_y, text_size[0], text_size[1])
    while has_text(image, bounding_box):
        # Adjust the text position further away
        text_x = text_x + direction * text_size[0]
        bounding_box = (text_x, text_y, text_size[0], text_size[1])

    # Draw text on the image
    cv2.putText(image, text, (text_x, text_y), font_face, font_scale, text_color, thickness_px, line_type)

    return image


def has_text(image, bounding_box):
    x, y, width, height = bounding_box
    region = image[y : y + height, x : x + width]
    has_pixels = numpy.any(region < 255)
    return has_pixels


def draw_just_ratio(image, frequency_ratio, primes, exponent_combination, color):
    semitones = 12 * math.log2(frequency_ratio)
    wavelength_ratio = 1.0 / frequency_ratio
    height, width, _ = image.shape
    string = 0.9 * height
    nut = height - string
    center_x = int(width * 0.5)
    center_y = int(nut + string * 1.8 * (1.0 - wavelength_ratio))
    radius = 10
    cv2.circle(image, (center_x, center_y), radius, color, 1)

    add_text_with_centroid(image, f"{semitones:.2f}T", (center_x, center_y), 18, 1)
    add_text_with_centroid(
        image,
        f"{ [str(prime) + '(' + str(exponent) + ')' for prime, exponent in zip(primes, exponent_combination)  ] }",
        (center_x, center_y),
        18,
        -1,
    )


def draw_ratio(image, frequency_ratio, color):
    wavelength_ratio = 1.0 / frequency_ratio
    height, width, _ = image.shape
    string = 0.9 * height
    nut = height - string
    center_y = int(nut + string * 1.8 * (1.0 - wavelength_ratio))
    cv2.line(image, (0, center_y), (width, center_y), color, 2)


def pitches():
    primes = [2, 3, 5]
    prime_ranges = [(-10, 10), (-10, 10), (-10, 10)]

    image_width, image_height = 1920, 1080
    image = numpy.full((image_height, image_width, 3), 255, numpy.uint8)

    for ratio, exponent_combination in FrequencyRatio.just_intonations(
        primes, prime_ranges, FrequencyRatio.pythagorean_ratios
    ):
        draw_just_ratio(image, ratio, primes, exponent_combination, (0, 255, 0))
    for ratio, exponent_combination in FrequencyRatio.just_intonations(
        primes, prime_ranges, FrequencyRatio.classical_intonation_ratios
    ):
        draw_just_ratio(image, ratio, primes, exponent_combination, (0, 0, 255))
    for step in range(0, 54):
        ratio = FrequencyRatio.equal_temperament(float(step), 53.0)
        draw_ratio(image, ratio, (255, 0, 0))

    return image


def main():
    with contextlib.ExitStack() as stack:
        stack.enter_context(window("image"))
        cv2.imshow("image", pitches())
        cv2.waitKey(0)


if __name__ == "__main__":
    main()
