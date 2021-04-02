import unittest
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

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_sample_controller(self):
        response = self.client.get("/sample_controller/?id=1234")
        self.assertEqual(response.status_code, 200)

    def test_post_sample_controller(self):
        response = self.client.post("/sample_controller/", json={"id": "test"})
        self.assertEqual(response.status_code, 201)

if __name__ == "__main__":
    unittest.main()
