def reverse(text):
    """
    Возвращает перевёрнутую версиб текста иои целого числа.
    """
    if isinstance(text, str):
        return text[::-1]
    elif isinstance(text, int):
        sign = -1 if text < 0 else 1
        return sign * int(str(abs(text))[::-1])
    else:
        text_type = type(text).__name__
        raise TypeError(f"reverse() expected str or int, got {text_type}")

def upper_first(text):
    """
    Влзвращает строку с заглавным первым символом.
    """
    if isinstance(text, str):
        if text == "": return ""
        else: return text[0].upper() + text[1:]
    else:
        text_type = type(text).__name__
        raise TypeError(f"upper_first() expected str, got {text_type}")
