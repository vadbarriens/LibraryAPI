import re
from django.core.exceptions import ValidationError


def validate_profanity(value):
    """Валидатор, который не пропускает плохие слова"""
    if not isinstance(value, str):
        return

    bad_words = {'крипта', 'казино', 'насилие', 'расист', 'убийство', 'наркотик', 'коррупция'}
    lower_value = value.lower()

    # Разбиваем текст на слова с учётом пунктуации
    words = re.findall(r'\b\w+\b', lower_value)

    for word in words:
        if word in bad_words:
            raise ValidationError(f"Запрещённое слово: '{word}'")
