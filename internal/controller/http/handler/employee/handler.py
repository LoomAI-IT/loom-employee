from fastapi import Request
from fastapi.responses import JSONResponse

from internal import interface
from internal.controller.http.handler.employee.model import (
    CreateEmployeeBody, UpdateEmployeePermissionsBody, UpdateEmployeeRoleBody
)
from pkg.log_wrapper import auto_log

from pkg.trace_wrapper import traced_method


class EmployeeController(interface.IEmployeeController):
    def __init__(
            self,
            tel: interface.ITelemetry,
            employee_service: interface.IEmployeeService,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.employee_service = employee_service
    
    @auto_log()
    @traced_method()
    async def create_employee(
            self,
            request: Request,
            body: CreateEmployeeBody
    ) -> JSONResponse:
        employee_id = await self.employee_service.create_employee(
            organization_id=body.organization_id,
            invited_from_account_id=body.invited_from_account_id,
            account_id=body.account_id,
            name=body.name,
            role=body.role
        )

        return JSONResponse(
            status_code=201,
            content={"employee_id": employee_id}
        )

    @auto_log()
    @traced_method()
    async def get_employee_by_account_id(self, request: Request, account_id: int) -> JSONResponse:
        employee = await self.employee_service.get_employee_by_account_id(account_id)
        return JSONResponse(
            status_code=200,
            content=[employee.to_dict() for employee in employee]
        )

    @auto_log()
    @traced_method()
    async def get_employees_by_organization(self, request: Request, organization_id: int) -> JSONResponse:
        employees = await self.employee_service.get_employees_by_organization(organization_id)

        return JSONResponse(
            status_code=200,
            content={"employees": [emp.to_dict() for emp in employees]}
        )

    @auto_log()
    @traced_method()
    async def update_employee_permissions(
            self,
            request: Request,
            body: UpdateEmployeePermissionsBody
    ) -> JSONResponse:
        await self.employee_service.update_employee_permissions(
            account_id=body.account_id,
            required_moderation=body.required_moderation,
            autoposting_permission=body.autoposting_permission,
            add_employee_permission=body.add_employee_permission,
            edit_employee_perm_permission=body.edit_employee_perm_permission,
            top_up_balance_permission=body.top_up_balance_permission,
            sign_up_social_net_permission=body.sign_up_social_net_permission,
            setting_category_permission=body.setting_category_permission,
            setting_organization_permission=body.setting_organization_permission
        )

        return JSONResponse(
            status_code=200,
            content={}
        )

    @auto_log()
    @traced_method()
    async def update_employee_role(
            self,
            request: Request,
            body: UpdateEmployeeRoleBody
    ) -> JSONResponse:
        await self.employee_service.update_employee_role(
            account_id=body.account_id,
            role=body.role
        )
        return JSONResponse(
            status_code=200,
            content={}
        )

    @auto_log()
    @traced_method()
    async def delete_employee(self, request: Request, account_id: int) -> JSONResponse:
        await self.employee_service.delete_employee(account_id)

        return JSONResponse(
            status_code=200,
            content={}
        )
