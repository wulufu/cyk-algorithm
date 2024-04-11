def main():

    input_string = input("Enter a string: ")
    rules = {}

    with open("cfg.txt") as file:
        lines = file.read().splitlines()

    for line in lines:
        line = line.replace(' ', '')
        lhs = line[0]
        rhs = line[3:]

        if lhs in rules:
            rules[lhs].append(rhs)
        else:
            rules[lhs] = [rhs]


if __name__ == "__main__":
    main()
