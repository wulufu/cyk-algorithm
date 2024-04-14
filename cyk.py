import argparse
import re
import sys

_DEFAULT_FILENAME = "cfg.txt"


def main():
    """Performs CYK on strings input by the user until the program exits.

    A CFG is generated from a file. The name for this file can be provided
    using command-line arguments, otherwise _DEFAULT_FILENAME will be used.
    The program will exit if the file is not found, or if the file does not
    contain a valid CFG.

    Once the CFG is created the user will be prompted to enter a string.
    CYK will be performed on this string, and the result will be displayed.
    This will repeat indefinitely until the program is terminated.
    """
    args = _get_cmdline_args()
    filename = args.file

    try:
        with open(filename) as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f'File "{filename}" was not found.')
        sys.exit(1)
    except OSError:
        print(f'File "{filename}" could not be opened.')
        sys.exit(1)

    try:
        cfg = CFG(lines)
    except CFGFormatError:
        print(f'File "{filename}" does not contain a valid CFG.')
        sys.exit(1)

    try:
        while True:
            string = input("Enter a string: ")
            result = cfg.test_string(string)

            if result:
                print(f'String "{string}" can be generated by the CFG.')
            else:
                print(f'String "{string}" can NOT be generated by the CFG.')
    except (KeyboardInterrupt, EOFError):
        sys.exit()


class CFG:
    """A context-free grammar in Chomsky Normal Form."""

    _PATTERN = re.compile(r"[A-Z]->([A-Z][A-Z]|[^A-Z])(\|([A-Z][A-Z]|[^A-Z]))*")

    def __init__(self, rules: list[str]) -> None:
        """Converts a list of strings representing rules into a CFG.

        Each string must be a single line of the form "A -> BC" or "A -> a",
        where 'A', 'B', and 'C' are variables, and 'a' is a terminal.
        Optionally, two or more rules with the same left-hand side can be
        combined into one line using the form "A -> BC | a".

        A variable that appears on the right-hand side of a rule must also be
        defined on the left-hand side of at least one rule. The first variable
        to be defined is assumed to be the axiom of the CFG.

        If any rule is formatted incorrectly, a CFGFormatError is raised.
        """
        self._rules: dict[str, set[str]] = {}

        for string in rules:
            self._add_rule(string)

        self._variables = self._rules.keys()
        self._axiom = next(iter(self._variables))

        self._validate_rules()

    def test_string(self, string: str) -> bool:
        """Uses CYK to determine if a string can be generated by the CFG."""
        if not string:
            return False

        length = len(string)
        table = [[set() for _ in range(length)] for _ in range(length)]

        # Generate bottom row using the characters of the input string
        for i in range(length):
            for variable in self._variables:
                if string[i] in self._rules[variable]:
                    table[i][i].add(variable)

        # Generate remaining rows using dynamic programming approach
        for row in range(1, length):
            for i in range(length - row):
                j = i + row

                for k in range(row):
                    result = _cross_product(table[i][i + k], table[i + k + 1][j])

                    # Find any variables that produce strings in the result
                    for string in result:
                        for variable in self._variables:
                            if string in self._rules[variable]:
                                table[i][j].add(variable)

        top_row = table[0][length - 1]
        return self._axiom in top_row

    def _add_rule(self, string: str) -> None:
        # Converts a string into a CFG rule and adds it to the dict of rules.
        # If the string is not valid a CFGFormatError is raised.
        rule = re.sub(r"\s+", "", string)

        if not re.fullmatch(self._PATTERN, rule):
            raise CFGFormatError

        split_rule = rule.split("->")
        lhs = split_rule[0]
        rhs = split_rule[1].split('|')

        if lhs not in self._rules:
            self._rules[lhs] = set(rhs)
        else:
            self._rules[lhs].union(set(rhs))

    def _validate_rules(self) -> None:
        # Raises a CFGFormatError if a variable appears on the right-hand side
        # of a rule but is never defined.
        for rhs in self._rules.values():
            for string in rhs:
                if len(string) > 1:
                    for variable in string:
                        if variable not in self._variables:
                            raise CFGFormatError


class CFGFormatError(Exception):
    """Raised when attempting to create a rule from an invalid string."""


def _cross_product(first_set: set[str], second_set: set[str]) -> set[str]:
    # Computes and returns the cross product of two sets of strings.
    result = set()

    for string_first in first_set:
        for string_second in second_set:
            result.add(string_first + string_second)

    return result


def _get_cmdline_args() -> argparse.Namespace:
    # Parses and returns command-line arguments for the program.
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",
                        default=_DEFAULT_FILENAME,
                        help='the file to generate rules from '
                             '(default: "%(default)s")')

    return parser.parse_args()


if __name__ == "__main__":
    main()
