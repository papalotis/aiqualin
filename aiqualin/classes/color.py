from aiqualin.classes.indexable_enum import IndexableEnum


class Color(str, IndexableEnum):
    """
    Represents different types of colors in the game Aqualin.
    """
    BLUE = "blue"
    GREEN = "green"
    PINK = "pink"
    PURPLE = "purple"
    RED = "red"
    YELLOW = "yellow"
    EMPTY = "empty"


if __name__ == "__main__":
    # reveal_type(Color.BLUE)
    # reveal_type(Color.from_index(0))

    print(Color.from_index(0) == Color.BLUE)
    print(Color.to_index(Color.BLUE) == 0)
