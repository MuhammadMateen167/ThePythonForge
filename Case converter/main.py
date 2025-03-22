def convert_to_snake_case(pascal_or_camel_cased_string):
    snake_case_string = [
        "_" + char.lower() if char.isupper() else char
        for char in pascal_or_camel_cased_string
    ]
    return "".join(snake_case_string).strip("_")


def main():
    camelCase_or_PascalCase_string = input(
        "Enter the string you want to convert into snake_case: "
    )
    snake_case_string = convert_to_snake_case(camelCase_or_PascalCase_string)
    print(snake_case_string)


if __name__ == "__main__":
    main()
