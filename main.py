import uvicorn

from infrastructure.pg.pg import PG
from infrastructure.telemetry.telemetry import Telemetry, AlertManager

from pkg.client.internal.kontur_authorization.client import KonturAuthorizationClient
from pkg.client.internal.kontur_tg_bot.client import KonturTgBotClient

from internal.controller.http.middlerware.middleware import HttpMiddleware
from internal.controller.http.handler.employee.handler import EmployeeController

from internal.service.employee.service import EmployeeService
from internal.repo.employee.repo import EmployeeRepo

from internal.app.http.app import NewHTTP
from internal.config.config import Config

cfg = Config()

alert_manager = AlertManager(
    cfg.alert_tg_bot_token,
    cfg.service_name,
    cfg.alert_tg_chat_id,
    cfg.alert_tg_chat_thread_id,
    cfg.grafana_url,
    cfg.monitoring_redis_host,
    cfg.monitoring_redis_port,
    cfg.monitoring_redis_db,
    cfg.monitoring_redis_password,
    cfg.openai_api_key
)

tel = Telemetry(
    cfg.log_level,
    cfg.root_path,
    cfg.environment,
    cfg.service_name,
    cfg.service_version,
    cfg.otlp_host,
    cfg.otlp_port,
    alert_manager
)

# Инициализация клиентов
db = PG(tel, cfg.db_user, cfg.db_pass, cfg.db_host, cfg.db_port, cfg.db_name)

# Инициализация внешних клиентов
kontur_authorization_client = KonturAuthorizationClient(
    tel=tel,
    host=cfg.kontur_authorization_host,
    port=cfg.kontur_authorization_port,
)

kontur_tg_bot_client = KonturTgBotClient(
    tel=tel,
    host=cfg.kontur_tg_bot_host,
    port=cfg.kontur_tg_bot_port,
    interserver_secret_key=cfg.interserver_secret_key
)

# Инициализация репозиториев
employee_repo = EmployeeRepo(tel, db)

# Инициализация сервисов
employee_service = EmployeeService(
    tel=tel,
    employee_repo=employee_repo,
    kontur_tg_bot_client=kontur_tg_bot_client
)

# Инициализация контроллеров
employee_controller = EmployeeController(tel, employee_service)

# Инициализация middleware
http_middleware = HttpMiddleware(tel, kontur_authorization_client, cfg.prefix)

if __name__ == "__main__":
    app = NewHTTP(
        db=db,
        employee_controller=employee_controller,
        http_middleware=http_middleware,
        prefix=cfg.prefix,
    )
    uvicorn.run(app, host="0.0.0.0", port=int(cfg.http_port), access_log=False)
