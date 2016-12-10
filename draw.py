import sys
from PIL import Image, ImageDraw

im = Image.open("sample_data/1.jpg")

draw = ImageDraw.Draw(im)
draw.line((0, 0) + im.size, fill=128)
draw.line((0, im.size[1], im.size[0], 0), fill=128)
del draw


im.show()
# write to stdout
# im.save(sys.stdout, "PNG")