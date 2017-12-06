from rest_framework.exceptions import ValidationError


def validate_content_type(value, content_types: list):
    """
    Validate file for available content types.

    :param value: file
    :param content_types: list Available content types as str list.
    :return: bool
    """
    if value.content_type not in content_types:
        raise ValidationError(_('Incorrect file type'))
