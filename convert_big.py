# Hasty conversion utility for flame pendant project.  Takes a bunch of
# images (filenames received on command line) and outputs a big C array
# to use with the accompanying Arduino sketch.
# Typical invocation: python convert.py *.png > animation.h
# Inputs are assumed valid; this does NOT perform extensive checking to
# confirm all images are the same size, etc.
# Requires Python and Python Imaging Library.

# Originally part of https://github.com/wbphelps/FeatherCandle 
# Increased numBytes so it can handle large amounts of frames

from PIL import Image
import sys
import glob
import os

# --------------------------------------------------------------------------

cols     = 99 # Current column number in output (force indent on first one)
byteNum  = 0
numBytes = 0
width    = 7
height   = 15

def writeByte(n):
	global cols, byteNum, numBytes

	cols += 1                      # Increment column #
	if cols > width:                 # If max column exceeded...
		print                  # end current line
		sys.stdout.write("  ") # and start new one
		cols = 1               # Reset counter
	sys.stdout.write("{0:#0{1}X}".format(n, 4))
	byteNum += 1
	if byteNum < numBytes:
		sys.stdout.write(",")
		if cols < width:
			sys.stdout.write(" ")

# --------------------------------------------------------------------------

prior    = None
bytes    = 0
numBytes = 0xFFFFF
images   = 0

sys.stdout.write("const uint8_t PROGMEM anim[] = {")

#for name in sys.argv[1:]: # For each image passed to script...
#list = glob.glob("*.png")
list = sorted(glob.glob('*.png'), key=os.path.getmtime)
for name in list: # For each image passed to script...
	image = Image.open(name)
	image.pixels = image.load()
	x1 = width   # width - wm: truncate image
	y1 = height  # height - wm: trncate image

	if image.mode != 'L': # Not grayscale? Convert it
		image = image.convert("L")
		image.pixels = image.load()

	image = image.resize((width, height), Image.LANCZOS)  # resize to fit
	image.pixels = image.load()
	
	# Gamma correction:
#	for y in range(image.size[1]):
#		for x in range(image.size[0]):
	for y in range(y1):
		for x in range(x1):
			image.pixels[x, y] = int(pow(
			  (image.pixels[x, y] / 255.0), 2.7) * 255.0 + 0.5)

	if prior:
		# Determine bounds of changed area
#		w = image.size[0]
#		h = image.size[1]
		x1 = width   # wm: truncate image
		y1 = height  # wm: trncate image
		x2 = y2 = -1
		for y in range(height):
			for x in range(width):
				if image.pixels[x, y] != prior.pixels[x, y]:
					if x < x1: x1 = x  # expand image array
					if x > x2: x2 = x
					if y < y1: y1 = y
					if y > y2: y2 = y
	else:
		# First image = full frame
		x1 = y1 = 0
		x2 = width-1
		y2 = height-1

	if (cols>0):
		print  # start new line
		sys.stdout.write("  ") # and start new one
		cols = 0

	# Column major!
	writeByte((x1 << 4) | y1) # Top left corner
	writeByte((x2 << 4) | y2) # Bottom right corner

	images += 1
	print "  // ", name, x1, x2, y1, y2
	cols = 0
	sys.stdout.write("  ") # and start new one
	bytes += 2

	tw = width
	width = x2 - x1 + 1
	for y in range(y1, y2 + 1):
		for x in range(x1, x2 + 1):
			writeByte(image.pixels[x, y])
			bytes += 1
	width = tw

	prior = image

print  # start new line
sys.stdout.write("  ") # and start new one
cols = 0
writeByte(0xFF) # EOD marker
writeByte(0xFF) # EOD marker
writeByte(0xFF) # EOD marker
bytes += 3

print "};"
print
print "// " + str(bytes) + " bytes"
