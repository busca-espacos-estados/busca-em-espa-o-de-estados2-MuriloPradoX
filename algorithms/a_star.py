import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult



_GOAL_POS: dict[int, tuple[int, int]] = {
    tile: (i // 3, i % 3)
    for i, tile in enumerate(GOAL_STATE)
}


class AStar(BaseSearch):
    """Busca A* com heurística de distância de Manhattan.

    f(n) = g(n) + h(n)
        g(n) = custo real do caminho da raiz até n (número de movimentos)
        h(n) = soma das distâncias de Manhattan de cada peça até sua
               posição no estado objetivo

    Propriedades da heurística:
        Admissível  — nunca superestima o custo real (cada peça precisa
                      de pelo menos |Δrow| + |Δcol| movimentos).
        Consistente — satisfaz a desigualdade triangular, garantindo que
                      cada estado seja expandido no máximo uma vez e que
                      a solução encontrada seja ótima.

    Complexidade:
        Tempo  : O(b^d) no pior caso, mas muito melhor na prática
        Espaço : O(b^d) — todos os nós gerados precisam ficar no heap
    """

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan total de todas as peças até suas posições-alvo."""
        total = 0
        for i, tile in enumerate(state.tiles):
            if tile == 0:
                continue  
            goal_row, goal_col = _GOAL_POS[tile]
            curr_row, curr_col = i // 3, i % 3
            total += abs(curr_row - goal_row) + abs(curr_col - goal_col)
        return total

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(solution=initial, depth=0)

       
        counter = 0
        heap: list[tuple[int, int, State]] = [
            (self.heuristic(initial), counter, initial)
        ]

        
        best_g: dict[tuple, int] = {initial.tiles: 0}

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while heap:
            max_frontier_size = max(max_frontier_size, len(heap))

            _f, _tie, node = heapq.heappop(heap)

            
            if node.cost > best_g.get(node.tiles, float("inf")):
                continue

            nodes_expanded += 1

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            for child in node.neighbors():
                nodes_generated += 1

                if child.cost < best_g.get(child.tiles, float("inf")):
                    best_g[child.tiles] = child.cost
                    f = child.cost + self.heuristic(child)
                    counter += 1
                    heapq.heappush(heap, (f, counter, child))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
