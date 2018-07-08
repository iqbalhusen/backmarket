import copy


def find_bracket_indices(s, bracket_open_char, bracket_close_char):
    s.insert(0, bracket_open_char)
    bracket_indices = {}
    bracket_stack = []

    for i, c in enumerate(s):
        if c == bracket_open_char:
            bracket_stack.append(i)
        elif c == bracket_close_char:
            if len(bracket_stack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            bracket_indices[bracket_stack.pop()] = i

    if len(bracket_stack) > 0:
        raise IndexError("No matching opening parens at: " + str(bracket_stack.pop()))

    return bracket_indices


def parse_molecule(molecule, multiply_by=1):
    atom = None
    molecule = list(molecule)

    while molecule:
        char = molecule.pop(0)

        if char.isupper():
            if atom:
                if atom in UNIQUE_ATOM_COUNTS:
                    UNIQUE_ATOM_COUNTS[atom] += multiply_by
                else:
                    UNIQUE_ATOM_COUNTS[atom] = multiply_by

            atom = char

        elif char.islower():
            atom += char

        elif char == '(':
            call_recursive(molecule, multiply_by, '(', ')')

        elif char == '[':
            call_recursive(molecule, multiply_by, '[', ']')

        elif char == '{':
            call_recursive(molecule, multiply_by, '{', '}')

        else:
            atom_count = int(char)
            if atom in UNIQUE_ATOM_COUNTS:
                UNIQUE_ATOM_COUNTS[atom] += atom_count * multiply_by
            else:
                UNIQUE_ATOM_COUNTS[atom] = atom_count * multiply_by
            atom = None

    if atom:
        if atom in UNIQUE_ATOM_COUNTS:
            UNIQUE_ATOM_COUNTS[atom] += multiply_by
        else:
            UNIQUE_ATOM_COUNTS[atom] = multiply_by


def call_recursive(_molecule, _multiply_by, bracket_open_char, bracket_close_char):
    bracket_indices = find_bracket_indices(copy.deepcopy(_molecule), bracket_open_char, bracket_close_char)
    list_inside_bracket = _molecule[:bracket_indices[0] - 1]
    char_after_closing_bracket = _molecule[bracket_indices[0]] if bracket_indices[0] < len(_molecule) else None

    del_till_index = bracket_indices[0]

    if char_after_closing_bracket.isdigit():
        _multiply_by *= int(char_after_closing_bracket)
        del_till_index += 1

    del _molecule[:del_till_index]

    parse_molecule(list_inside_bracket, _multiply_by)


if __name__ == '__main__':
    molecule_formula = input('Type molecule formula and hit enter: ')
    print('Formula entered: ' + molecule_formula)

    UNIQUE_ATOM_COUNTS = {}

    parse_molecule(molecule_formula)
    print('UNIQUE_ATOM_COUNTS: ', UNIQUE_ATOM_COUNTS)
