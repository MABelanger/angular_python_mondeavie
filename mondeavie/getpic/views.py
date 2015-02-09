from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
import os
from mondeavie import settings
from PIL import Image
import os.path


def get_resize_path(path, width):
	dir_lst = path.split(os.sep)
	dir_lst.insert(-1, 'resize')
	resize_dir = os.sep.join(dir_lst[:-1])
	if not os.path.exists(resize_dir):
		os.makedirs(resize_dir)

	path_resize =  os.sep.join(dir_lst)
	file_name, file_ext = os.path.splitext(path_resize)
	return file_name + '_' + width + file_ext


def save_resize_image(image_path, resize_path, width):
	image = Image.open(image_path)
	w, h = image.size
	prop = w / float(width)
	image = image.resize((int(width), int(h/prop)), Image.ANTIALIAS)
	# Save the image
	image.save(resize_path, 'JPEG', quality=90)
	resize_image = open(resize_path)
	return resize_image


def get_resize_image(request, path_relative, width, extention):

	if int(width) > 1024 : 
		return HttpResponseBadRequest('size to big')

	image_path = os.path.join(settings.MEDIA_ROOT, path_relative + extention)
	resize_path = get_resize_path(image_path, width)

	# if the file exist, return the file
	if os.path.isfile(resize_path) :
		resize_image = open(resize_path)
		return HttpResponse(resize_image, content_type="image/jpg")

	# if the file do not exist, resize and save it and return the saved image
	if os.path.isfile(image_path) :
		resize_image = save_resize_image(image_path, resize_path, width)
		return HttpResponse(resize_image, content_type="image/jpg")

	return HttpResponseBadRequest('image not found')
