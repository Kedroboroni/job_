def check_string_conversion(string):
    """
    Проверяет, можно ли преобразовать строку в число
    """
    try:
        # Попытка преобразовать в float
        num = float(string)
        return True
    
    except ValueError:
        return False