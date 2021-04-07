from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_router_controller import ControllersTags
from controller.sample_controller import SampleController
from controller.sample_controller_2 import AnotherSampleController

app = FastAPI(
    title='A sample application using fastapi_router_controller',
    version="0.1.0",
    openapi_tags=ControllersTags)

app.include_router(SampleController.router())
app.include_router(AnotherSampleController.router())
