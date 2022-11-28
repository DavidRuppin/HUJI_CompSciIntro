from image_editor import *


def test_separate_channels() -> None:
    image = [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
    image_lst = [[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                 [[2, 2, 2], [2, 2, 2], [2, 2, 2], [2, 2, 2]],
                 [[3, 3, 3], [3, 3, 3], [3, 3, 3], [3, 3, 3]]]

    assert separate_channels(image) == image_lst

    image = [[[1, 2, 3], [1, 2, 3], [1, 2, 3], [2, 3, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3], [3, 3, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3], [2, 3, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3], [2, 3, 4]]]
    image_lst = [[[1, 1, 1, 2], [1, 1, 1, 3], [1, 1, 1, 2], [1, 1, 1, 2]],
                 [[2, 2, 2, 3], [2, 2, 2, 3], [2, 2, 2, 3], [2, 2, 2, 3]],
                 [[3, 3, 3, 3], [3, 3, 3, 3], [3, 3, 3, 3], [3, 3, 3, 4]]]

    assert separate_channels(image) == image_lst


def test_combine() -> None:
    image = [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
    image_lst = [[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                 [[2, 2, 2], [2, 2, 2], [2, 2, 2], [2, 2, 2]],
                 [[3, 3, 3], [3, 3, 3], [3, 3, 3], [3, 3, 3]]]

    assert combine_channels(image_lst) == image

    image = [[[1, 2, 3], [1, 2, 3], [1, 2, 3], [2, 3, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3], [3, 3, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3], [2, 3, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3], [2, 3, 4]]]
    image_lst = [[[1, 1, 1, 2], [1, 1, 1, 3], [1, 1, 1, 2], [1, 1, 1, 2]],
                 [[2, 2, 2, 3], [2, 2, 2, 3], [2, 2, 2, 3], [2, 2, 2, 3]],
                 [[3, 3, 3, 3], [3, 3, 3, 3], [3, 3, 3, 3], [3, 3, 3, 4]]]

    assert combine_channels(image_lst) == image

    image = [[[1, 58, 3], [1, 2, 3], [1, 2, 3], [2, 3, 3], [1, 2, 3], [100, 32, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3], [3, 3, 3], [34, 2, 3], [100, 32, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 77, 3], [
                 2, 3, 3], [1, 15, 3], [100, 32, 3]],
             [[1, 24, 3], [1, 2, 3], [1, 2, 3], [2, 3, 4], [1, 66, 3], [100, 32, 3]]]

    assert image == combine_channels(separate_channels(image))


def test_RGB2grayscale() -> None:
    image_lst = [[[100, 180, 240]]]
    image = [[163]]
    assert RGB2grayscale(image_lst) == image

    image_lst = [[[200, 0, 14], [15, 6, 50]]]
    image = [[61, 14]]
    assert RGB2grayscale(image_lst) == image

    image_lst = [[[200, 0, 14], [15, 6, 50]], [[200, 0, 14], [15, 6, 50]]]
    image = [[61, 14], [61, 14]]
    assert RGB2grayscale(image_lst) == image

    image_lst = [[[200, 0, 14], [100, 180, 240], [15, 6, 50]],
                 [[100, 180, 240], [200, 0, 14], [15, 6, 50]]]
    image = [[61, 163, 14], [163, 61, 14]]
    assert RGB2grayscale(image_lst) == image


def test_blur_kernel() -> None:
    assert blur_kernel(3) == [[1/9, 1/9, 1/9],
                              [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]
    assert blur_kernel(4) == [[1/16, 1/16, 1/16, 1/16],
                              [1/16, 1/16, 1/16, 1/16], [1/16, 1/16, 1/16, 1/16], [1/16, 1/16, 1/16, 1/16]]
    assert blur_kernel(1) == [[1]]


def test_apply_kernel() -> None:
    image = [[0, 128, 255]]
    kernel = blur_kernel(3)
    blur = [[14, 128, 241]]
    assert apply_kernel(image, kernel) == blur

    image = [[10, 20, 30, 40, 50],
             [8, 16, 24, 32, 40],
             [6, 12, 18, 24, 30],
             [4, 8, 12, 16, 20]]
    kernel = blur_kernel(5)
    blur = [[12, 20, 26, 34, 44],
            [11, 17, 22, 27, 34],
            [10, 16, 20, 24, 29],
            [7, 11, 16, 18, 21]]
    assert apply_kernel(image, kernel) == blur


def test_bilinear_interpolation() -> None:
    assert bilinear_interpolation([[0, 64], [128, 255]], 0, 0) == 0
    assert bilinear_interpolation([[0, 64], [128, 255]], 0, 0) == 0
    assert bilinear_interpolation([[0, 64], [128, 255]], 1, 1) == 255
    assert bilinear_interpolation([[0, 64], [128, 255]], 0.5, 0.5) == 112
    assert bilinear_interpolation([[0, 64], [128, 255]], 0.5, 1) == 160
    assert bilinear_interpolation([[15, 30, 45, 60, 75], [90, 105, 120, 135, 150], [
                                  165, 180, 195, 210, 225]], 4/5, 8/3) == 115


def test_resize() -> None:
    assert resize([[0, 50], [100, 200]], 3, 4) == [
        [0, 17, 33, 50], [50, 75, 100, 125], [100, 133, 167, 200]]


def test_rotate_90() -> None:
    image: Image = [[1, 2, 3], [4, 5, 6]]
    dir = 'R'
    result = [[4, 1],
              [5, 2],
              [6, 3]]
    assert rotate_90(image, dir) == result
    image = [[1, 2, 3], [4, 5, 6]]
    dir = 'L'
    result = [[3, 6],
              [2, 5],
              [1, 4]]
    assert rotate_90(image, dir) == result
    image = [[[1, 2, 3], [4, 5, 6]],
             [[0, 5, 9], [255, 200, 7]]]
    dir = 'L'
    result = [[[4, 5, 6], [255, 200, 7]],
              [[1, 2, 3], [0, 5, 9]]]
    assert rotate_90(image, dir) == result
    image = [[0], [1], [2], [3]]
    result = [[3, 2, 1, 0]]
    assert rotate_90(image, 'R') == result
    image = [[3, 2, 1, 0]]
    result = [[3], [2], [1], [0]]
    assert rotate_90(image, 'R') == result
    image = [[[1, 58, 3], [1, 2, 3], [1, 2, 3], [2, 3, 3], [1, 2, 3], [100, 32, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 2, 3], [3, 3, 3], [34, 2, 3], [100, 32, 3]],
             [[1, 2, 3], [1, 2, 3], [1, 77, 3], [
                 2, 3, 3], [1, 15, 3], [100, 32, 3]],
             [[1, 24, 3], [1, 2, 3], [1, 2, 3], [2, 3, 4], [1, 66, 3], [100, 32, 3]]]
    assert rotate_90(
        rotate_90(rotate_90(rotate_90(image, 'R'), 'R'), 'R'), 'R') == image
    assert rotate_90(rotate_90(image, 'R'), 'R') == rotate_90(
        rotate_90(image, 'L'), 'L')


def test_get_edges() -> None:
    assert get_edges([[200, 50, 200]], 3, 3, 10) == [[255, 0, 255]]


def test_quantize() -> None:
    assert quantize([[0, 50, 100], [150, 200, 250]], 8) == [
        [0, 36, 109], [146, 219, 255]]
