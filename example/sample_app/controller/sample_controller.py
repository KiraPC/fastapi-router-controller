from fastapi import APIRouter, status, Query, Body, Depends
from fastapi_router_controller import Controller
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

router = APIRouter(prefix='/sample_controller')

controller = Controller(router, openapi_tag={
    'name': 'sample_controller',
})

new_controller = Controller(router, openapi_tag={
    'name': 'sample_controller',
})

class SampleObject(BaseModel):
    id: str = Field(..., description='sample id')

    def to_json(self):
        return {'id': self.id}

class Foo():
    def create_foo(_, item):
        print('Created Foo', str(item))

def get_foo():
    return Foo()

# With the "resource" decorator define the controller Class linked to the Controller router arguments 
@controller.resource()
class SampleController():
    def __init__(self, foo: Foo = Depends(get_foo)):
        self.foo = foo

    @controller.route.get(
        '/',
        tags=['sample_controller'], 
        summary='return a sample object')
    def sample_get_request(self, id: str = Query(..., title="itemId", description="The id of the sample object")):
        return JSONResponse(status_code=status.HTTP_200_OK, content=SampleObject(**{'id': id}).to_json())

    @controller.route.post(
        '/', 
        tags=['sample_controller'], 
        summary='create another sample object', 
        status_code=201)
    def sample_post_request(self, simple_object: SampleObject = Body({}, title="SampleObject", description="A sample object model")):
        self.foo.create_foo(simple_object)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={})
