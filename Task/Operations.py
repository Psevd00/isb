import json


class JsonOperations:
    @staticmethod
    def write(filename: str, data: dict) -> None:
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except PermissionError:
            print(f"No permission to write to file {filename}.")
        except Exception as exc:
            print(f"Error writing JSON: {exc}")

    @staticmethod
    def read(filename: str) -> dict:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return {}
        except json.JSONDecodeError as e:
            print(f"JSON format error in file {filename}: {e}")
            return {}
        except Exception as exc:
            print(f"Error reading JSON: {exc}")
            return {}
