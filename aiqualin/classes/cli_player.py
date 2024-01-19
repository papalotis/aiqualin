from aiqualin.classes.action import Action
from aiqualin.classes.action_generator import ActionGenerator
from aiqualin.classes.board import Board
from aiqualin.classes.player import AbstractPlayer
from aiqualin.classes.tile import Tile


class CLIPlayer(AbstractPlayer):
    def next_action(
        self, board: Board, open_tiles: list[Tile], closed_tiles: list[Tile]
    ) -> Action:
        print()

        our_score = self.our_score(board)
        their_score = self.their_score(board)

        our_side_str = f"{self.our_side.__name__.title()}"
        their_side_str = f"{self.their_side.__name__.title()}"

        print(f"Your score: {our_score} ({our_side_str})")
        print(f"Opponent score: {their_score} ({their_side_str})")

        board.visualize()
        print()
        print("Currently open tiles:")
        for i, tile in enumerate(open_tiles, start=1):
            tile_pretty = f"{tile.color.name.title()} {tile.animal.name.title()} {tile.short_string()}"
            print(f"{i}. {tile_pretty}")

        print()
        print("Number of closed tiles:", len(closed_tiles))
        print()

        action_str = input("Enter action: ")

        all_possible_actions = ActionGenerator(
            board, open_tiles, closed_tiles
        ).generate_actions()
        while True:
            while True:
                try:
                    action_string_parts = action_str.split()
                    new_tile = open_tiles[int(action_string_parts[-1]) - 1]

                    new_tile_str = filter(str.isdigit, new_tile.short_string())

                    string_input = " ".join(action_string_parts[:-1] + [*new_tile_str])

                    print("You entered:", string_input)

                    action = Action.from_string(string_input)
                    break
                except Exception:
                    action_str = input("Invalid input. Try again: ")
                    continue

            if action in all_possible_actions:
                break

            action_str = input("Invalid action. Try again: ")

        print()

        return action


class CLIPlayerWithBestMoveSuggestion(CLIPlayer):
    def next_action(
        self, board: Board, open_tiles: list[Tile], closed_tiles: list[Tile]
    ) -> Action:
        """
        Prints the move that would currently give the highest score difference. Then prompts the user to enter their move.
        """
        actions = ActionGenerator(board, open_tiles, closed_tiles).generate_actions()

        best_action = max(
            actions,
            key=lambda action: self.our_score(board.apply_action(action))
            - self.their_score(board.apply_action(action)),
        )

        print("Best move:", best_action)

        return super().next_action(board, open_tiles, closed_tiles)
