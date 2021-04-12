class MultipleRouterException(Exception):
    def __init__(self):
        super().__init__('Router already used by another Controller')
