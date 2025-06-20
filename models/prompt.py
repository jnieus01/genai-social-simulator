from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Prompt:
    prompt: str  # Instructions for the model to stay in character or follow a specific style

    def apply(self, user_prompt: str) -> str:
        return f"{self.prompt}\n\n{user_prompt}"
