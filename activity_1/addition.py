def addition(x: int|float, y: int|float) -> int|float:
    """Add two numbers.
    
    Args:
        x (int): The first number to add.
        y (int): The second number to add.
        
    Returns:
        int: The sum of x and y.
    """
    return x + y

def main():
    """Entry point for the program."""
    print(addition(1, 2))
    
if __name__ == "__main__":
    main()