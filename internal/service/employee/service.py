from opentelemetry.trace import Status, StatusCode, SpanKind
from internal import interface, model, common
from internal.interface.client.loom_tg_bot import ILoomTgBotClient


class EmployeeService(interface.IEmployeeService):
    def __init__(
            self,
            tel: interface.ITelemetry,
            employee_repo: interface.IEmployeeRepo,
            loom_tg_bot_client: ILoomTgBotClient,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.employee_repo = employee_repo
        self.loom_tg_bot_client = loom_tg_bot_client

    async def create_employee(
            self,
            organization_id: int,
            invited_from_account_id: int,
            account_id: int,
            name: str,
            role: str
    ) -> int:
        with self.tracer.start_as_current_span(
                "EmployeeService.create_employee",
                kind=SpanKind.INTERNAL,
                attributes={
                    "organization_id": organization_id,
                    "account_id": account_id,
                    "name": name,
                    "role": role
                }
        ) as span:
            try:
                # Проверяем права пригласившего сотрудника
                if invited_from_account_id != 0:  # 0 означает создание первого админа
                    await self._check_employee_permission(invited_from_account_id, "add_employee_permission")

                required_moderation = False
                autoposting_permission = False
                add_employee_permission = False
                edit_employee_perm_permission = False
                top_up_balance_permission = False
                sign_up_social_net_permission = False

                if role == "admin":
                    required_moderation = False
                    autoposting_permission = True
                    add_employee_permission = True
                    edit_employee_perm_permission = True
                    top_up_balance_permission = True
                    sign_up_social_net_permission = True

                employee_id = await self.employee_repo.create_employee(
                    organization_id=organization_id,
                    invited_from_account_id=invited_from_account_id,
                    account_id=account_id,
                    name=name,
                    role=role,
                    required_moderation=required_moderation,
                    autoposting_permission=autoposting_permission,
                    add_employee_permission=add_employee_permission,
                    edit_employee_perm_permission=edit_employee_perm_permission,
                    top_up_balance_permission=top_up_balance_permission,
                    sign_up_social_net_permission=sign_up_social_net_permission,
                )

                await self.loom_tg_bot_client.notify_employee_added(
                    account_id=account_id,
                    organization_id=organization_id,
                    employee_name=name,
                    role=role,
                )

                span.set_status(Status(StatusCode.OK))
                return employee_id

            except Exception as e:
                
                span.set_status(StatusCode.ERROR, str(e))
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
                
                span.set_status(StatusCode.ERROR, str(e))
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
                
                span.set_status(StatusCode.ERROR, str(e))
                raise

    async def update_employee_permissions(
            self,
            account_id: int,
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
                attributes={"account_id": account_id}
        ) as span:
            try:
                # Проверяем, что сотрудник существует
                employees = await self.employee_repo.get_employee_by_account_id(account_id)
                if not employees:
                    raise common.ErrEmployeeNotFound()

                await self.employee_repo.update_employee_permissions(
                    account_id=account_id,
                    required_moderation=required_moderation,
                    autoposting_permission=autoposting_permission,
                    add_employee_permission=add_employee_permission,
                    edit_employee_perm_permission=edit_employee_perm_permission,
                    top_up_balance_permission=top_up_balance_permission,
                    sign_up_social_net_permission=sign_up_social_net_permission
                )

                span.set_status(Status(StatusCode.OK))

            except Exception as e:
                
                span.set_status(StatusCode.ERROR, str(e))
                raise

    async def update_employee_role(
            self,
            account_id: int,
            role: model.EmployeeRole
    ) -> None:
        with self.tracer.start_as_current_span(
                "EmployeeService.update_employee_role",
                kind=SpanKind.INTERNAL,
                attributes={"account_id": account_id, "role": role.value}
        ) as span:
            try:
                # Проверяем, что сотрудник существует
                employees = await self.employee_repo.get_employee_by_account_id(account_id)
                if not employees:
                    raise common.ErrEmployeeNotFound()

                await self.employee_repo.update_employee_role(
                    account_id=account_id,
                    role=role
                )

                span.set_status(Status(StatusCode.OK))

            except Exception as e:
                
                span.set_status(StatusCode.ERROR, str(e))
                raise

    async def delete_employee(self, account_id: int) -> None:
        with self.tracer.start_as_current_span(
                "EmployeeService.delete_employee",
                kind=SpanKind.INTERNAL,
                attributes={"account_id": account_id}
        ) as span:
            try:
                # Проверяем, что сотрудник существует
                employees = await self.employee_repo.get_employee_by_account_id(account_id)
                if not employees:
                    raise common.ErrEmployeeNotFound()

                await self.employee_repo.delete_employee(account_id)

                span.set_status(Status(StatusCode.OK))

            except Exception as e:
                
                span.set_status(StatusCode.ERROR, str(e))
                raise

    async def check_employee_permission(
            self,
            account_id: int,
            permission_type: str
    ) -> bool:
        with self.tracer.start_as_current_span(
                "EmployeeService.check_employee_permission",
                kind=SpanKind.INTERNAL,
                attributes={"account_id": account_id, "permission_type": permission_type}
        ) as span:
            try:
                return await self._check_employee_permission(account_id, permission_type)

            except Exception as e:
                
                span.set_status(StatusCode.ERROR, str(e))
                raise

    async def _check_employee_permission(
            self,
            account_id: int,
            permission_type: str
    ) -> bool:
        """Внутренний метод для проверки разрешений"""
        employees = await self.employee_repo.get_employee_by_account_id(account_id)
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
            raise common.ErrInsufficientPermissions(f"Employee {account_id} lacks permission: {permission_type}")

        return True
