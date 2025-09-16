from pydantic import BaseModel
from typing import Optional
from internal.model.employee import EmployeeRole


class CreateEmployeeBody(BaseModel):
    account_id: int
    organization_id: int
    invited_from_account_id: int
    name: str
    role: str

    class Config:
        json_schema_extra = {
            "example": {
                "organization_id": 1,
                "invited_from_account_id": 1,
                "name": "John Doe",
                "role": "сотрудник"
            }
        }


class UpdateEmployeePermissionsBody(BaseModel):
    employee_id: int
    required_moderation: Optional[bool] = None
    autoposting_permission: Optional[bool] = None
    add_employee_permission: Optional[bool] = None
    edit_employee_perm_permission: Optional[bool] = None
    top_up_balance_permission: Optional[bool] = None
    sign_up_social_net_permission: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": 1,
                "required_moderation": False,
                "autoposting_permission": True,
                "add_employee_permission": False,
                "edit_employee_perm_permission": False,
                "top_up_balance_permission": False,
                "sign_up_social_net_permission": True
            }
        }


class UpdateEmployeeRoleBody(BaseModel):
    employee_id: int
    role: EmployeeRole

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": 1,
                "role": "модератор"
            }
        }


# Response models
class CreateEmployeeResponse(BaseModel):
    message: str
    employee_id: int


class GetEmployeeResponse(BaseModel):
    message: str
    employee: dict


class GetEmployeesByOrganizationResponse(BaseModel):
    message: str
    employees: list[dict]


class UpdateEmployeePermissionsResponse(BaseModel):
    message: str


class UpdateEmployeeRoleResponse(BaseModel):
    message: str


class DeleteEmployeeResponse(BaseModel):
    message: str