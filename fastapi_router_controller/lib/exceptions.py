class MultipleRouterException(Exception):
    def __init__(self):
        super().__init__("Router already used by another Controller")


class MultipleResourceException(Exception):
    def __init__(self):
        super().__init__("Controller already used by another Resource")
