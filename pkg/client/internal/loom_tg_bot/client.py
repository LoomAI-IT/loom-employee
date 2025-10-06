from contextvars import ContextVar

from opentelemetry.trace import SpanKind

from internal import interface
from pkg.client.client import AsyncHTTPClient
from pkg.trace_wrapper import traced_method


class LoomTgBotClient(interface.ILoomTgBotClient):
    def __init__(
            self,
            tel: interface.ITelemetry,
            host: str,
            port: int,
            interserver_secret_key: str,
            log_context: ContextVar[dict],
    ):
        logger = tel.logger()
        self.client = AsyncHTTPClient(
            host,
            port,
            prefix="/api/tg-bot",
            use_tracing=True,
            logger=logger,
            log_context=log_context
        )
        self.tracer = tel.tracer()

        self.interserver_secret_key = interserver_secret_key

    @traced_method(SpanKind.CLIENT)
    async def notify_employee_added(
            self,
            account_id: int,
            organization_id: int,
            employee_name: str,
            role: str,
    ):
        body = {
            "account_id": account_id,
            "organization_id": organization_id,
            "employee_name": employee_name,
            "role": role,
            "interserver_secret_key": self.interserver_secret_key,
        }
        response = await self.client.post("/employee/notify/added", json=body)
