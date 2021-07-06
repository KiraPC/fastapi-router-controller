from fastapi import FastAPI
from fastapi_router_controller import Controller, ControllersTags

# just import the main package to load all the controllers in
import controller  # noqa

app = FastAPI(
    title="A sample application using fastapi_router_controller"
    + "with controller auto import",
    version="0.1.0",
    # all of the router openapi_tags are collected in ControllerTags object
    openapi_tags=ControllersTags,
)

for router in Controller.routers():
    app.include_router(router)
