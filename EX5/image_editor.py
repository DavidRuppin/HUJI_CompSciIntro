#################################################################
# FILE : image_editor.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex5 2022-2023
#################################################################
from math import floor, ceil

##############################################################################
#                                   Imports                                  #
##############################################################################
from ex5_helper import *
from typing import Optional


##############################################################################
#                                  Functions                                 #
##############################################################################


def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    row_size = len(image)
    col_size = len(image[0])
    channel_size = len(image[0][0])

    return [[[image[row][col][channel] for row in range(row_size)] for col in range(col_size)] for channel in
            range(channel_size)]


def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    return separate_channels(channels)


# noinspection PyPep8Naming
def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    return [[pixel_to_grayscale(*pixel) for pixel in row] for row in colored_image]


def pixel_to_grayscale(r: int, g: int, b: int) -> int:
    return round(r * 0.299 + g * 0.587 + b * 0.114)


def blur_kernel(size: int) -> Kernel:
    return [[1 / pow(size, 2) for col in range(size)] for row in range(size)]


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    return [[apply_kernel_for_coordinate(image, kernel, row, col) for col in range(len(image[0]))] for row in
            range(len(image))]


# HELPER FUNCTIONS FOR apply_kernel #
def apply_kernel_for_coordinate(image, kernel, row: int, col: int) -> int:
    blurred_sum = 0
    kernel_height = len(kernel)
    kernel_width = len(kernel[0])

    # Iterating over the kernel and summing the product with the appropriate coordinates in @image
    for kernel_row in range(kernel_height):
        for kernel_col in range(kernel_width):
            x, y = row - kernel_height // 2 + kernel_row, col - kernel_width // 2 + kernel_col
            blurred_sum += get_single_channel_pixel_bound_safe(image, x, y, image[row][col]) * kernel[kernel_row][
                kernel_col]

    # If the sum is somehow bigger than 255 or smaller than 0 return 255 or 0 appropriately
    return round(blurred_sum) if 255 > blurred_sum > 0 else 0 if blurred_sum <= 0 else 255


def get_single_channel_pixel_bound_safe(image, row: int, col: int, original_channel) -> int:
    # Returns the channel at image[row][col] if it's within bounds, else the original channel
    return image[row][col] if len(image) > row >= 0 and len(image[0]) > col >= 0 else original_channel


# END OF APPLY KERNEL #


# BILINEAR INTERPOLATION HELPER FUNCTIONS #

def get_weighted_pixels(a, b, c, d, x, y):
    return [a * (1 - x) * (1 - y), b * y * (1 - x), c * x * (1 - y), d * x * y]


def get_delta_x_y(x, y) -> tuple:
    # Returns the ∆x, ∆y
    return x - floor(x), y - floor(y)


# END OF BILINEAR INTERPOLATION HELPER FUNCTIONS #

def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    # Applies the bilinear interpolation formula on the appropriate pixels
    a = image[floor(y)][floor(x)]
    b = image[ceil(y)][floor(x)]
    c = image[floor(y)][ceil(x)]
    d = image[ceil(y)][ceil(x)]
    return round(sum(get_weighted_pixels(a, b, c, d, *get_delta_x_y(x, y))))


# RESIZE HELPER FUNCTIONS #
def init_resized_image(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    new_image = [[0 for j in range(new_width)] for i in range(new_height)]
    # Iterating over the corners
    for corner in [(0, 0), (0, -1), (-1, 0), (-1, -1)]:
        new_image[corner[0]][corner[1]] = image[corner[0]][corner[1]]

    return new_image

# END OF RESIZE HELPER FUNCTIONS #


def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    new_image = init_resized_image(image, new_height, new_width)
    for row in (1, new_height - 1):
        for col in (1, new_width - 1):
            # TODO - WATCH OUT FOR POSSIBLE ZEROS HERE
            proportionate_coord = (col * (len(image[0]) - 1) / (new_height - 1),
                                   row * (len(image) - 1) / (new_height - 1))
            new_image[row][col] = bilinear_interpolation(image, *proportionate_coord)

    return new_image


def rotate_90(image: Image, direction: str) -> Image:
    ...


def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    ...


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    ...


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    ...


if __name__ == '__main__':
    ...
