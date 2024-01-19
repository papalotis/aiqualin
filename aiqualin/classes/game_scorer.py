from dataclasses import dataclass

import networkx as nx

from aiqualin.classes.animal import Animal
from aiqualin.classes.board import Board
from aiqualin.classes.color import Color
from aiqualin.classes.tile import EMPTY_TILE, Tile


@dataclass
class GameScorer:
    board: Board

    def get_property_from_tile(
        self, tile: Tile, property_to_score: type[Animal | Color]
    ) -> Animal | Color:
        if property_to_score == Animal:
            return tile.animal
        elif property_to_score == Color:
            return tile.color

        raise ValueError("property_to_score must be Animal or Color")

    def create_tile_graph(self, property_to_score: type[Animal | Color]) -> nx.Graph:
        graph = nx.Graph()

        for row_index, row in enumerate(self.board.tiles):
            for col_index, tile in enumerate(row):
                if tile == EMPTY_TILE:
                    continue

                property_value = self.get_property_from_tile(
                    tile, property_to_score=property_to_score
                )

                # we work in undirected graphs, we only need to look up and left
                # because we will add the edges in both directions
                if row_index > 0:
                    left_neighbor_tile = self.board.tiles[row_index - 1][col_index]
                    left_neighbor_property_value = self.get_property_from_tile(
                        left_neighbor_tile, property_to_score=property_to_score
                    )

                    if left_neighbor_property_value == property_value:
                        graph.add_edge(tile, left_neighbor_tile)

                if col_index > 0:
                    top_neighbor_tile = self.board.tiles[row_index][col_index - 1]
                    top_neighbor_property_value = self.get_property_from_tile(
                        top_neighbor_tile, property_to_score=property_to_score
                    )

                    if top_neighbor_property_value == property_value:
                        graph.add_edge(tile, top_neighbor_tile)

        return graph

    def score_for_property(self, property_to_score: type[Animal | Color]) -> int:
        graph = self.create_tile_graph(property_to_score=property_to_score)

        ccs = nx.connected_components(graph)

        length_to_score_map = {
            1: 0,
            2: 1,
            3: 3,
            4: 6,
            5: 10,
            6: 15,
        }

        score = sum(length_to_score_map[len(cc)] for cc in ccs if len(cc) > 1)

        return score

    @property
    def score(self) -> int:
        score_animal = self.score_for_property(Animal)
        score_color = self.score_for_property(Color)

        # the difference between the two scores is the final score
        return score_animal - score_color
