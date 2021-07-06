import os
from fastapi_router_controller import ControllerLoader

this_dir = os.path.dirname(__file__)

# load all the module inside the given path
ControllerLoader.load(this_dir, __package__)
