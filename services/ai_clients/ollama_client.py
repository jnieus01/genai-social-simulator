import requests
from services.ai_clients.ai_client import AIClient

class OllamaClient(AIClient):
    def __init__(self, base_url, model, generation_config: dict = None):
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._generation_config = generation_config or {}

    def generate_response(self, prompt: str) -> str | None:
        url = f"{self._base_url}/v1/chat/completions"
        payload = {
            "model": self._model,
            "messages": [{"role": "user", "content": prompt}],
            **self._generation_config
        }
        try:
            resp = requests.post(url, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        
        except requests.exceptions.RequestException as e:
            print(f"[OllamaClient] Error: {e}")
            return None
