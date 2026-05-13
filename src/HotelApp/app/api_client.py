"""
Cliente HTTP para comunicarse con la API FastAPI de HOT TEL.

Centraliza toda comunicacion entre la interfaz (ej. Streamlit o CLI Typer) y el backend:
  - URL base leida desde settings (una sola fuente de verdad).
  - Manejo uniforme de errores HTTP: extrae el campo 'detail' que
    FastAPI siempre incluye en sus respuestas de error.
  - Timeouts configurados para evitar que la UI se congele si
    el backend no responde.
  - Devuelve (data, error): el llamador decide como mostrar el error,
    manteniendo la logica de UI separada del transporte HTTP.

Patron de uso:

    from src.app.api_client import ApiClient

    client = ApiClient()
    users, err = client.get("/users/")
    if err:
        print(f"Error: {err}")
    else:
        print(users)
"""

import httpx

from src.core.config import settings

# Timeout en segundos para todas las peticiones al backend.
_TIMEOUT = 10.0


class ApiClient:
    """Cliente HTTP liviano sobre httpx para consumir la API FastAPI."""

    def __init__(self) -> None:
        self.base_url = settings.api_base_url.rstrip("/")

    # ── Helpers privados ──────────────────────────────────────────────────────

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    @staticmethod
    def _handle(response: httpx.Response) -> tuple[dict | list | None, str | None]:
        """Procesa una respuesta HTTP y retorna (data, error).

        Returns:
            (data, None)  si la respuesta es exitosa (2xx).
            (None, error) si la respuesta es un error HTTP o de red.
        """
        try:
            response.raise_for_status()
            # 204 No Content: exito sin cuerpo.
            if response.status_code == 204:
                return None, None
            return response.json(), None
        except httpx.HTTPStatusError:
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            return None, str(detail)

    # ── Metodos HTTP publicos ─────────────────────────────────────────────────

    def get(self, path: str) -> tuple[list | dict | None, str | None]:
        """GET al path indicado."""
        try:
            r = httpx.get(self._url(path), timeout=_TIMEOUT)
            return self._handle(r)
        except httpx.RequestError as e:
            return None, f"No se pudo conectar con la API: {e}"

    def post(self, path: str, body: dict) -> tuple[dict | None, str | None]:
        """POST con body JSON al path indicado."""
        try:
            r = httpx.post(self._url(path), json=body, timeout=_TIMEOUT)
            return self._handle(r)
        except httpx.RequestError as e:
            return None, f"No se pudo conectar con la API: {e}"

    def put(self, path: str, body: dict) -> tuple[dict | None, str | None]:
        """PUT con body JSON al path indicado. Útil para actualizar la info del Hotel."""
        try:
            r = httpx.put(self._url(path), json=body, timeout=_TIMEOUT)
            return self._handle(r)
        except httpx.RequestError as e:
            return None, f"No se pudo conectar con la API: {e}"

    def patch(self, path: str, body: dict) -> tuple[dict | None, str | None]:
        """PATCH con body JSON al path indicado."""
        try:
            r = httpx.patch(self._url(path), json=body, timeout=_TIMEOUT)
            return self._handle(r)
        except httpx.RequestError as e:
            return None, f"No se pudo conectar con la API: {e}"

    def delete(self, path: str) -> tuple[None, str | None]:
        """DELETE al path indicado."""
        try:
            r = httpx.delete(self._url(path), timeout=_TIMEOUT)
            return self._handle(r)
        except httpx.RequestError as e:
            return None, f"No se pudo conectar con la API: {e}"