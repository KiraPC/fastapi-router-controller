from fastapi import APIRouter, status, Query, Body
from fastapi_router_controller import Controller
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

router = APIRouter(prefix='/sample_controller_2')

controller = Controller(router, openapi_tag={
    'name': 'sample_controller_2',
})

class SampleObject(BaseModel):
    id: str = Field(..., description='sample id')

# With the "resource" decorator define the controller Class linked to the Controller router arguments 
@controller.resource()
class AnotherSampleController():
    @controller.route.get(
        '/',
        tags=['sample_controller_2'], 
        summary='return another sample object')
    def sample_get_request(_, id: str = Query(..., title="itemId", description="The id of the sample object")):
        return JSONResponse(status_code=status.HTTP_200_OK, content=SampleObject(id))

    @controller.route.post(
        '/', 
        tags=['sample_controller_2'], 
        summary='create a sample object', 
        status_code=201)
    def sample_post_request(_, simple_object: SampleObject = Body(None, title="SampleObject", description="A sample object model")):
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={})
