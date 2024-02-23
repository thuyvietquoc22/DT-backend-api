from PIL import Image, ImageOps
import os


def resize_image(original_image, output_image_path, max_size):
    width, height = original_image.size

    if width > height:
        ratio = max_size / width
    else:
        ratio = max_size / height

    new_width = int(width * ratio)
    new_height = int(height * ratio)

    resized_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)

    resized_image.save(output_image_path)


def compress_image(image, output_image_path, max_file_size):
    image = ImageOps.exif_transpose(image)
    resize_image(image, output_image_path, 1080)

    file_size = os.path.getsize(output_image_path)
    file_stats = os.stat(output_image_path)
    if file_stats.st_size/(1024*1024) > max_file_size:
        quality = int(90 * max_file_size * 1024 / file_size)

        resized_image = Image.open(output_image_path)
        resized_image.save(output_image_path, optimize=True, quality=quality)
