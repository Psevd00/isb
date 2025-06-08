from Task.AlgLuhn import LuhnValidator
from Task.Find_card import CardFinder
from Task.Operations import JsonOperations
from Task.Measuring_time import PerformanceMeasurer


class BankCardSystem:
    def __init__(self):
        self.settings = JsonOperations.read_json("Settings.json")
        self.card_finder = CardFinder()
        self.performance_measurer = PerformanceMeasurer()
        self.luhn_validator = LuhnValidator()

    def find_card_action(self) -> None:
        try:
            bins = self.settings["bins"]
            last_digits = self.settings["last_four_digits"]
            target_hash = self.settings["hash"]
            filepath = self.settings["filepath"]

            card = self.card_finder.find_card_parallel(bins, last_digits, target_hash)

            if card:
                print(f"\nFound card: {card}")
                self.card_finder.serialization_res(bins, last_digits, target_hash, filepath)
            else:
                print("\nCard not found")
        except Exception as e:
            print(f"\nError: {e}")

    def measure_performance_action(self) -> None:
        try:
            print("\nMeasuring performance...")
            times_result = self.performance_measurer.meas_time(
                self.settings["bins"],
                self.settings["last_four_digits"],
                self.settings["hash"]
            )
            self.performance_measurer.plot_time(times_result)
        except Exception as e:
            print(f"\nError: {e}")

    def validate_card_action(self) -> None:
        card = input("\nEnter card number to validate: ")
        if self.luhn_validator.validate(card):
            print("Card is valid")
        else:
            print("Card is invalid")

    def change_settings_action(self) -> None:
        new_file = input("\nEnter settings filename (or press Enter to cancel): ")
        if new_file:
            try:
                self.settings = JsonOperations.read_json(new_file)
                print("Settings updated!")
            except Exception as e:
                print(f"Error loading settings: {e}")

    def show_menu(self) -> None:
        print("\n" + "=" * 40)
        print("  BANK CARD SEARCH SYSTEM  ".center(40, "="))
        print("=" * 40)
        print("1. Find card by hash")
        print("2. Measure performance")
        print("3. Validate card (Luhn algorithm)")
        print("4. Change settings")
        print("0. Exit")
        print("=" * 40)

    def run(self) -> None:
        while True:
            self.show_menu()
            choice = input("Select option: ")

            match choice:
                case "1":
                    self.find_card_action()
                case "2":
                    self.measure_performance_action()
                case "3":
                    self.validate_card_action()
                case "4":
                    self.change_settings_action()
                case "0":
                    print("Exiting...")
                    break
                case _:
                    print("Invalid selection")

            input("\nPress Enter to continue...")


if __name__ == "__main__":
    system = BankCardSystem()
    system.run()
