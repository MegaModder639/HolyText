def truncate(text, num):
    """
    Возвращает строку, ограниченную указанным количеством символов.
    """
    if isinstance(text, str) and isinstance(num, int) and num>0:
        if len(text) > num:
            return text[:num] + "..."
        else:
            return text[:num]
    elif isinstance(num, int) and num <= 0:
        raise ValueError("truncate() expected truncate(str, num) num>0")
    else:
        text_type = type(text).__name__
        num_type = type(num).__name__
        raise TypeError(f"truncate() expected truncate(str, int), got truncate({text_type}, {num_type})")

def slugify(text):
    """
    Возвращает строку в формате slug для использования в URL.
    """
    if isinstance(text, str):
        r0 = text.lower()
        r1 = r0.split()
        cw = []
        for word in r1:
            clean_word = ''
            for ch in word:
                if ch.isalnum():
                    clean_word += ch
            if clean_word != '':
                cw.append(clean_word)
        return "-".join(cw)
    else:
        text_type = type(text).__name__
        raise TypeError(f"slugify() expected str, got {text_type}")
