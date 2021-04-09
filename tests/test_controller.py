import unittest

from pydantic import BaseModel
from fastapi_router_controller import Controller, ControllersTags
from fastapi import APIRouter, Depends, FastAPI, Query
from fastapi.testclient import TestClient


class SampleObject(BaseModel):
    id: str


def get_x():
    class Foo:
        def create(self):
            return "XXX"

    return Foo()


def get_y():
    try:
        yield "get_y_dep"
    finally:
        print("get_y done")


class Filter(BaseModel):
    foo: str


def create_app_declerative():
    router = APIRouter()
    controller = Controller(router, openapi_tag={"name": "sample_controller"})

    # With the 'resource' decorator define the controller Class linked to the Controller router arguments
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
            id: str = Query(
                ..., title="itemId", description="The id of the sample object"
            ),
        ):
            id += self.x.create()
            return SampleObject(id=id)

        @controller.route.post(
            "/hello", response_model=SampleObject,
        )
        def hello(self, f: Filter, y=Depends(get_y)):
            _id = f.foo
            _id += y
            _id += self.x.create()
            return SampleObject(id=_id)

    app = FastAPI(
        title="A sample application using fastapi_router_controller",
        version="0.1.0",
        openapi_tags=ControllersTags,
    )

    app.include_router(SampleController.router())
    return app


def create_app_imperative():
    class SampleController:
        def __init__(self, x=Depends(get_x)):
            self.x = x

        def root(
            self,
            id: str = Query(
                ..., title="itemId", description="The id of the sample object"
            ),
        ):
            id += self.x.create()
            return SampleObject(id=id)

        def hello(self, f: Filter, y=Depends(get_y)):
            _id = f.foo
            _id += y
            _id += self.x.create()
            return SampleObject(id=_id)

    app = FastAPI(
        title="A sample application using fastapi_router_controller",
        version="0.1.0",
        openapi_tags=ControllersTags,
    )

    router = APIRouter()
    controller = Controller(router, openapi_tag={"name": "sample_controller"})

    SampleController = controller.add_resource(SampleController)
    controller.route.add_api_route(
        "/",
        SampleController.root,
        tags=["sample_controller"],
        summary="return a sample object",
        response_model=SampleObject,
        methods=["GET"],
    )
    controller.route.add_api_route(
        "/hello", SampleController.hello, response_model=SampleObject, methods=["POST"]
    )
    app.include_router(SampleController.router())
    return app


class TestRoutesDeclerative(unittest.TestCase):
    def setUp(self):
        app = create_app_declerative()
        self.client = TestClient(app)

    def test_root(self):
        response = self.client.get("/?id=12")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "12XXX"})

    def test_hello(self):
        response = self.client.post("/hello", json={"foo": "WOW"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "WOWget_y_depXXX"})


class TestRoutesImperative(unittest.TestCase):
    def setUp(self):
        app = create_app_imperative()
        self.client = TestClient(app)

    def test_root(self):
        response = self.client.get("/?id=12")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "12XXX"})

    def test_hello(self):
        response = self.client.post("/hello", json={"foo": "WOW"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "WOWget_y_depXXX"})
