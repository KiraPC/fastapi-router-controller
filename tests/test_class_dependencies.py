import unittest
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from fastapi_router_controller import Controller
from fastapi.testclient import TestClient


router = APIRouter()
controller = Controller(router, openapi_tag={"name": "sample_controller"})


def user_exists(user_id: int):
    if user_id <= 5:
        raise HTTPException(status_code=400, detail="No User")


def user_is_id(user_id: int):
    if user_id == 6:
        raise HTTPException(status_code=400, detail="Not exact user")


@controller.resource()
class User:
    dependencies = [Depends(user_exists)]

    @controller.route.get("/users/{user_id}", dependencies=[Depends(user_is_id)])
    def read_users(self, user_id: int):
        return {"user_id": user_id}


def create_app():
    app = FastAPI()

    app.include_router(User.router())
    return app


class TestRoutes(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.client = TestClient(app)

    def test_class_dep(self):
        response = self.client.get("/users/1")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "No User"})

    def test_func_dep(self):
        response = self.client.get("/users/6")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Not exact user"})

    def test_pass(self):
        response = self.client.get("/users/7")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"user_id": 7})
