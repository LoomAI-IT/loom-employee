from opentelemetry.trace import Status, StatusCode, SpanKind
from .sql_query import *
from internal import interface, model, common


class EmployeeRepo(interface.IEmployeeRepo):
    def __init__(
            self,
            tel: interface.ITelemetry,
            db: interface.IDB,
    ):
        self.tracer = tel.tracer()
        self.db = db

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
        with self.tracer.start_as_current_span(
                "EmployeeRepo.create_employee",
                kind=SpanKind.INTERNAL,
                attributes={
                    "organization_id": organization_id,
                    "account_id": account_id,
                    "name": name,
                    "role": role
                }
        ) as span:
            try:
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

                span.set_status(Status(StatusCode.OK))
                return employee_id
            except Exception as err:
                
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def get_employee_by_account_id(self, account_id: int) -> list[model.Employee]:
        with self.tracer.start_as_current_span(
                "EmployeeRepo.get_employee_by_account_id",
                kind=SpanKind.INTERNAL,
                attributes={"account_id": account_id}
        ) as span:
            try:
                args = {'account_id': account_id}
                rows = await self.db.select(get_employee_by_account_id, args)
                employees = model.Employee.serialize(rows) if rows else []

                span.set_status(Status(StatusCode.OK))
                return employees
            except Exception as err:
                
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def get_employees_by_organization(self, organization_id: int) -> list[model.Employee]:
        with self.tracer.start_as_current_span(
                "EmployeeRepo.get_employees_by_organization",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": organization_id}
        ) as span:
            try:
                args = {'organization_id': organization_id}
                rows = await self.db.select(get_employees_by_organization, args)
                employees = model.Employee.serialize(rows) if rows else []

                span.set_status(Status(StatusCode.OK))
                return employees
            except Exception as err:
                
                span.set_status(StatusCode.ERROR, str(err))
                raise err

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
                "EmployeeRepo.update_employee_permissions",
                kind=SpanKind.INTERNAL,
                attributes={"account_id": account_id}
        ) as span:
            try:
                # Формируем запрос динамически в зависимости от переданных параметров
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
                    # Если нет полей для обновления, просто возвращаемся
                    span.set_status(Status(StatusCode.OK))
                    return

                # Формируем финальный запрос
                query = f"""
                UPDATE employees 
                SET {', '.join(update_fields)}
                WHERE account_id = :account_id;
                """

                await self.db.update(query, args)

                span.set_status(Status(StatusCode.OK))
            except Exception as err:
                
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def update_employee_role(
            self,
            account_id: int,
            role: model.EmployeeRole
    ) -> None:
        with self.tracer.start_as_current_span(
                "EmployeeRepo.update_employee_role",
                kind=SpanKind.INTERNAL,
                attributes={"account_id": account_id, "role": role.value}
        ) as span:
            try:
                args = {
                    'account_id': account_id,
                    'role': role.value
                }
                await self.db.update(update_employee_role, args)

                span.set_status(Status(StatusCode.OK))
            except Exception as err:
                
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def delete_employee(self, account_id: int) -> None:
        with self.tracer.start_as_current_span(
                "EmployeeRepo.delete_employee",
                kind=SpanKind.INTERNAL,
                attributes={"account_id": account_id}
        ) as span:
            try:
                args = {'account_id': account_id}
                await self.db.update(delete_employee, args)

                span.set_status(Status(StatusCode.OK))
            except Exception as err:
                
                span.set_status(StatusCode.ERROR, str(err))
                raise err
