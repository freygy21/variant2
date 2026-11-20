from app.services.card_service import CardService
from app.support.types import Repository
from app.domain.usage import AllowedCardTypeRule, OnlineUsageRule

def build_service(repository=None, rules=None):
    if repository is None:
        repository = Repository("card_id")

    if rules is None:
        rules = (
            AllowedCardTypeRule({"STANDARD"}),
            OnlineUsageRule(),
        )
    return CardService(repository, rules)
