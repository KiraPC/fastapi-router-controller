from fastapi import FastAPI
from fastapi_router_controller import ControllersTags
from controller.sample_controller import SampleController
from controller.sample_controller_2 import AnotherSampleController

app = FastAPI(
    title='A sample application using fastapi_router_controller',
    version="0.1.0",
    openapi_tags=ControllersTags)

sample_controller = SampleController()
another_sample_controller = AnotherSampleController()

app.include_router(sample_controller.router())
app.include_router(another_sample_controller.router())

print(app.openapi())
