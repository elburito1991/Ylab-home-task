from fastapi import HTTPException, status


class MenuException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class MenuDontExistsException(MenuException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'menu not found'
