from fastapi import FastAPI
from starlette.responses import StreamingResponse

from internal import model, interface
from internal.controller.http.handler.employee.model import *


def NewHTTP(
        db: interface.IDB,
        employee_controller: interface.IEmployeeController,
        http_middleware: interface.IHttpMiddleware,
        prefix: str
):
    app = FastAPI(
        title="Employee Service API",
        description="API для управления сотрудниками",
        version="1.0.0",
        openapi_url=prefix + "/openapi.json",
        docs_url=prefix + "/docs",
        redoc_url=prefix + "/redoc",
    )
    include_middleware(app, http_middleware)
    include_db_handler(app, db, prefix)
    include_employee_handlers(app, employee_controller, prefix)

    return app


def include_middleware(
        app: FastAPI,
        http_middleware: interface.IHttpMiddleware,
):
    # Порядок middleware важен - они применяются в обратном порядке регистрации
    http_middleware.authorization_middleware04(app)
    http_middleware.logger_middleware03(app)
    http_middleware.metrics_middleware02(app)
    http_middleware.trace_middleware01(app)


def include_employee_handlers(
        app: FastAPI,
        employee_controller: interface.IEmployeeController,
        prefix: str
):
    # Создание сотрудника
    app.add_api_route(
        prefix + "/employee",
        employee_controller.create_employee,
        methods=["POST"],
        tags=["Employee"],
        response_model=CreateEmployeeResponse,
        summary="Создать сотрудника",
        description="Создает нового сотрудника в организации"
    )

    # Получение сотрудника по ID
    app.add_api_route(
        prefix + "/employee/{employee_id}",
        employee_controller.get_employee_by_id,
        methods=["GET"],
        tags=["Employee"],
        response_model=model.Employee,
        summary="Получить сотрудника по ID",
        description="Возвращает информацию о сотруднике по его идентификатору"
    )

    # Получение сотрудников по организации
    app.add_api_route(
        prefix + "/organization/{organization_id}/employees",
        employee_controller.get_employees_by_organization,
        methods=["GET"],
        tags=["Employee"],
        response_model=list[model.Employee],
        summary="Получить сотрудников организации",
        description="Возвращает список всех сотрудников указанной организации"
    )

    # Обновление прав сотрудника
    app.add_api_route(
        prefix + "/employee/permissions",
        employee_controller.update_employee_permissions,
        methods=["PUT"],
        tags=["Employee"],
        response_model=UpdateEmployeePermissionsResponse,
        summary="Обновить права сотрудника",
        description="Обновляет права доступа сотрудника"
    )

    # Обновление роли сотрудника
    app.add_api_route(
        prefix + "/employee/role",
        employee_controller.update_employee_role,
        methods=["PUT"],
        tags=["Employee"],
        response_model=UpdateEmployeeRoleResponse,
        summary="Обновить роль сотрудника",
        description="Обновляет роль сотрудника в организации"
    )

    # Удаление сотрудника
    app.add_api_route(
        prefix + "/employee/{employee_id}",
        employee_controller.delete_employee,
        methods=["DELETE"],
        tags=["Employee"],
        response_model=DeleteEmployeeResponse,
        summary="Удалить сотрудника",
        description="Удаляет сотрудника из организации"
    )


def include_db_handler(app: FastAPI, db: interface.IDB, prefix: str):
    """
    Добавляет служебные эндпоинты для управления базой данных
    """
    app.add_api_route(
        prefix + "/table/create",
        create_table_handler(db),
        methods=["GET"],
        tags=["Database"],
        summary="Создать таблицы",
        description="Создает все необходимые таблицы в базе данных"
    )

    app.add_api_route(
        prefix + "/table/drop",
        drop_table_handler(db),
        methods=["GET"],
        tags=["Database"],
        summary="Удалить таблицы",
        description="Удаляет все таблицы из базы данных"
    )


def create_table_handler(db: interface.IDB):
    async def create_table():
        try:
            await db.multi_query(model.create_organization_tables_queries)
            return {"message": "Tables created successfully"}
        except Exception as err:
            raise err

    return create_table


def drop_table_handler(db: interface.IDB):
    async def drop_table():
        try:
            await db.multi_query(model.drop_organization_tables_queries)
            return {"message": "Tables dropped successfully"}
        except Exception as err:
            raise err

    return drop_table