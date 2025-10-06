from fastapi import Request
from fastapi.responses import JSONResponse

from internal import interface
from internal.controller.http.handler.employee.model import (
    CreateEmployeeBody, UpdateEmployeePermissionsBody, UpdateEmployeeRoleBody
)

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

    @traced_method()
    async def create_employee(
            self,
            request: Request,
            body: CreateEmployeeBody
    ) -> JSONResponse:
        self.logger.info("Начало создания сотрудника")

        employee_id = await self.employee_service.create_employee(
            organization_id=body.organization_id,
            invited_from_account_id=body.invited_from_account_id,
            account_id=body.account_id,
            name=body.name,
            role=body.role
        )

        self.logger.info("Создание сотрудника завершено")
        return JSONResponse(
            status_code=201,
            content={"employee_id": employee_id}
        )

    @traced_method()
    async def get_employee_by_account_id(self, request: Request, account_id: int) -> JSONResponse:
        self.logger.info("Начало получения сотрудника по ID аккаунта")

        employee = await self.employee_service.get_employee_by_account_id(account_id)

        self.logger.info("Получение сотрудника завершено")
        return JSONResponse(
            status_code=200,
            content=[employee.to_dict() for employee in employee]
        )

    @traced_method()
    async def get_employees_by_organization(self, request: Request, organization_id: int) -> JSONResponse:
        self.logger.info("Начало получения сотрудников организации")

        employees = await self.employee_service.get_employees_by_organization(organization_id)

        self.logger.info("Получение сотрудников завершено")

        return JSONResponse(
            status_code=200,
            content={"employees": [emp.to_dict() for emp in employees]}
        )

    @traced_method()
    async def update_employee_permissions(
            self,
            request: Request,
            body: UpdateEmployeePermissionsBody
    ) -> JSONResponse:
        self.logger.info("Начало обновления прав сотрудника")

        await self.employee_service.update_employee_permissions(
            account_id=body.account_id,
            required_moderation=body.required_moderation,
            autoposting_permission=body.autoposting_permission,
            add_employee_permission=body.add_employee_permission,
            edit_employee_perm_permission=body.edit_employee_perm_permission,
            top_up_balance_permission=body.top_up_balance_permission,
            sign_up_social_net_permission=body.sign_up_social_net_permission
        )

        self.logger.info("Обновление прав сотрудника завершено")
        return JSONResponse(
            status_code=200,
            content={}
        )

    @traced_method()
    async def update_employee_role(
            self,
            request: Request,
            body: UpdateEmployeeRoleBody
    ) -> JSONResponse:
        self.logger.info("Начало обновления роли сотрудника")

        await self.employee_service.update_employee_role(
            account_id=body.account_id,
            role=body.role
        )

        self.logger.info("Обновление роли сотрудника завершено")
        return JSONResponse(
            status_code=200,
            content={}
        )

    @traced_method()
    async def delete_employee(self, request: Request, account_id: int) -> JSONResponse:
        self.logger.info("Начало удаления сотрудника")

        await self.employee_service.delete_employee(account_id)

        self.logger.info("Удаление сотрудника завершено")

        return JSONResponse(
            status_code=200,
            content={}
        )
