from abc import abstractmethod
from typing import Protocol

from internal import model


class ILoomTgBotClient(Protocol):
    @abstractmethod
    async def notify_employee_added(
            self,
            account_id: int,
            organization_id: int,
            employee_name: str,
            role: str,
    ): pass