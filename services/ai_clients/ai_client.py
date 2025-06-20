from abc import ABC, abstractmethod


class AIClient(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass
