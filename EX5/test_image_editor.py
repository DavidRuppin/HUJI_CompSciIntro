from image_editor import *


# noinspection DuplicatedCode
def test_separate_channels():
    assert separate_channels([[[1, 2]]]) == [[[1]], [[2]]]

    image = [
        [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
        [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
        [[1, 2, 3], [1, 2, 3], [4, 2, 3]]
    ]
    image_lst = [
        [[1, 1, 1], [1, 1, 1], [1, 1, 4]],
        [[2, 2, 2], [2, 2, 2], [2, 2, 2]],
        [[3, 3, 3], [3, 3, 3], [3, 3, 3]]
    ]

    assert separate_channels(image) == image_lst


# noinspection DuplicatedCode
def test_combine_channels():
    assert combine_channels([[[1]], [[2]]]) == [[[1, 2]]]

    image = [
        [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
        [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
        [[1, 2, 3], [1, 2, 3], [4, 2, 3]]
    ]
    image_lst = [
        [[1, 1, 1], [1, 1, 1], [1, 1, 4]],
        [[2, 2, 2], [2, 2, 2], [2, 2, 2]],
        [[3, 3, 3], [3, 3, 3], [3, 3, 3]]
    ]

    assert combine_channels(image_lst) == image


def test_rgb_to_grayscale():
    assert RGB2grayscale([[[100, 180, 240]]]) == [[163]]


def test_blur_kernel():
    assert blur_kernel(3) == [[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9]]


def test_apply_blur_kernel():
    assert apply_kernel([[0, 128, 255]], blur_kernel(3)) == [[14, 128, 241]]
    original = [[10, 20, 30, 40, 50],
                [8, 16, 24, 32, 40],
                [6, 12, 18, 24, 30],
                [4, 8, 12, 16, 20]]

    blurred = [[12, 20, 26, 34, 44],
               [11, 17, 22, 27, 34],
               [10, 16, 20, 24, 29],
               [7, 11, 16, 18, 21]]

    assert apply_kernel(original, blur_kernel(5)) == blurred


def test_bilinear_interpolation():
    assert bilinear_interpolation([[0, 64], [128, 255]], 0, 0) == 0
    assert bilinear_interpolation([[0, 64], [128, 255]], 1, 1) == 255
    assert bilinear_interpolation([[0, 64], [128, 255]], 0.5, 0.5) == 112
    assert bilinear_interpolation([[0, 64],
                                   [128, 255]], 0.5, 1) == 160
    assert bilinear_interpolation([[15, 30, 45, 60, 75], [90, 105, 120, 135, 150], [165, 180, 195, 210, 225]], 4 / 5,
                                  8 / 3) == 115


def test_resize():
    assert resize([255], 2, 2) == [[255, 255], [255, 255]]
