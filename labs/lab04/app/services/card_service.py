from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError
from app.domain.card import Card
from app.domain.usage import AllowedCardTypeRule, OnlineUsageRule

class CardService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        self._rules = [AllowedCardTypeRule({"STANDARD"}), OnlineUsageRule()]  # конкретные объекты пока создаются здесь

    def register(self, entity):
        return self._repository.add(entity)

    def get(self, key):
        return self._repository.get(key)

    def activate(self, key):
        entity = self.get(key)
        if entity.status not in ('NEW',):
            raise DomainError("INVALID_STATE")
        entity._status = "ACTIVE"

    def block(self, key):
        entity = self.get(key)
        if entity.status not in ('ACTIVE',):
            raise DomainError("INVALID_STATE")
        entity._status = "BLOCKED"

    def unblock(self, key):
        entity = self.get(key)
        if entity.status not in ('BLOCKED',):
            raise DomainError("INVALID_STATE")
        entity._status = "ACTIVE"

    def close(self, key):
        entity = self.get(key)
        if entity.status not in ('NEW', 'ACTIVE', 'BLOCKED'):
            raise DomainError("INVALID_STATE")
        entity._status = "CLOSED"

    def check(self, key, context):
        entity = self.get(key)
        result = entity.availability(context.as_of)
        if not result.allowed:
            return result
        for rule in self._rules:
            result = checked(rule.check(entity, context))
            if not result.allowed:
                return result
        return CheckResult(True)

    def diagnostic(self, key):
        entity = self.get(key)
        return f"{entity.card_id}:{entity.status}:{entity.card_type}"

def make_entity(*args, **kwargs):
    return Card(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'card_id': entity.card_id, 'customer_id': entity.customer_id, 'account_id': entity.account_id, 'expiration_date': entity.expiration_date, 'card_type': entity.card_type, 'online_enabled': entity.online_enabled, 'contactless_enabled': entity.contactless_enabled, 'status': entity.status}


from app.support.types import Repository

def new_service(repository=None):
    return CardService(repository if repository is not None else Repository("card_id"))
