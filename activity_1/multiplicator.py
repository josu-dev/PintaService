def multiplication(x: int|float, y: int|float) -> int|float:
    """Multiplicate two numbers.
    
    Args:
        x (int): The first number to operate.
        y (int): The second number to operate.
        
    Returns:
        int: The product of x and y.
    """
    return x * y

def main():
    """Entry point for the program."""
    print(multiplication(1, 2))
    
if __name__ == "__main__":
    main()