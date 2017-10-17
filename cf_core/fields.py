from django import forms
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class RestrictedFileField(models.FileField):

    errors = {
        'max_size': "Превышен размер файла, "
                    "максимальный размер для загрузки: %s",
        'invalid_ext': 'Неразрешенный тип файла, список доступных типов: %s'
    }

    def __init__(self, verbose_name=None, name=None, content_types=None,
                 max_upload_size=0, **kwargs):
        self.content_types = content_types or []
        self.max_upload_size = max_upload_size
        super(RestrictedFileField, self).__init__(verbose_name, name, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(RestrictedFileField, self).clean(*args, **kwargs)

        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if self.max_upload_size > 0:
                    if file._size > self.max_upload_size:
                        raise forms.ValidationError(
                            self.errors['max_size'] % self.max_upload_size
                        )
            else:
                raise forms.ValidationError(
                    self.errors['invalid_ext'] % self.content_types
                )
        except AttributeError:
            pass

        return data


class RestrictedImageField(RestrictedFileField, ThumbnailerImageField):
    pass
