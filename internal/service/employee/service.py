from internal import interface, model, common
from internal.interface.client.loom_tg_bot import ILoomTgBotClient

from pkg.trace_wrapper import traced_method


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

    @traced_method()
    async def create_employee(
            self,
            organization_id: int,
            invited_from_account_id: int,
            account_id: int,
            name: str,
            role: str
    ) -> int:
        # Проверяем права пригласившего сотрудника
        if invited_from_account_id != 0:  # 0 означает создание первого админа
            self.logger.info("Проверка прав приглашающего сотрудника")
            await self._check_employee_permission(invited_from_account_id, "add_employee_permission")

        required_moderation = False
        autoposting_permission = False
        add_employee_permission = False
        edit_employee_perm_permission = False
        top_up_balance_permission = False
        sign_up_social_net_permission = False

        if role == "admin":
            self.logger.info("Назначение роли администратора")
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

        return employee_id

    @traced_method()
    async def get_employee_by_account_id(self, account_id: int) -> list[model.Employee]:
        employee = await self.employee_repo.get_employee_by_account_id(account_id)

        return employee

    @traced_method()
    async def get_employees_by_organization(self, organization_id: int) -> list[model.Employee]:
        employees = await self.employee_repo.get_employees_by_organization(organization_id)

        return employees

    @traced_method()
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
        employees = await self.employee_repo.get_employee_by_account_id(account_id)
        if not employees:
            self.logger.warning("Сотрудник не найден")
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

    @traced_method()
    async def update_employee_role(
            self,
            account_id: int,
            role: model.EmployeeRole
    ) -> None:
        employees = await self.employee_repo.get_employee_by_account_id(account_id)
        if not employees:
            self.logger.warning("Сотрудник не найден")
            raise common.ErrEmployeeNotFound()

        await self.employee_repo.update_employee_role(
            account_id=account_id,
            role=role
        )

    @traced_method()
    async def delete_employee(self, account_id: int) -> None:
        employees = await self.employee_repo.get_employee_by_account_id(account_id)
        if not employees:
            self.logger.warning("Сотрудник не найден")
            raise common.ErrEmployeeNotFound()

        await self.employee_repo.delete_employee(account_id)

    @traced_method()
    async def check_employee_permission(
            self,
            account_id: int,
            permission_type: str
    ) -> bool:
        return await self._check_employee_permission(account_id, permission_type)

    @traced_method()
    async def _check_employee_permission(
            self,
            account_id: int,
            permission_type: str
    ) -> bool:
        employees = await self.employee_repo.get_employee_by_account_id(account_id)
        if not employees:
            self.logger.warning("Сотрудник не найден")
            raise common.ErrEmployeeNotFound()

        employee = employees[0]

        # Админы имеют все права
        if employee.role == model.EmployeeRole.ADMIN:
            self.logger.info("Сотрудник является администратором")
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
            self.logger.warning("Недостаточно прав")
            raise common.ErrInsufficientPermissions(f"Employee {account_id} lacks permission: {permission_type}")

        return True
