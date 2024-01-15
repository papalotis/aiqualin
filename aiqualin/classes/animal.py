from aiqualin.classes.indexable_enum import IndexableEnum


class Animal(str, IndexableEnum):
    """
    Represents different types of animals in the game Aqualin.
    """

    CRAB = "crab"
    FISH = "fish"
    JELLYFISH = "jellyfish"
    SEAHORSE = "seahorse"
    STARFISH = "starfish"
    TURTLE = "turtle"
    EMPTY = "empty"
