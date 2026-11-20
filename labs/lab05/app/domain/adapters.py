from app.domain.usage import CardUsageRule
from app.support.types import CheckResult

class LegacyAdapter(CardUsageRule):
    def __init__(self, legacy):
        self._legacy = legacy

    def check(self, entity, context):
        if self._legacy.allowed(entity.card_type):
            return CheckResult(True)
        else:
            return CheckResult(False, "CARD_TYPE_DENIED")
