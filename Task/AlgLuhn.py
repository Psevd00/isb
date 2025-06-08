class LuhnValidator:
    @staticmethod
    def validate(num_card: str) -> bool:
        total = 0
        for i, digit in enumerate(reversed(num_card)):
            num = int(digit)
            if i % 2 == 1:
                num *= 2
                if num > 9:
                    num -= 9
            total += num
        return total % 10 == 0

    @staticmethod
    def print_result(num_card: str) -> None:
        if LuhnValidator.validate(num_card):
            print("This card number is valid")
        else:
            print("This card number is not valid")
