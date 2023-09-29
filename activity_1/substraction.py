def substraction(x: int | float, y: int | float) -> int | float:
    """Substract two numbers.

    Args:
        x (int): The first number to substract.
        y (int): The second number to substract.

    Returns:
        int: The substract of x and y.
    """
    return x - y


def main():
    """Entry point for the program."""
    print(substraction(1, 2))


if __name__ == "__main__":
    main()
