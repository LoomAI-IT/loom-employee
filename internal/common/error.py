class ErrEmployeeNotFound(Exception):
    def __init__(self, message="Employee not found"):
        self.message = message
        super().__init__(self.message)


class ErrInsufficientPermissions(Exception):
    def __init__(self, message="Insufficient permissions"):
        self.message = message
        super().__init__(self.message)
