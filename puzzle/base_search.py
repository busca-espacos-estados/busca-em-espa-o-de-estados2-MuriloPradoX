from abc import ABC, abstractmethod
from puzzle.state import State
from puzzle.result import SearchResult


class BaseSearch(ABC):
    """Interface que todos os algoritmos de busca devem implementar."""

    @abstractmethod
    def search(self, initial: State) -> SearchResult:
        """Executa a busca a partir do estado inicial e retorna o resultado."""
        ...
