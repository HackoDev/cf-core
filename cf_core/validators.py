from rest_framework.exceptions import ValidationError


def validate_content_type(value, content_types: list):
    """
    Проверка типа файла на наличие в списке разрешенных.
    В случае, если проверка не пройдена, возбуждается исключение типа
    rest_framework.exceptions.ValidationError
    
    :param value: file pointer
    :param content_types: list Список доступных расширений
    :return: 
    """

    if value.content_type not in content_types:
        raise ValidationError("Некорректный тип файла")
