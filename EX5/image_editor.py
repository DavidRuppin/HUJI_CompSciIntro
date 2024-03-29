#################################################################
# FILE : image_editor.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex5 2022-2023
#################################################################
import sys
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

    # For each channel, iterate over the rows.
    # In each row create a new array made from pixel[channel] for each pixel (pixel = col)
    return [[
        [image[row][col][channel] for col in range(col_size)]
        for row in range(row_size)]
        for channel in range(channel_size)]


def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    return separate_channels(separate_channels(channels))


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
    new_image = [[image[0] if type(image[0]) is int else 0 for j in range(new_width)] for i in range(new_height)]
    # Iterating over the corners if they exist
    if type(image[0]) is list:
        for corner in [(0, 0), (0, -1), (-1, 0), (-1, -1)]:
            new_image[corner[0]][corner[1]] = image[corner[0]][corner[1]]

    return new_image


# END OF RESIZE HELPER FUNCTIONS #


def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    new_image = init_resized_image(image, new_height, new_width)
    if type(image[0]) != int:
        for row in range(0, new_height):
            for col in range(0, new_width):
                # TODO - WATCH OUT FOR POSSIBLE ZEROS HERE
                proportionate_coord = row * (len(image) - 1) / (new_height - 1), \
                                      col * (len(image[0]) - 1) / (new_width - 1)
                new_image[row][col] = bilinear_interpolation(image, *proportionate_coord)

    return new_image


# ROTATE_90 HELPER FUNCTIONS #
def rotate_right(image) -> Image:
    new_matrix = []
    for col in range(len(image[0])):
        new_matrix.append([image[-row][col] for row in range(1, len(image) + 1)])

    return new_matrix


# END OF ROTATE_90 HELPER FUNCTIONS #

def rotate_90(image: Image, direction: str) -> Image:
    # If the image is a single pixel, return it
    if type(image[0]) is int:
        return image

    if direction.upper() == "L":
        for i in range(3):
            image = rotate_right(image)
    else:
        image = rotate_right(image)

    return image


# GET_EDGES HELPER FUNCTIONS #
def get_square_around_point_average(image, row, col, square_size) -> float:
    # Iterating over a @square_sized square around (row, col), returning the average from said square
    pixel_block = []
    for i in range(-(square_size // 2), (square_size // 2) + 1):
        for j in range(-(square_size // 2), (square_size // 2) + 1):
            pixel_block.append(get_single_channel_pixel_bound_safe(image, row + i, col + j, image[row][col]))

    return sum(pixel_block) / len(pixel_block)


# END OF GET_EDGES HELPER FUNCTIONS #

def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    # Creating the blurred image
    blurred_image = apply_kernel(image, blur_kernel(blur_size))

    new_image = [[0 if get_square_around_point_average(blurred_image, row, col, block_size) - c > blurred_image[row][
        col] else 255
                  for col in range(len(blurred_image[0]))] for row in range(len(blurred_image))]

    new_image = []
    for row in range(len(blurred_image)):
        row_arr = []
        for col in range(len(blurred_image[0])):
            threshold = get_square_around_point_average(blurred_image, row, col, block_size) - c
            temp = blurred_image[row][col]
            if threshold > blurred_image[row][col]:
                row_arr.append(0)
            else:
                row_arr.append(255)

        new_image.append(row_arr)

    return new_image


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    new_image = [
        [round(floor(pixel * (N / 256)) * (255 / (N - 1))) for pixel in row] for row in image
    ]

    return new_image


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    seperated = separate_channels(image)
    return combine_channels([quantize(row, N) for row in seperated])


# MAIN HELPER FUNCTIONS #
def string_is_positive_integer(suspect: str):
    if suspect.isnumeric() and int(suspect) > 0:
        return True
    return False


def string_is_odd_positive_integer(suspect: str):
    if string_is_positive_integer(suspect) and int(suspect) % 2 == 1:
        return True
    return False


def user_convert_to_grayscale(image, prompt=True):
    if type(image[0][0]) is int:
        if prompt:
            print("Grayscale already bro")
    else:
        image = RGB2grayscale(image)
    return image


def user_blur(image):
    kernel_size = input("Please choose a positive odd kernel size: ")
    if string_is_odd_positive_integer(kernel_size):
        kernel = blur_kernel(int(kernel_size))
        seperated_channels = separate_channels(image)
        image = combine_channels([apply_kernel(channel, kernel) for channel in seperated_channels])
    else:
        print("Bad input bro...")

    return image


def user_resize(image):
    user_size = input("Please enter two integers greater than 1 seperated by a comma (X,Y): ")
    width_height_list = user_size.split(",")
    if len(width_height_list) == 2 and string_is_positive_integer(width_height_list[0]) \
            and string_is_positive_integer(width_height_list[1]):
        width, height = int(width_height_list[0]), int(width_height_list[1])
        image = resize(image, width, height)
    else:
        print("Invalid values nerd")

    return image


def user_rotate(image):
    rotation = input("Which way would you like to rotate? (L/R): ")
    if rotation in ["L", "R"]:
        image = rotate_90(image, rotation)
    else:
        print("Invalid direction bro")

    return image


def user_get_edges(image):
    user_decision = input("Please choose blur size, block size and c value: ").strip()
    user_decision_split = user_decision.split(",")
    # Making sure the input is valid, all numbers are in format at that only the third variable can be a float
    if len(user_decision_split) == 3 and string_is_odd_positive_integer(user_decision_split[0]) \
            and string_is_odd_positive_integer(user_decision_split[1]) \
            and string_is_positive_integer(user_decision_split[2].replace(".", "")) \
            and user_decision_split[2].count(".") <= 1:  # Making sure we don't have a malformed float

        blur_size, block_size = int(user_decision_split[0]), int(user_decision_split[1])
        c = float(user_decision_split[2])

        image = get_edges(user_convert_to_grayscale(image, prompt=False), blur_size, block_size, c)
    else:
        print("Invalid values chum")

    return image


def user_quantize(image):
    user_N = input("Please enter the desired N: ")
    if string_is_positive_integer(user_N):
        N = int(user_N)
        if type(image[0][0]) is int:
            image = quantize(image, N)
        else:
            image = quantize_colored_image(image, N)
    else:
        print("Bad value gonk!")

    return image


# END OF MAIN HELPER FUNCTIONS #

USER_MENU_PROMPT = "~~~~~ MENU ~~~~~~\n1. convert to black and white\n2. blur\n3. resize\n4. rotate\n" \
                   "5. get edges\n6. quantize\n7. show image\n8. quit\n"


def main():
    image = load_image(sys.argv[1])

    while True:
        decision = input(USER_MENU_PROMPT).strip()
        if decision == "1":
            image = user_convert_to_grayscale(image)
        elif decision == "2":
            image = user_blur(image)
        elif decision == "3":
            image = user_resize(image)
        elif decision == "4":
            image = user_rotate(image)
        elif decision == "5":
            image = user_get_edges(image)
        elif decision == "6":
            image = user_quantize(image)
        elif decision == "7":
            show_image(image)
        elif decision == "8":
            save_path = input("Where would you like to save the image? ")
            save_image(image, save_path)
            return


if __name__ == '__main__':
    arguments = sys.argv
    # Checking that there's enough arguments§
    if len(arguments) != 2:
        print("Bad args bro <3 ")

    else:
        main()
