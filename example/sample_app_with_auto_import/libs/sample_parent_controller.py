from fastapi import APIRouter, status
from fastapi_router_controller import Controller
from fastapi.responses import JSONResponse

router = APIRouter()

controller = Controller(router)


# This is a Sample Controller that can be exteded by another to inherit its routes
@controller.resource()
class SampleParentController:
    @controller.route.get(
        "/parent_api",
        summary="A sample API from the extended class,"
        + "it will inherit the basepat of the child router",
    )
    def sample_parent_api(_):
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "I'm the parent"}
        )
