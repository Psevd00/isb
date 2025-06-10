class LuhnValidator:
    @staticmethod
    def validate(card_number: str) -> bool:
        clean_num = ''.join(filter(str.isdigit, card_number))
        total = 0
        reverse_digits = clean_num[::-1]
        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        return total % 10 == 0
