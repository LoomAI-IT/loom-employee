from opentelemetry.trace import Status, StatusCode, SpanKind
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from internal import interface
from internal.controller.http.handler.employee.model import (
    CreateEmployeeBody, UpdateEmployeePermissionsBody, UpdateEmployeeRoleBody
)


class EmployeeController(interface.IEmployeeController):
    def __init__(
            self,
            tel: interface.ITelemetry,
            employee_service: interface.IEmployeeService,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.employee_service = employee_service

    async def create_employee(
            self,
            request: Request,
            body: CreateEmployeeBody
    ) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "EmployeeController.create_employee",
                kind=SpanKind.INTERNAL,
                attributes={
                    "organization_id": body.organization_id,
                    "name": body.name,
                    "role": body.role
                }
        ) as span:
            try:

                self.logger.info("Create employee request", {
                    "account_id": body.account_id,
                    "organization_id": body.organization_id,
                    "employee_name": body.name,
                    "role": body.role
                })

                employee_id = await self.employee_service.create_employee(
                    organization_id=body.organization_id,
                    invited_from_account_id=body.invited_from_account_id,
                    account_id=body.account_id,
                    name=body.name,
                    role=body.role
                )

                self.logger.info("Employee created successfully", {
                    "account_id": body.account_id,
                    "employee_id": employee_id
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=201,
                    content={
                        "message": "Employee created successfully",
                        "employee_id": employee_id
                    }
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def get_employee_by_id(self, request: Request, employee_id: int) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "EmployeeController.get_employee_by_id",
                kind=SpanKind.INTERNAL,
                attributes={"employee_id": employee_id}
        ) as span:
            try:
                self.logger.info("Get employee by ID request", {
                    "employee_id": employee_id
                })

                employee = await self.employee_service.get_employee_by_id(employee_id)

                self.logger.info("Employee retrieved successfully", {
                    "employee_id": employee_id
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": "Employee retrieved successfully",
                        "employee": employee.to_dict()
                    }
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err


    async def get_employee_by_account_id(self, request: Request, account_id: int) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "EmployeeController.get_employee_by_account_id",
                kind=SpanKind.INTERNAL,
                attributes={"account_id": account_id}
        ) as span:
            try:
                self.logger.info("Get employee by ID request", {
                    "account_id": account_id,
                })

                employee = await self.employee_service.get_employee_by_account_id(account_id)

                self.logger.info("Employee retrieved successfully", {
                    "account_id": account_id,
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=200,
                    content=[employee.to_dict() for employee in employee]
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def get_employees_by_organization(self, request: Request, organization_id: int) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "EmployeeController.get_employees_by_organization",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": organization_id}
        ) as span:
            try:

                self.logger.info("Get employees by organization request", {
                    "organization_id": organization_id
                })

                employees = await self.employee_service.get_employees_by_organization(organization_id)

                self.logger.info("Employees retrieved successfully", {
                    "organization_id": organization_id,
                    "count": len(employees)
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": "Employees retrieved successfully",
                        "employees": [emp.to_dict() for emp in employees]
                    }
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def update_employee_permissions(
            self,
            request: Request,
            body: UpdateEmployeePermissionsBody
    ) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "EmployeeController.update_employee_permissions",
                kind=SpanKind.INTERNAL,
                attributes={"employee_id": body.employee_id}
        ) as span:
            try:

                self.logger.info("Update employee permissions request", {
                    "employee_id": body.employee_id
                })

                await self.employee_service.update_employee_permissions(
                    employee_id=body.employee_id,
                    required_moderation=body.required_moderation,
                    autoposting_permission=body.autoposting_permission,
                    add_employee_permission=body.add_employee_permission,
                    edit_employee_perm_permission=body.edit_employee_perm_permission,
                    top_up_balance_permission=body.top_up_balance_permission,
                    sign_up_social_net_permission=body.sign_up_social_net_permission
                )

                self.logger.info("Employee permissions updated successfully", {
                    "employee_id": body.employee_id
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=200,
                    content={"message": "Employee permissions updated successfully"}
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def update_employee_role(
            self,
            request: Request,
            body: UpdateEmployeeRoleBody
    ) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "EmployeeController.update_employee_role",
                kind=SpanKind.INTERNAL,
                attributes={"employee_id": body.employee_id, "role": body.role.value}
        ) as span:
            try:

                self.logger.info("Update employee role request", {
                    "employee_id": body.employee_id,
                    "role": body.role.value
                })

                await self.employee_service.update_employee_role(
                    employee_id=body.employee_id,
                    role=body.role
                )

                self.logger.info("Employee role updated successfully", {
                    "employee_id": body.employee_id,
                    "role": body.role.value
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=200,
                    content={"message": "Employee role updated successfully"}
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def delete_employee(self, request: Request, employee_id: int) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "EmployeeController.delete_employee",
                kind=SpanKind.INTERNAL,
                attributes={"employee_id": employee_id}
        ) as span:
            try:
                self.logger.info("Delete employee request", {
                    "employee_id": employee_id
                })

                await self.employee_service.delete_employee(employee_id)

                self.logger.info("Employee deleted successfully", {
                    "employee_id": employee_id
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=200,
                    content={"message": "Employee deleted successfully"}
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err