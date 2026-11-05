from abc import ABC, abstractmethod
from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError

class CardUsageRule(ABC):
    @abstractmethod
    def check(self, entity, context):
        raise NotImplementedError

class AllowedCardTypeRule(CardUsageRule):
    def __init__(self, values):
        self._values = frozenset(values)
        for value in self._values:
            choice(value, ('STANDARD', 'VIRTUAL'), "INVALID_CONFIG")

    def check(self, entity, context):
        if entity.card_type not in self._values:
            return CheckResult(False, 'CARD_TYPE_DENIED')
        return CheckResult(True)

class OnlineUsageRule(CardUsageRule):
    def __init__(self):
        self._channel = "ONLINE"

    def check(self, entity, context):
        if context.channel == self._channel and not entity.online_enabled:
            return CheckResult(False, 'CARD_ONLINE_DISABLED')
        return CheckResult(True)
