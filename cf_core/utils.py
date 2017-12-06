import os
import uuid
from easy_thumbnails.files import get_thumbnailer


def generate_random_str(length=10):
    """
    Return random generated string with optional length.

    :param length: int Str length
    :return:
    """
    return os.urandom(length).hex()[:length]


def uuid_replacer_handler(instance, filename, path=''):
    """
    Replace filename to uuid str.

    :param instance: models.Model subclass
    :param filename: str File name
    :param path: str File path
    :return: str Result file path
    """

    ext = filename.split('.')[-1]
    new_filename = os.path.join(
        path,
        str(instance.id),
        '{}.{}'.format(uuid.uuid4(), ext).lower()
    )
    return new_filename


def upload_path_handler(instance, filename):
    """
    Replace filename for uuid str.
    Would be used for `upload_to` FileField attribute.

    :param instance: model instance
    :param filename: str Origin filename
    :return: str Result filename
    """

    path = instance.FILE_PATH
    return uuid_replacer_handler(instance, filename, path=path)


def get_thumbnail(image_field, width, height, crop=False):
    """
    Return thumbnail image using minimal size: 300x200 => 150x100

    :param image_field: ImageField
    :param width: int Width result image
    :param height: int Height result image
    :param crop: crop image
    :return: str Result url path
    """

    if image_field.width > image_field.height:
        size = 0, height
    else:
        size = width, 0

    options = {'size': size, 'crop': crop, 'upscale': True}
    return get_thumbnailer(image_field).get_thumbnail(options).url


def format_number(number):
    """
    Return formatted number string.

    :param number: number
    :return: str
    """
    return '{:,}'.format(number).replace(',', ' ')
