from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Cada movimento representa o espaço vazio se deslocando numa direção.
# O nome da ação descreve para onde o espaço vazio vai.
#   UP    → blank sobe    → delta = -3
#   DOWN  → blank desce   → delta = +3
#   LEFT  → blank vai esq → delta = -1
#   RIGHT → blank vai dir → delta = +1
_MOVES = [
    ("UP",    -3),
    ("DOWN",  +3),
    ("LEFT",  -1),
    ("RIGHT", +1),
]

# Coluna de cada índice do tabuleiro (0..8)
_COL = [i % 3 for i in range(9)]


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(
        self,
        tiles: Tuple[int, ...],
        parent: Optional["State"] = None,
        action: Optional[str] = None,
        cost: int = 0,
    ):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    # ------------------------------------------------------------------
    # Propriedades auxiliares
    # ------------------------------------------------------------------

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    # ------------------------------------------------------------------
    # Métodos a implementar
    # ------------------------------------------------------------------

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado.

        Para cada direção possível, verifica se o movimento é válido
        (dentro dos limites do tabuleiro e sem cruzar bordas laterais)
        e gera o estado filho trocando o espaço vazio com a peça adjacente.
        """
        children: List[State] = []
        blank = self.blank_index
        blank_col = _COL[blank]

        for action, delta in _MOVES:
            target = blank + delta

            # Fora dos limites do tabuleiro
            if target < 0 or target > 8:
                continue

            # LEFT não pode cruzar a borda esquerda (col 0 → col 2 da linha acima)
            if action == "LEFT" and blank_col == 0:
                continue

            # RIGHT não pode cruzar a borda direita (col 2 → col 0 da linha abaixo)
            if action == "RIGHT" and blank_col == 2:
                continue

            # Troca blank com a peça de destino
            new_tiles = list(self.tiles)
            new_tiles[blank], new_tiles[target] = new_tiles[target], new_tiles[blank]

            children.append(
                State(
                    tiles=tuple(new_tiles),
                    parent=self,
                    action=action,
                    cost=self.cost + 1,
                )
            )

        return children

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este.

        Percorre a cadeia de ponteiros parent de trás para frente e
        inverte a lista para ter a ordem cronológica correta.
        """
        states: List[State] = []
        node: Optional[State] = self
        while node is not None:
            states.append(node)
            node = node.parent
        states.reverse()
        return states

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este.

        Usa path() e descarta o primeiro elemento (estado inicial,
        que não possui ação associada).
        """
        return [s.action for s in self.path() if s.action is not None]

    # ------------------------------------------------------------------
    # Métodos de suporte (não alterar)
    # ------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        # Necessário para desempate no heapq do A*
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
