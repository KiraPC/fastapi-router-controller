"""FastAPI Router Contoller, FastAPI utility to allow Controller Class usage"""

from fastapi_router_controller.lib.controller import Controller as Controller
from fastapi_router_controller.lib.controller import OPEN_API_TAGS as ControllersTags
from fastapi_router_controller.lib.controller_loader import (
    ControllerLoader as ControllerLoader,
)

__all__ = ["Controller", "ControllersTags", "ControllerLoader"]
