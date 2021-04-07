import unittest

from pydantic import BaseModel
from fastapi_router_controller import Controller, ControllersTags
from fastapi import APIRouter, Depends, FastAPI, Query
from fastapi.testclient import TestClient

router = APIRouter()

controller = Controller(router, openapi_tag={"name": "sample_controller"})


class SampleObject(BaseModel):
    id: str


def get_x():
    class Foo:
        def create(self):
            return "XXX"

    return Foo()


class Filter(BaseModel):
    foo: str


# With the "resource" decorator define the controller Class linked to the Controller router arguments
@controller.resource()
class SampleController:
    def __init__(self, x=Depends(get_x)):
        self.x = x

    @controller.route.get(
        "/",
        tags=["sample_controller"],
        summary="return a sample object",
        response_model=SampleObject,
    )
    def root(
        self,
        id: str = Query(..., title="itemId", description="The id of the sample object"),
    ):
        id += self.x.create()
        return SampleObject(id=id)

    @controller.route.post(
        "/hello",
        response_model=SampleObject,
    )
    def hello(
        self,
        f: Filter,
    ):
        _id = f.foo
        return SampleObject(id=_id)


def create_app():
    app = FastAPI(
        title="A sample application using fastapi_router_controller",
        version="0.1.0",
        openapi_tags=ControllersTags,
    )

    app.include_router(SampleController.router())
    return app


class TestRoutes(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.client = TestClient(app)

    def test_root(self):
        response = self.client.get("/?id=12")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "12XXX"})

    def test_hello(self):
        response = self.client.post("/hello", json={"foo": "WOW"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "WOW"})
