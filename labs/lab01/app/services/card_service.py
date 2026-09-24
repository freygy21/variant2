from app.support.types import CheckResult, Repository
from app.domain.card import Card


class CardService:
    def __init__(self, repository, rules=()):
        self._repository = repository

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
        result = entity.availability(context.as_of)

        if not result.allowed:
            return result

        if entity.card_type != "STANDARD":
            return CheckResult(False, "CARD_TYPE_DENIED")

        if context.channel == "ONLINE" and not entity.online_enabled:
            return CheckResult(False, "CARD_ONLINE_DISABLED")

        return CheckResult(True)


def make_entity(
    card_id,
    customer_id,
    account_id,
    expiration_date,
    card_type,
    online_enabled=True,
    contactless_enabled=True,
):
    return Card(
        card_id,
        customer_id,
        account_id,
        expiration_date,
        card_type,
        online_enabled,
        contactless_enabled,
    )


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


def invoke(service, method, *args, **kwargs):
    if not hasattr(service, method):
        raise ValueError(method)

    return getattr(service, method)(*args, **kwargs)


def new_service(repository=None):
    return CardService(
        repository if repository is not None else Repository("card_id")
    )
