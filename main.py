import argparse
from conf_lang import parse_config_string


def main():
    parser = argparse.ArgumentParser(
        description="Convert XML config to a custom language."
    )
    parser.add_argument("xml_file", help="Path to the input XML file.")
    args = parser.parse_args()

    try:
        with open(args.xml_file, "r", encoding="utf-8") as file:
            xml_string = file.read()
        output = parse_config_string(xml_string)
        if output:
            print(output, end="")
    except FileNotFoundError:
        print(f"Error: File '{args.xml_file}' not found.")


if __name__ == "__main__":
    main()
