from .sql_query import *
from internal import interface, model

from pkg.trace_wrapper import traced_method


class EmployeeRepo(interface.IEmployeeRepo):
    def __init__(
            self,
            tel: interface.ITelemetry,
            db: interface.IDB,
    ):
        self.tracer = tel.tracer()
        self.db = db

    @traced_method()
    async def create_employee(
            self,
            organization_id: int,
            invited_from_account_id: int,
            account_id: int,
            name: str,
            role: str,
            required_moderation: bool = False,
            autoposting_permission: bool = False,
            add_employee_permission: bool = False,
            edit_employee_perm_permission: bool = False,
            top_up_balance_permission: bool = False,
            sign_up_social_net_permission: bool = False,
    ) -> int:
        args = {
            'organization_id': organization_id,
            'invited_from_account_id': invited_from_account_id,
            'account_id': account_id,
            'name': name,
            'role': role,
            'required_moderation': required_moderation,
            'autoposting_permission': autoposting_permission,
            'add_employee_permission': add_employee_permission,
            'edit_employee_perm_permission': edit_employee_perm_permission,
            'top_up_balance_permission': top_up_balance_permission,
            'sign_up_social_net_permission': sign_up_social_net_permission,
        }

        employee_id = await self.db.insert(create_employee, args)

        return employee_id

    @traced_method()
    async def get_employee_by_account_id(self, account_id: int) -> list[model.Employee]:
        args = {'account_id': account_id}
        rows = await self.db.select(get_employee_by_account_id, args)
        employees = model.Employee.serialize(rows) if rows else []

        return employees

    @traced_method()
    async def get_employees_by_organization(self, organization_id: int) -> list[model.Employee]:
        args = {'organization_id': organization_id}
        rows = await self.db.select(get_employees_by_organization, args)
        employees = model.Employee.serialize(rows) if rows else []

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
        update_fields = []
        args: dict = {'account_id': account_id}

        if required_moderation is not None:
            update_fields.append("required_moderation = :required_moderation")
            args['required_moderation'] = required_moderation

        if autoposting_permission is not None:
            update_fields.append("autoposting_permission = :autoposting_permission")
            args['autoposting_permission'] = autoposting_permission

        if add_employee_permission is not None:
            update_fields.append("add_employee_permission = :add_employee_permission")
            args['add_employee_permission'] = add_employee_permission

        if edit_employee_perm_permission is not None:
            update_fields.append("edit_employee_perm_permission = :edit_employee_perm_permission")
            args['edit_employee_perm_permission'] = edit_employee_perm_permission

        if top_up_balance_permission is not None:
            update_fields.append("top_up_balance_permission = :top_up_balance_permission")
            args['top_up_balance_permission'] = top_up_balance_permission

        if sign_up_social_net_permission is not None:
            update_fields.append("sign_up_social_net_permission = :sign_up_social_net_permission")
            args['sign_up_social_net_permission'] = sign_up_social_net_permission

        if not update_fields:
            return

        # Формируем финальный запрос
        query = f"""
                UPDATE employees 
                SET {', '.join(update_fields)}
                WHERE account_id = :account_id;
                """

        await self.db.update(query, args)

    @traced_method()
    async def update_employee_role(
            self,
            account_id: int,
            role: model.EmployeeRole
    ) -> None:
        args = {
            'account_id': account_id,
            'role': role.value
        }
        await self.db.update(update_employee_role, args)

    @traced_method()
    async def delete_employee(self, account_id: int) -> None:
        args = {'account_id': account_id}
        await self.db.update(delete_employee, args)
