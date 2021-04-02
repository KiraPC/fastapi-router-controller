import inspect
from fastapi import APIRouter, Depends

OPEN_API_TAGS = []
__app_controllers__ = []
__router_params__ = [
        'response_model',
        'status_code',
        'tags',
        'dependencies',
        'summary',
        'description',
        'response_description',
        'responses',
        'deprecated',
        'methods',
        'operation_id',
        'response_model_include',
        'response_model_exclude',
        'response_model_by_alias',
        'response_model_exclude_unset',
        'response_model_exclude_defaults',
        'response_model_exclude_none',
        'include_in_schema',
        'response_class',
        'name',
        'callbacks'
    ]

class Controller():
    '''
        The Controller class.

        It expose some utilities and decorator functions to define a router controller class
    '''
    RC_KEY = '__router__'
    SIGNATURE_KEY = '__signature__'

    def __init__(self, router: APIRouter, openapi_tag: dict = None) -> None:
        '''
            :param router:          The FastApi router to link to the Class
            :param openapi_tag:     An openapi object that will describe your routes in the openapi tamplate 
        '''
        self.router = router
        self.openapi_tag = openapi_tag

        if openapi_tag:
            OPEN_API_TAGS.append(openapi_tag)
    
    def __get_parent_routes(self, router: APIRouter):
        '''
            Private utility to get routes from an extended class
        '''
        for route in router.routes:
            options = {key: getattr(route, key) for key in __router_params__}

            # inherits child tags if presents
            if len(options['tags']) == 0 and self.openapi_tag:
                options['tags'].append(self.openapi_tag['name'])

            self.router.add_api_route(route.path, route.endpoint, **options)

    def resource(self):
        '''
            A decorator function to mark a Class as a Controller
        '''
        def wrapper(cls):
            # check if cls was extended from another Controller
            if hasattr(cls, Controller.RC_KEY):
                self.__get_parent_routes(cls.__router__)
            
            cls.__router__ = self.router
            cls.router = lambda: Controller.__parse_controller_router(cls)
            return cls

        return wrapper

    def use(_):
        '''
            A decorator function to mark a Class to be automatically loaded by the Controller
        '''
        def wrapper(cls):
            __app_controllers__.append(cls)
            return cls

        return wrapper

    @staticmethod
    def __parse_controller_router(cls):
        '''
            Private utility to parse the router controller property and extract the correct functions handlers
        '''
        router = getattr(cls, Controller.RC_KEY)

        for route in router.routes:
            # get the signature of the endpoint function
            signature = inspect.signature(route.endpoint)
            # get the parameters of the endpoint function
            signature_parameters = list(signature.parameters.values())

            # replace the class instance with the itself FastApi Dependecy
            signature_parameters[0] = signature_parameters[0].replace(default=Depends(cls))
            new_signature = signature.replace(parameters=signature_parameters)
            setattr(route.endpoint, Controller.SIGNATURE_KEY, new_signature)
        
        return router

    @staticmethod
    def routers():
        '''
            It returns all the Classes marked to be used by the "use" decorator
        '''
        routers = []

        for app_controller in __app_controllers__:
            routers.append(
                app_controller.router()
            )
        
        return routers
    
    @property
    def route(self) -> APIRouter:
        '''
            It returns the FastAPI router.
            Use it as if you are using the original one.
        '''
        return self.router
