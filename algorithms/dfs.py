from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):
    """Busca em Profundidade com limite de profundidade (Depth-Limited DFS).

    Implementação iterativa com pilha explícita para evitar estouro de pilha
    de recursão em puzzles profundos.

    A detecção de ciclos é feita por caminho (path-checking): cada nó carrega
    o conjunto de tiles do seu caminho desde a raiz. Isso permite que estados
    já visitados em outros ramos sejam explorados novamente — comportamento
    correto e necessário para a DFS com limite de profundidade.

    Complexidade:
        Tempo  : O(b^m)  — m = depth_limit
        Espaço : O(b × m) — apenas o caminho atual precisa ficar em memória
    """

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(solution=initial, depth=0)

        
        stack: list[tuple[State, frozenset]] = [
            (initial, frozenset({initial.tiles}))
        ]

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while stack:
            max_frontier_size = max(max_frontier_size, len(stack))

            node, path_visited = stack.pop()
            nodes_expanded += 1

            
            if node.cost >= self.depth_limit:
                continue

            
            for child in reversed(node.neighbors()):
                nodes_generated += 1

                if child.is_goal:
                    return SearchResult(
                        solution=child,
                        nodes_expanded=nodes_expanded,
                        nodes_generated=nodes_generated,
                        max_frontier_size=max_frontier_size,
                        depth=child.cost,
                    )

                
                if child.tiles not in path_visited:
                    stack.append((child, path_visited | {child.tiles}))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
