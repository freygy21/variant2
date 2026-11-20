from app.services.card_service import CardService
from app.support.types import Repository
from app.domain.usage import AllowedCardTypeRule, OnlineUsageRule

def build_service(repository=None, rules=None):
    repository = repository if repository is not None else Repository("card_id")
    rules = (AllowedCardTypeRule({"STANDARD"}), OnlineUsageRule()) if rules is None else rules
    return CardService(repository, rules)
