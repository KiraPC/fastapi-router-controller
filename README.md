# fastapi-router-controller

[![Build](https://github.com/KiraPC/fastapi-router-controller/workflows/fastapi-router-controller/badge.svg)](https://github.com/KiraPC/fastapi-router-controller)
[![PyPI version fury.io](https://badge.fury.io/py/fastapi-router-controller.svg)](https://pypi.python.org/pypi/fastapi-router-controller)

#### A FastAPI utility to allow Controller Class usage

## Installation: 

install the package
```
pip install fastapi-router-controller
```

## How to use

Here we see a Fastapi CBV (class based view) application
with class wide Basic Auth dependencies.

```python
import uvicorn

from pydantic import BaseModel
from fastapi_router_controller import Controller
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter()
controller = Controller(router)
security = HTTPBasic()


def verify_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = credentials.username == "john"
    correct_password = credentials.password == "silver"
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect auth",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


class Foo(BaseModel):
    bar: str = "wow"


async def amazing_fn():
    return Foo(bar="amazing_variable")


@controller.resource()
class ExampleController:

    # add class wide dependencies e.g. auth
    dependencies = [Depends(verify_auth)]

    # you can define in the Controller init some FastApi Dependency and them are automatically loaded in controller methods
    def __init__(self, x: Foo = Depends(amazing_fn)):
        self.x = x

    @controller.route.get(
        "/some_api", summary="A sample description", response_model=Foo
    )
    def sample_api(self):
        print(self.x.bar)  # -> amazing_variable
        return self.x


# Load the controller to the main FastAPI app

app = FastAPI(
    title="A sample application using fastapi_router_controller", version="0.1.0"
)

app.include_router(ExampleController.router())

uvicorn.run(app, host="0.0.0.0", port=9090)
```

### Screenshot

All you expect from Fastapi

![Swagger UI](./swagger_ui.png?raw=true)

Also the login dialog

![Swagger UI Login](./swagger_ui_basic_auth.png?raw=true)


## For some Example use-cases visit the example folder
