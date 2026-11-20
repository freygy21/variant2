from app.support.types import CheckResult, CardContext, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError
from app.domain.card import Card
from app.domain.usage import AllowedCardTypeRule, OnlineUsageRule

class CardService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        self._rules = tuple(rules)

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
        card = self.get(key)
        availability = checked(card.availability(context.as_of))
        if not availability.allowed:
            return availability
        for rule in self._rules:
            result = checked(rule.check(card, context))
            if not result.allowed:
                return result
        return CheckResult(True)

    def check_dates(self, card_id, dates):
        results = []

        for as_of in dates:
            context = CardContext(as_of)
            result = self.check(card_id, context)
            results.append((as_of, result))

        return tuple(results)

    def allowed_dates(self, card_id, dates):
        allowed = []

        for as_of, result in self.check_dates(card_id, dates):
            if result.allowed:
                allowed.append(as_of)

        return tuple(allowed)

def make_entity(*args, **kwargs):
    return Card(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'card_id': entity.card_id, 'customer_id': entity.customer_id, 'account_id': entity.account_id, 'expiration_date': entity.expiration_date, 'card_type': entity.card_type, 'online_enabled': entity.online_enabled, 'contactless_enabled': entity.contactless_enabled, 'status': entity.status}
