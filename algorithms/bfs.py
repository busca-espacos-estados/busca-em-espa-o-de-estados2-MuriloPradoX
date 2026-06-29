from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):
    """Busca em Largura (Breadth-First Search).

    Explora os nós camada por camada em ordem crescente de profundidade,
    garantindo que a primeira solução encontrada seja a de menor custo
    (número de movimentos).

    Complexidade:
        Tempo  : O(b^d)  — b = fator de ramificação (≤ 4), d = profundidade da solução
        Espaço : O(b^d)  — todos os nós da fronteira precisam ficar em memória
    """

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(solution=initial, depth=0)

        
        frontier: deque[State] = deque([initial])

        
        visited: set[tuple] = {initial.tiles}

        nodes_expanded = 0
        nodes_generated = 1          
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))

            node = frontier.popleft()
            nodes_expanded += 1

            for child in node.neighbors():
                nodes_generated += 1

                if child.is_goal:
                    return SearchResult(
                        solution=child,
                        nodes_expanded=nodes_expanded,
                        nodes_generated=nodes_generated,
                        max_frontier_size=max_frontier_size,
                        depth=child.cost,
                    )

                if child.tiles not in visited:
                    visited.add(child.tiles)
                    frontier.append(child)

        
        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
