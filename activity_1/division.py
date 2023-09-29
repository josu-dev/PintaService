def division(a: int | float, b: int | float) -> int | float:
    """Divides two numbers and returns the result.

    Args:
        a (int|float): The dividend.
        b (int|float): The divisor.

    Raises:
        ZeroDivisionError: If the divisor is zero.

    Returns:
        int|float: The quotient.
    """

    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def main():
    assert division(10, 5) == 2

    exception_raised = False
    try:
        division(10, 0)
    except ZeroDivisionError:
        exception_raised = True
    assert exception_raised


if __name__ == "__main__":
    main()
