# TODO: Rewrite
class GetOutagesError(Exception):
    def __init__(self, err):
        message = f"Error occured while getting outages:\n{err}"
        super().__init__(message)
