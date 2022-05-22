import base64
from math import sqrt
import re

import cv2
import numpy as np
import pytesseract


class ConfigError(Exception):
    pass

class NotCoupon(Exception):
    pass


def rgb(x):
    """Convert #[AA]RRGGBB color in integer or string to (r,g,b) tuple
    
    Alpha (AA) component is simply ignored.
    
    rgb(0xff0000ff)
    >>> (0, 0, 255)
    rgb('#ff0000')
    >>> (255, 0, 0)
    """
    
    if isinstance(x, str) and x[0] == '#':
        x = int(x[1:], 16)
    return ((x >> 16) & 0xff, (x >> 8) & 0xff, (x) & 0xff)


def cie94(L1_a1_b1, L2_a2_b2):
    """Calculate color difference by using CIE94 formulae
    
    See http://en.wikipedia.org/wiki/Color_difference or
    http://www.brucelindbloom.com/index.html?Eqn_DeltaE_CIE94.html.
    
    cie94(rgb2lab((255, 255, 255)), rgb2lab((0, 0, 0)))
    >>> 58.0
    cie94(rgb2lab(rgb(0xff0000)), rgb2lab(rgb('#ff0000')))
    >>> 0.0
    """
    
    L1, a1, b1 = L1_a1_b1
    L2, a2, b2 = L2_a2_b2
    
    C1 = sqrt(a1 ** 2 + b1 ** 2)
    C2 = sqrt(a2 ** 2 + b2 ** 2)
    delta_L = L1 - L2
    delta_C = C1 - C2
    delta_a = a1 - a2
    delta_b = b1 - b2
    delta_H_square = delta_a ** 2 + delta_b ** 2 - delta_C ** 2
    return (sqrt(delta_L ** 2 
                 + delta_C ** 2 / (1.0 + 0.045 * C1) ** 2
                 + delta_H_square / (1.0 + 0.015 * C1) ** 2
                ))


def rgb2lab(R_G_B):
    """Convert RGB colorspace to Lab
    
    Adapted from http://www.easyrgb.com/index.php?X=MATH.
    """
    
    R, G, B = R_G_B
    
    # Convert RGB to XYZ
    
    var_R = ( R / 255.0 )        # R from 0 to 255
    var_G = ( G / 255.0 )        # G from 0 to 255
    var_B = ( B / 255.0 )        # B from 0 to 255

    if ( var_R > 0.04045 ): var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
    else:                   var_R = var_R / 12.92
    if ( var_G > 0.04045 ): var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
    else:                   var_G = var_G / 12.92
    if ( var_B > 0.04045 ): var_B = ( ( var_B + 0.055 ) / 1.055 ) ** 2.4
    else:                   var_B = var_B / 12.92

    var_R = var_R * 100.0
    var_G = var_G * 100.0
    var_B = var_B * 100.0

    # Observer. = 2°, Illuminant = D65
    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505
    
    # Convert XYZ to L*a*b*
    
    var_X = X / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
    var_Y = Y / 100.000        # ref_Y = 100.000
    var_Z = Z / 108.883        # ref_Z = 108.883

    if ( var_X > 0.008856 ): var_X = var_X ** ( 1.0/3.0 )
    else:                    var_X = ( 7.787 * var_X ) + ( 16.0 / 116.0 )
    if ( var_Y > 0.008856 ): var_Y = var_Y ** ( 1.0/3.0 )
    else:                    var_Y = ( 7.787 * var_Y ) + ( 16.0 / 116.0 )
    if ( var_Z > 0.008856 ): var_Z = var_Z ** ( 1.0/3.0 )
    else:                    var_Z = ( 7.787 * var_Z ) + ( 16.0 / 116.0 )

    CIE_L = ( 116.0 * var_Y ) - 16.0
    CIE_a = 500.0 * ( var_X - var_Y )
    CIE_b = 200.0 * ( var_Y - var_Z )
    return (CIE_L, CIE_a, CIE_b)


def modify_coords(x, y, height, width):
    return x * width // 500, y * height // 500


def check_markers(image, markers):
    if not markers:
        return [1000]
    result = []
    height, width, _ = image.shape
    for x, y, color in markers:
        x, y = modify_coords(x, y, height, width)
        expected = rgb2lab(rgb(color))
        now = rgb2lab(image[y, x])
        result.append(cie94(expected, now))
    return sorted(result, reverse=True)


def crop_rect(img, coords):
    cnt = np.array([[point] for point in coords])
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    # cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
    width = int(rect[1][0])
    height = int(rect[1][1])
    
    if rect[2] > 45:
        width, height = height, width
        box = np.roll(box, 1, axis=0)
    
    src_pts = box.astype("float32")
    # coordinate of the points in box points after the rectangle has been
    # straightened
    dst_pts = np.array([[0, height-1],
                        [0, 0],
                        [width-1, 0],
                        [width-1, height-1]], dtype="float32")
    
    # the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # directly warp the rotated rectangle to get the straightened rectangle
    warped = cv2.warpPerspective(img, M, (width, height))
    return warped


def img2html(image):
    b64img = base64.b64encode(cv2.imencode('.png', image)[1].tobytes()).decode('utf-8')
    return f'<img width="300px" src="data:image/png;base64, {b64img}"/>'


def ocr_locations(image, locations, config_id):
    height, width, _ = image.shape
    result = []
    for label in locations:
        if len(locations[label]) == 0:
            result.append((label, ''))
            continue
        crop = crop_rect(image, [modify_coords(x, y, height, width) for x, y in locations[label]])
        text = re.findall('\d+', pytesseract.image_to_string(crop, lang='eng').strip())
        text = text[0] if len(text) != 0 else None
        result.append((label, text))
    result.append(('config_id', config_id))
    for field in result:
        if field[1] is not None and field[0] != 'config_id':
            return result
    raise NotCoupon


def process_image(image, templates, threshold=5):
    scores = [check_markers(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), template.get('markers')) for template in templates]
    template_id = min(range(len(scores)), key=scores.__getitem__)
    if scores[template_id][0] > threshold:
        raise ConfigError('threshold')
    template = templates[template_id]
    return ocr_locations(image, template.get('locations'), config_id=template.get('id'))
