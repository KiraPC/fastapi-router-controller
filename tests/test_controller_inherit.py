import unittest

from pydantic import BaseModel
from fastapi_router_controller import Controller, ControllersTags
from fastapi import APIRouter, Depends, FastAPI, Query
from fastapi.testclient import TestClient

router = APIRouter()
controller = Controller(router, openapi_tag={"name": "controller"})


class Object(BaseModel):
    id: str


def get_x():
    class Foo:
        def create(self):
            return "XXX"

    return Foo()


def get_bla():
    try:
        yield "get_bla_dep"
    finally:
        print("get_bla done")


class Filter(BaseModel):
    foo: str


# XXX if we set this the test will hang
@controller.resource()
class Base:
    def __init__(self, bla=Depends(get_bla)):
        self.bla = "foo"

    @controller.route.get(
        "/hambu", response_model=Object,
    )
    def hambu(self):
        return Object(id="hambu-%s" % self.bla)


# With the 'resource' decorator define the controller Class linked to the Controller router arguments
@controller.resource()
class Controller(Base):
    def __init__(self, x=Depends(get_x)):
        super().__init__()
        self.x = x

    @controller.route.get(
        "/", tags=["_controller"], summary="return a  object", response_model=Object,
    )
    def root(
        self, id: str = Query(..., title="itemId", description="The id of the  object"),
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

    def test_hambu(self):
        response = self.client.get("/hambu")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "hambu-foo"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(create_app(), host="0.0.0.0", port=9090)
