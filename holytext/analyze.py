def count_words(text):
    """
    Возвращает количество слов в строке.
    """
    if isinstance(text, str):
        words = text.split()
        return len(words)
    else:
        text_type = type(text).__name__
        raise TypeError(f"count_words() expected str, got {text_type}")
        
def is_palindrome(text):
    """
    Проверяет, является ли строка палиндромом.
    """
    if isinstance(text, str):
        r = text[::-1].lower()
        if r == text.lower():
            return True
        else: return False
    else:
        text_type = type(text).__name__
        raise TypeError(f"is_palindrome() expected str, got {text_type}")
