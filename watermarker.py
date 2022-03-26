import os
import string
from email.utils import parseaddr

from PIL import Image


def watermark(img_path: string, output_path: string, watermark_path: string = './watermark/sample.png', padding: tuple[int, int] = (200, 200), pos: string = 'BL', opacity: float = 0.6):
    assert os.path.splitext(os.path.basename(watermark_path))[
        1] == '.png', "Watermark file must be of type PNG."
    assert pos in ['TL', 'TR', 'BL', 'BR'], "Specified watermark position is invalid. Valid position values are TL, TR, BL and BR"
    base_image = Image.open(img_path)
    img_w, img_h = base_image.size

    wm_img = Image.open(watermark_path)
    wm_img.convert("RGBA")
    # wm_img.putalpha(int(255*opacity))
    wm_w, wm_h = wm_img.size

    wm_pos = ()
    if pos == 'TL':
        wm_pos = (padding[0], padding[1])
    elif pos == 'TR':
        wm_pos = (img_w - padding[0] - wm_w, padding[1])
    elif pos == 'BR':
        wm_pos = (img_w - padding[0] - wm_w, img_h - padding[1] - wm_h)
    elif pos == 'BL':
        wm_pos = (padding[0], img_h - padding[1] - wm_h)

    output_img = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))
    output_img.paste(base_image, (0, 0))
    output_img.paste(wm_img, wm_pos, mask=wm_img)
    output_img = output_img.convert('RGB')
    output_img.save(output_path)
