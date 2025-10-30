from pydantic import BaseModel
from internal.model.employee import EmployeeRole


class CreateEmployeeBody(BaseModel):
    account_id: int
    organization_id: int
    invited_from_account_id: int
    name: str
    role: str


class UpdateEmployeePermissionsBody(BaseModel):
    account_id: int
    required_moderation: bool = None
    autoposting_permission: bool = None
    add_employee_permission: bool = None
    edit_employee_perm_permission: bool = None
    top_up_balance_permission: bool = None
    sign_up_social_net_permission: bool = None
    setting_category_permission: bool = None
    setting_organization_permission: bool = None


class UpdateEmployeeRoleBody(BaseModel):
    account_id: int
    role: EmployeeRole

# Response models
class CreateEmployeeResponse(BaseModel):
    employee_id: int


class GetEmployeeResponse(BaseModel):
    employee: dict


class GetEmployeesByOrganizationResponse(BaseModel):
    employees: list[dict]
