from opentelemetry.trace import Status, StatusCode, SpanKind
from internal import interface, model, common




class EmployeeService(interface.IEmployeeService):
    def __init__(
            self,
            tel: interface.ITelemetry,
            employee_repo: interface.IEmployeeRepo,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.employee_repo = employee_repo

    async def create_employee(
            self,
            organization_id: int,
            invited_from_employee_id: int,
            account_id: int,
            name: str,
            role: model.EmployeeRole
    ) -> int:
        with self.tracer.start_as_current_span(
                "EmployeeService.create_employee",
                kind=SpanKind.INTERNAL,
                attributes={
                    "organization_id": organization_id,
                    "account_id": account_id,
                    "name": name,
                    "role": role.value
                }
        ) as span:
            try:
                # Проверяем права пригласившего сотрудника
                if invited_from_employee_id != 0:  # 0 означает создание первого админа
                    await self._check_employee_permission(invited_from_employee_id, "add_employee_permission")

                employee_id = await self.employee_repo.create_employee(
                    organization_id=organization_id,
                    invited_from_employee_id=invited_from_employee_id,
                    account_id=account_id,
                    name=name,
                    role=role
                )

                span.set_status(Status(StatusCode.OK))
                return employee_id

            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise

    async def get_employee_by_id(self, employee_id: int) -> model.Employee:
        with self.tracer.start_as_current_span(
                "EmployeeService.get_employee_by_id",
                kind=SpanKind.INTERNAL,
                attributes={"employee_id": employee_id}
        ) as span:
            try:
                employees = await self.employee_repo.get_employee_by_id(employee_id)
                if not employees:
                    raise common.ErrEmployeeNotFound()

                employee = employees[0]

                span.set_status(Status(StatusCode.OK))
                return employee

            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise


    async def get_employee_by_account_id(self, account_id: int) -> list[model.Employee]:
        with self.tracer.start_as_current_span(
                "EmployeeService.get_employee_by_account_id",
                kind=SpanKind.INTERNAL,
                attributes={"account_id": account_id}
        ) as span:
            try:
                employee = await self.employee_repo.get_employee_by_account_id(account_id)

                span.set_status(Status(StatusCode.OK))
                return employee

            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise

    async def get_employees_by_organization(self, organization_id: int) -> list[model.Employee]:
        with self.tracer.start_as_current_span(
                "EmployeeService.get_employees_by_organization",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": organization_id}
        ) as span:
            try:
                employees = await self.employee_repo.get_employees_by_organization(organization_id)

                span.set_status(Status(StatusCode.OK))
                return employees

            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise

    async def update_employee_permissions(
            self,
            employee_id: int,
            required_moderation: bool = None,
            autoposting_permission: bool = None,
            add_employee_permission: bool = None,
            edit_employee_perm_permission: bool = None,
            top_up_balance_permission: bool = None,
            sign_up_social_net_permission: bool = None
    ) -> None:
        with self.tracer.start_as_current_span(
                "EmployeeService.update_employee_permissions",
                kind=SpanKind.INTERNAL,
                attributes={"employee_id": employee_id}
        ) as span:
            try:
                # Проверяем, что сотрудник существует
                employees = await self.employee_repo.get_employee_by_id(employee_id)
                if not employees:
                    raise common.ErrEmployeeNotFound()

                await self.employee_repo.update_employee_permissions(
                    employee_id=employee_id,
                    required_moderation=required_moderation,
                    autoposting_permission=autoposting_permission,
                    add_employee_permission=add_employee_permission,
                    edit_employee_perm_permission=edit_employee_perm_permission,
                    top_up_balance_permission=top_up_balance_permission,
                    sign_up_social_net_permission=sign_up_social_net_permission
                )

                span.set_status(Status(StatusCode.OK))

            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise

    async def update_employee_role(
            self,
            employee_id: int,
            role: model.EmployeeRole
    ) -> None:
        with self.tracer.start_as_current_span(
                "EmployeeService.update_employee_role",
                kind=SpanKind.INTERNAL,
                attributes={"employee_id": employee_id, "role": role.value}
        ) as span:
            try:
                # Проверяем, что сотрудник существует
                employees = await self.employee_repo.get_employee_by_id(employee_id)
                if not employees:
                    raise common.ErrEmployeeNotFound()

                await self.employee_repo.update_employee_role(
                    employee_id=employee_id,
                    role=role
                )

                span.set_status(Status(StatusCode.OK))

            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise

    async def delete_employee(self, employee_id: int) -> None:
        with self.tracer.start_as_current_span(
                "EmployeeService.delete_employee",
                kind=SpanKind.INTERNAL,
                attributes={"employee_id": employee_id}
        ) as span:
            try:
                # Проверяем, что сотрудник существует
                employees = await self.employee_repo.get_employee_by_id(employee_id)
                if not employees:
                    raise common.ErrEmployeeNotFound()

                await self.employee_repo.delete_employee(employee_id)

                span.set_status(Status(StatusCode.OK))

            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise

    async def check_employee_permission(
            self,
            employee_id: int,
            permission_type: str
    ) -> bool:
        with self.tracer.start_as_current_span(
                "EmployeeService.check_employee_permission",
                kind=SpanKind.INTERNAL,
                attributes={"employee_id": employee_id, "permission_type": permission_type}
        ) as span:
            try:
                return await self._check_employee_permission(employee_id, permission_type)

            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise

    async def _check_employee_permission(
            self,
            employee_id: int,
            permission_type: str
    ) -> bool:
        """Внутренний метод для проверки разрешений"""
        employees = await self.employee_repo.get_employee_by_id(employee_id)
        if not employees:
            raise common.ErrEmployeeNotFound()

        employee = employees[0]

        # Админы имеют все права
        if employee.role == model.EmployeeRole.ADMIN:
            return True

        # Проверяем конкретное разрешение
        permission_map = {
            "required_moderation": employee.required_moderation,
            "autoposting_permission": employee.autoposting_permission,
            "add_employee_permission": employee.add_employee_permission,
            "edit_employee_perm_permission": employee.edit_employee_perm_permission,
            "top_up_balance_permission": employee.top_up_balance_permission,
            "sign_up_social_net_permission": employee.sign_up_social_net_permission,
        }

        has_permission = permission_map.get(permission_type, False)

        if not has_permission:
            raise common.ErrInsufficientPermissions(f"Employee {employee_id} lacks permission: {permission_type}")

        return True