from abc import ABC, abstractmethod

from app.support.types import CheckResult


class CardUsageRule(ABC):
    @abstractmethod
    def check(self, entity, context):
        """Проверяет, разрешено ли использование карты."""
        raise NotImplementedError


class AllowedCardTypeRule(CardUsageRule):
    def __init__(self, types):
        self._types = frozenset(types)

    def check(self, entity, context):
        if entity.card_type not in self._types:
            return CheckResult(False, "CARD_TYPE_DENIED")
        return CheckResult(True)


class OnlineUsageRule(CardUsageRule):
    def __init__(self, denied_channel="ONLINE"):
        self._denied_channel = denied_channel

    def check(self, entity, context):
        if (
            context.channel == self._denied_channel
            and not entity.online_enabled
        ):
            return CheckResult(False, "CARD_ONLINE_DISABLED")
        return CheckResult(True)


class ContactlessUsageRule(CardUsageRule):
    def check(self, entity, context):
        if context.contactless and not entity.contactless_enabled:
            return CheckResult(False, "CARD_CONTACTLESS_DISABLED")
        return CheckResult(True)
