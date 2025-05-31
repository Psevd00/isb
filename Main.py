from Task.AlgLuhn import Luhn
from Task.Find_card import FindCard
from Task.Operations import read_json
from Task.Measuring_time import MeasuringTime


def find_card_action(settings: dict) -> None:
    """
    Найдите карту по ее хэш-значению, используя параллельную обработку.
    :return: None
    """ ""
    try:
        bins = settings["bins"]
        last_digits = settings["last_four_digits"]
        target_hash = settings["hash"]
        filepath = settings["filepath"]
        cores = FindCard.number_of_cores()

        card = FindCard.find_card_parallel(bins, last_digits, target_hash, cores)

        if card:
            print(f"\nFound card: {card}")
            FindCard.serialization_res(bins, last_digits, target_hash, cores, filepath)
        else:
            print("\nCard not found")
    except Exception as e:
        print(f"\nError: {e}")


def measure_performance_action(settings: dict) -> None:
    """
    Измеряет эффективность поиска с помощью различных основных показателей.
    :return: None
    """

    try:
        print("\nMeasuring performance...")

        bins = settings["bins"]
        last_digits = settings["last_four_digits"]
        target_hash = settings["hash"]

        times_result = MeasuringTime.meas_time(bins, last_digits, target_hash)
        MeasuringTime.plot_time(times_result)
    except Exception as e:
        print(f"\nError: {e}")


def validate_card_action() -> None:
    """Подтвердите номер карты с помощью алгоритма Луна."""
    card = input("\nEnter card number to validate: ")
    if Luhn.alg_luhn(card):
        print("Card is valid")
    else:
        print("Card is invalid")


def change_settings_action() -> dict:
    """
    Изменение настроек приложения, загрузив новый файл конфигурации.
    :return:
    """
    new_file = input("\nEnter settings filename (or press Enter to cancel): ")
    if new_file:
        try:
            settings = read_json(new_file)
            print("Settings updated!")
            return settings

        except Exception as e:
            print(f"Error loading settings: {e}")


def show_menu() -> None:
    """Отобразите пункты главного меню."""
    print("\n" + "=" * 40)
    print("  BANK CARD SEARCH SYSTEM  ".center(40, "="))
    print("=" * 40)
    print("1. Find card by hash")
    print("2. Measure performance")
    print("3. Validate card (Luhn algorithm)")
    print("4. Change settings")
    print("0. Exit")
    print("=" * 40)


def main() -> None:
    """Основная точка входа в приложение."""
    settings = read_json("Settings.json")

    while True:
        show_menu()
        choice = input("Select option: ")

        match choice:
            case "1":
                find_card_action(settings)
            case "2":
                measure_performance_action(settings)
            case "3":
                validate_card_action()
            case "4":
                new_settings = change_settings_action()
                settings = new_settings
            case "0":
                print("Exiting...")
                break
            case _:
                print("Invalid selection")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()