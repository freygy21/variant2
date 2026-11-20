from app.domain.usage import CardUsageRule
from app.support.types import CheckResult

class LegacyAdapter(CardUsageRule):
    def __init__(self, legacy):
        self._legacy = legacy

    def check(self, entity, context):
        raise NotImplementedError("Бонус: локальный адаптер")
