from aiqualin.classes.indexable_enum import IndexableEnum


class Animal(str, IndexableEnum):
    CRAB = "crab"
    FISH = "fish"
    JELLYFISH = "jellyfish"
    SEAHORSE = "seahorse"
    STARFISH = "starfish"
    TURTLE = "turtle"
    EMPTY = "empty"
