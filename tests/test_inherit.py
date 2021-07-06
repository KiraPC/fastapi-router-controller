import unittest

from pydantic import BaseModel
from fastapi_router_controller import Controller, ControllersTags
from fastapi import APIRouter, Depends, FastAPI, Query
from fastapi.testclient import TestClient

parent_router = APIRouter()
child_router = APIRouter()

parent_controller = Controller(parent_router, openapi_tag={"name": "parent"})
child_controller = Controller(child_router, openapi_tag={"name": "child"})


class Object(BaseModel):
    id: str


def get_x():
    class Foo:
        def create(self):
            return "XXX"

    return Foo()


class Filter(BaseModel):
    foo: str


@parent_controller.resource()
class Base:
    def __init__(self):
        self.bla = "foo"

    @parent_controller.route.get(
        "/hambu",
        tags=["parent"],
        response_model=Object,
    )
    def hambu(self):
        return Object(id="hambu-%s" % self.bla)


# With the 'resource' decorator define the controller
# Class linked to the Controller router arguments
@child_controller.resource()
class Controller(Base):
    def __init__(self, x=Depends(get_x)):
        super().__init__()
        self.x = x

    @child_controller.route.get(
        "/",
        tags=["child"],
        summary="return a  object",
        response_model=Object,
    )
    def root(
        self,
        id: str = Query(..., title="itemId", description="The id of the  object"),
    ):
        id += self.x.create() + self.bla
        return Object(id=id)


def create_app():
    app = FastAPI(
        title="A application using fastapi_router_controller",
        version="0.1.0",
        openapi_tags=ControllersTags,
    )

    app.include_router(Controller.router())
    return app


class TestRoutes(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.client = TestClient(app)

    def test_root(self):
        response = self.client.get("/?id=12")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "12XXXfoo"})

    def test_child1(self):
        response = self.client.get("/hambu")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "hambu-foo"})


class TestInvalid(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(Exception) as ex:

            @parent_controller.resource()
            class Controller2(Base):
                ...

        self.assertEqual(
            str(ex.exception), "Controller already used by another Resource"
        )
