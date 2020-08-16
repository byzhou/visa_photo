from PIL import Image
import face_recognition, sys

def detect_face(filename):
	image = face_recognition.load_image_file(filename)
	face_locations = face_recognition.face_locations(image)

	return face_locations[0]

def mm_to_pixel(a):
	return a * 602.0 / (2 * 25.4)

def pixel_to_mm(a, ratio=1.0 / 602 * (2 * 25.4)):
	return float(a) * ratio 

def dimension_from_pixel(crop_box):
	left, down, right, top = crop_box
	print (left, \
		   down, \
		   right, \
		   top \
			)
def verify_location(filename):
    photo_size = (48, 33)
    im = Image.open(filename)
    
    left, top, right, down = detect_face(filename)
    ratio = 1.0 / im.size[1] * 48
    print "pixel size", ratio
    print "face location", \
            pixel_to_mm(left, ratio=ratio),\
            pixel_to_mm(down, ratio=ratio),\
            pixel_to_mm(right, ratio=ratio),\
            pixel_to_mm(top, ratio=ratio)

    print "height width", pixel_to_mm(right - left, ratio=ratio), pixel_to_mm(top - down, ratio=ratio)

    im.close()


def convert_file(filename, im_size):
	inch_to_mm = 25.4
	output_size = (48, 33)
	head_width = (15, 22)
	head_length = (29, 33)

	original_height = mm_to_pixel(im_size[0] * inch_to_mm)
	original_width = mm_to_pixel(im_size[1] * inch_to_mm)
	
	im = Image.open(filename)
   
	alpha = 1.05
	beta = alpha
	width_crop_ratio = 0.5
	height_crop_ratio = 0.3
	total_crop_width  = mm_to_pixel(im_size[1] * inch_to_mm - output_size[1] * beta)
	total_crop_height = mm_to_pixel(im_size[0] * inch_to_mm - output_size[0] * alpha)

	print "total_crop_sizes:", 
	print (total_crop_height, total_crop_width)

	crop_box = (total_crop_width * width_crop_ratio,\
				total_crop_height * height_crop_ratio,\
				original_width - total_crop_width * (1 - width_crop_ratio),\
				original_height - total_crop_height * (1 - height_crop_ratio)\
				)

	print "Location to crop:",
	dimension_from_pixel(crop_box)

	output_photo = im.crop(crop_box)
	output_photo.show()

	output_name = "output.jpg"
	output_photo.save(output_name)

	left, top, right, down = detect_face(output_name)

	width_ratio = 1.0 / (original_width - total_crop_width) * output_size[1]
	height_ratio = 1.0 / (original_height - total_crop_height) * output_size[0]
	print "pixel size:", width_ratio, height_ratio
	print "face width (15, 22):", pixel_to_mm(right - left, ratio=width_ratio)
	print "face height (29, 33):", pixel_to_mm(top - down, ratio=height_ratio)
	print "aspect ratio:", (original_height - total_crop_height) / (original_width - total_crop_width), 48.0/33

	output_photo.close()
	im.close()

def make_wallet(filename, output_name):
	output_size = (48, 33)
	inch_to_mm = 25.4

	im = Image.open(filename)
	print "imported pixels:", im.size[0], im.size[1]
	pixel_size = 1.0 / im.size[1] * output_size[0]
	print "pixel size:", pixel_size

	num_width_pixel  = int(6.0 * inch_to_mm / pixel_size)
	num_height_pixel = int(4.0 * inch_to_mm / pixel_size)
	print "num of pixels on canvas:", num_width_pixel, num_height_pixel

	output = Image.new("RGB", (num_width_pixel, num_height_pixel), "white")
	margin = 40
	for i in range(num_width_pixel/im.size[0]):
		for j in range(num_height_pixel/im.size[1]):
			output.paste(im, (i * (im.size[0] + margin),\
							  j * (im.size[1] + margin), \
							  i * (im.size[0] + margin) + im.size[0], \
							  j * (im.size[1] + margin) + im.size[1]\
							  ))
	# output.show()
	# im.close()
	# output_name = "output_wallet.jpg"
	output.save(output_name)
	im.close()
	output.close()

if __name__ == "__main__":
	# convert_file('visa_photo.jpg', (2,2))
	make_wallet(sys.argv[1], sys.argv[2])
    # verify_location("output.jpg")
