import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_router_controller import Controller, ControllersTags

# just import the main package to load all the controllers in
import controller

app = FastAPI(
    title='A sample application using fastapi_router_controller with controller auto import',
    version="0.1.0",
    # all of the router openapi_tags are collected in ControllerTags object
    openapi_tags=ControllersTags)

for router in Controller.routers():
    app.include_router(router)

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_sample_extended_controller(self):
        response = self.client.get("/sample_extended_controller/?id=1234")
        self.assertEqual(response.status_code, 200)

    def test_get_sample_extended_controller_parent_api(self):
        response = self.client.get("/sample_extended_controller/parent_api")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
