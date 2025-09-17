from opentelemetry.trace import Status, StatusCode, SpanKind

from internal import model
from internal import interface
from pkg.client.client import AsyncHTTPClient


class KonturTgBotClient(interface.IKonturTgBotClient):
    def __init__(
            self,
            tel: interface.ITelemetry,
            host: str,
            port: int,
            interserver_secret_key: str,
    ):
        logger = tel.logger()
        self.client = AsyncHTTPClient(
            host,
            port,
            prefix="/api/tg-bot",
            use_tracing=True,
            logger=logger,
        )
        self.tracer = tel.tracer()

        self.interserver_secret_key = interserver_secret_key

    async def notify_employee_added(
            self,
            account_id: int,
            organization_id: int,
            employee_name: str,
            role: str,
    ):
        with self.tracer.start_as_current_span(
                "KonturAuthorizationClient.authorization",
                kind=SpanKind.CLIENT,
                attributes={
                    "account_id": account_id,
                    "organization_id": organization_id,
                    "employee_name": employee_name,
                    "role": role
                }
        ) as span:
            try:
                body = {
                    "account_id": account_id,
                    "organization_id": organization_id,
                    "employee_name": employee_name,
                    "role": role,
                    "interserver_secret_key": self.interserver_secret_key,
                }
                response = await self.client.post("/employee/notify/added", json=body)

                span.set_status(Status(StatusCode.OK))
            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise