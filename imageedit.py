from PIL import Image,ImageFilter
import os

for f in os.listdir('.'):
	if f.endswith('.jpg')L
		i=Image.open(f)
		fn,ftext=os.path.splitext(f)
		i.save('pngs/{}.png'.format(fn))

image1=Image.open('abc.png')
image1.show()

#image1.save('abc.jpeg')

size_300=(300,300)
size_700=(700,700)
for f in os.listdir('.'):
	if f.endswith('.jpg')L
		i=Image.open(f)
		fn,ftext=os.path.splitext(f)
		i.thumbnail(size_300)
		
		i.save('300/{}_300{}'.format(fn,fext))



#rotate 
image1.rotate(90).save('abc.png')
image1.convert(mode='L').save('abc.png')
#default arg=2
image1.filter(ImageFilter.GaussianBlur()).save('abc.png')
image1.filter(ImageFilter.GaussianBlur(15)).save('abc.png')
