import base64
import io
from dataclasses import dataclass

import requests
from config import Config


@dataclass
class LLMResponse:
    text: str


class OllamaGenerateModel:
    def __init__(self, response_format=None):
        self.response_format = response_format

    def generate_content(self, content):
        prompt, images = self._normalize_content(content)
        payload = {
            "model": Config.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        }

        if images:
            payload["images"] = images
        if self.response_format:
            payload["format"] = self.response_format

        try:
            response = requests.post(
                _ollama_url("/api/generate"),
                json=payload,
                timeout=Config.OLLAMA_REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise RuntimeError(f"Ollama request failed: {exc}") from exc
        except ValueError as exc:
            raise RuntimeError("Ollama returned a non-JSON response.") from exc

        return LLMResponse(text=data.get("response", ""))

    def _normalize_content(self, content):
        if isinstance(content, str):
            return content, []

        if not isinstance(content, (list, tuple)):
            return str(content), []

        prompt_parts = []
        images = []

        for item in content:
            if isinstance(item, str):
                prompt_parts.append(item)
            elif hasattr(item, "save"):
                images.append(_encode_image(item))
            else:
                prompt_parts.append(str(item))

        return "\n".join(prompt_parts), images


def _ollama_url(path):
    return f"{Config.OLLAMA_BASE_URL}{path}"


def _encode_image(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def get_available_models():
    try:
        response = requests.get(
            _ollama_url("/api/tags"),
            timeout=Config.OLLAMA_REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise RuntimeError(f"Unable to reach Ollama at {Config.OLLAMA_BASE_URL}: {exc}") from exc
    except ValueError as exc:
        raise RuntimeError("Ollama model list returned a non-JSON response.") from exc

    names = []
    for model in data.get("models", []):
        name = model.get("name") or model.get("model")
        if name:
            names.append(name)
    return names


def has_model(model_names, selected_model):
    if selected_model in model_names:
        return True
    if ":" not in selected_model and f"{selected_model}:latest" in model_names:
        return True
    return False


def is_model_available(model_name=None):
    selected_model = model_name or Config.OLLAMA_MODEL
    return has_model(get_available_models(), selected_model)


def get_vision_model():
    """Returns the local Ollama client used for vision inference."""
    return OllamaGenerateModel()


def get_quiz_model():
    """Returns the local Ollama client used for JSON quiz generation."""
    return OllamaGenerateModel(response_format="json")
