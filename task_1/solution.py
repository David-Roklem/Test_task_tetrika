import inspect


def strict(func):
    """Декоратор, который проверяет соответствие типов переданных аргументов
    типам, указанным в аннотациях функции."""
    sig = inspect.signature(func)
    parameters = sig.parameters
    param_names = list(parameters.keys())
    annotations = func.__annotations__
    expected_types = [annotations[name] for name in param_names]

    def wrapper(*args, **kwargs):
        bound_arguments = sig.bind(*args, **kwargs)
        bound_arguments.apply_defaults()
        arguments = bound_arguments.arguments

        for name, expected_type in zip(param_names, expected_types):
            value = arguments[name]
            actual_type = type(value)
            if actual_type is not expected_type:
                raise TypeError(
                    (f"Параметр '{name}' должен быть типа {expected_type.__name__},"
                     f" а вы передали тип {actual_type.__name__}")
                )

        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


# Тесты
def run_tests():
    # Тест 1: Корректные типы
    assert sum_two(3, 5) == 8, "Test 1 Failed"

    # Тест 2: Неправильный тип для 'a' (str)
    try:
        sum_two("3", 5)
    except TypeError as e:
        assert str(e) == "Параметр 'a' должен быть типа int, а вы передали тип str", "Test 2 Failed"

    # Тест 3: Неправильный тип для 'b' (str)
    try:
        sum_two(3, "5")
    except TypeError as e:
        assert str(e) == "Параметр 'b' должен быть типа int, а вы передали тип str", "Test 3 Failed"

    # Тест 4: Неправильный тип для 'a' (float)
    try:
        sum_two(3.0, 5)
    except TypeError as e:
        assert str(e) == "Параметр 'a' должен быть типа int, а вы передали тип float", "Test 4 Failed"

    # Тест 5: Неправильный тип для 'b' (float)
    try:
        sum_two(3, 5.0)
    except TypeError as e:
        assert str(e) == "Параметр 'b' должен быть типа int, а вы передали тип float", "Test 5 Failed"

    # Тест 6: Неправильный тип для 'a' (bool)
    try:
        sum_two(True, 5)
    except TypeError as e:
        assert str(e) == "Параметр 'a' должен быть типа int, а вы передали тип bool", "Test 6 Failed"

    # Тест 7: Неправильный тип для 'b' (bool)
    try:
        sum_two(3, False)
    except TypeError as e:
        assert str(e) == "Параметр 'b' должен быть типа int, а вы передали тип bool", "Test 7 Failed"

    print("Все тесты пройдены!")


if __name__ == "__main__":
    run_tests()
