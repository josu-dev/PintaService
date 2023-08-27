import addition as add
import division
import substraction as sub

def get_operand(name: str) -> float:
    while True:
        operand = input(f"Enter {name} operand: ").strip()
        try:
            return float(operand)
        except ValueError:
            print("Input is not a number. Please try again: ")


def main():
    while True:
        operation = input("What operation you want to perform? (+ - /):")
        left_operand = get_operand("left")
        right_operand = get_operand("right")

        match operation:
            case "+":
                print(
                    f"{left_operand} + {right_operand} = {add.addition(left_operand, right_operand)}")
            case "/":
                if right_operand == 0:
                    print("Division by zero is not allowed.")
                else:
                    print(
                    f"{left_operand} / {right_operand} = {division.division(left_operand, right_operand)}")
            case "-":
                print(
                    f"{left_operand} - {right_operand} = {sub.substraction(left_operand, right_operand)}")
            case _:
                print(
                    "Operation {operation} is not supported. Please try again.", end="\n\n")

        if input("Do you want to continue? (y/n): ").strip().lower() != "y":
            break


if __name__ == "__main__":
    main()
