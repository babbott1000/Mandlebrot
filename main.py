from PIL import Image
import pathlib
from time import gmtime, strftime
from colour import Color

iterations = 150
size = (320*40, 256*40)
domain = ((-2.0, 0.5), (-1, 1))

img = Image.new('RGB', size, color='white')
pixels = img.load()


color_size = [25, 80, 30]

color_size_sum = 0
for c in color_size:
	color_size_sum += c
for i, c in enumerate(color_size):
	color_size[i] = int(c * iterations / color_size_sum)

color_map = list(Color("black").range_to(Color("yellow"), color_size[0])) + list(Color("yellow").range_to(Color("pink"), color_size[1])) + list(Color("pink").range_to(Color("darkblue"), color_size[2]))

def divergence(num):
	z = 0.0j
	for i in range(iterations):
		z = z*z + num
		if(z.real*z.real+z.imag*z.imag >= 4):
			return i
	return iterations

def map_colors(num):	
	if(num > len(color_map) - 1):
		num = len(color_map) - 1
	num = (len(color_map) - 1) - num
	c = color_map[num]
	return (int(c.red*255), int(c.green*255), int(c.blue*255))

for i in range(img.size[0]):
	for j in range(img.size[1]):
		num = complex(((i+1)/img.size[0])*(domain[0][1]-domain[0][0])+domain[0][0], ((j+1)/img.size[1])*(domain[1][1]-domain[1][0])+domain[1][0])
		d = divergence(num)
		pixels[i, j] = map_colors(d)
		
print(str(pathlib.Path(__file__).parent.absolute()))
img.save(str(pathlib.Path(__file__).parent.absolute() / "mandlebrot-") + strftime("%Y-%m-%d@%H.%M.%S", gmtime()) + ".png", "PNG")
img.show()
