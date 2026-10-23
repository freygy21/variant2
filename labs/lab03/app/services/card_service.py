from app.domain.card import Card
from app.domain.usage import AllowedCardTypeRule, OnlineUsageRule, ContactlessUsageRule
from app.support.types import CheckResult, Repository
from app.support.errors import DomainError


class CardService:
    def __init__(self, repository, rules=()):
        self._repository = repository

        if rules:
            self._rules = list(rules)
        else:
            self._rules = [
                AllowedCardTypeRule({"STANDARD"}),
                OnlineUsageRule(),
                ContactlessUsageRule(),
            ]

    def register(self, entity):
        return self._repository.add(entity)

    def get(self, key):
        return self._repository.get(key)

    def activate(self, key):
        self.get(key).activate()

    def block(self, key):
        self.get(key).block()

    def unblock(self, key):
        self.get(key).unblock()

    def close(self, key):
        self.get(key).close()

    def check(self, key, context):
        entity = self.get(key)

        availability = entity.availability(context.as_of)

        if not availability.allowed:
            return availability

        for rule in self._rules:
            result = rule.check(entity, context)

            if not isinstance(result, CheckResult):
                raise DomainError("INVALID_RESULT")

            if not result.allowed:
                return result

        return CheckResult(True)


def make_entity(*args, **kwargs):
    return Card(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {
        "card_id": entity.card_id,
        "customer_id": entity.customer_id,
        "account_id": entity.account_id,
        "expiration_date": entity.expiration_date,
        "card_type": entity.card_type,
        "online_enabled": entity.online_enabled,
        "contactless_enabled": entity.contactless_enabled,
        "status": entity.status,
    }


def new_service(repository=None):
    return CardService(
        repository if repository is not None
        else Repository("card_id")
    )
