from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar

from flask import jsonify

F = TypeVar("F", bound=Callable[..., Any])


def handle_api_errors(func: F) -> F:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        except FileNotFoundError as exc:
            return jsonify({"error": str(exc)}), 404
        except Exception as exc:  # pragma: no cover - logging real error
            return jsonify({"error": str(exc)}), 500
    return wrapper  # type: ignore[return-value]

