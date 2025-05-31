class Luhn:

    @staticmethod
    def alg_luhn(num_card: str) -> bool:
        """
        Алгоритм Луна
        :param num_card: номер карты
        :return: true или false
        """
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
    def print_res(num_card: str) -> None:
        """
        Вывод результатов алгоритма Луна
        :param num_card:номер карты
        :return: None
        """
        if Luhn.alg_luhn(num_card):
            print("This card number is valid")
        else:
            print("This card number is not valid")