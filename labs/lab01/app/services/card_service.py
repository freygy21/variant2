# ЛР1: заготовленный сервис. Допишите отмеченный метод и подключите объекты.
from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository


from app.support.types import name as valid_name, country as valid_country


from app.support.errors import DomainError


from app.domain.card import Card


class CardService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        pass

    def register(self, entity):
        return self._repository.add(entity)

    def get(self, key):
        return self._repository.get(key)

    def activate(self, key):
        self.get(key).activate()

    def block(self, key):
        raise NotImplementedError("ЛР1: завершите CardService.block")

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


from app.support.types import Repository


# Ниже — прежний рабочий путь. Перенесите поведение, затем обновите
# make_entity, invoke, view и new_service: сигнатуры должны сохраниться.
from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError

def make_entity(card_id, customer_id, account_id, expiration_date, card_type, online_enabled=True, contactless_enabled=True):
    return {'card_id': card_id, 'customer_id': customer_id, 'account_id': account_id, 'expiration_date': expiration_date, 'card_type': card_type, 'online_enabled': online_enabled, 'contactless_enabled': contactless_enabled, "status": "NEW"}

def _new_legacy_service(repository):
    return {"repository": repository}

def view(entity):
    return dict(entity)

def invoke(service, method, *args, **kwargs):
    repository = service["repository"]
    if method == "register":
        return repository.add(args[0])
    entity = repository.get(args[0])
    if method == "get":
        return entity
    if method == "activate":
        entity["status"] = "ACTIVE"
        return None
    if method == "block":
        entity["status"] = "BLOCKED"
        return None
    if method == "unblock":
        entity["status"] = "ACTIVE"
        return None
    if method == "close":
        entity["status"] = "CLOSED"
        return None
    if method == "check":
        context = args[1]
        if entity["status"] != "ACTIVE":
            return CheckResult(False, "CARD_" + ("NOT_ACTIVE" if entity["status"] == "NEW" else entity["status"]))
        if context.as_of > entity["expiration_date"]:
            return CheckResult(False, "CARD_EXPIRED")
        if entity["card_type"] != "STANDARD":
            return CheckResult(False, "CARD_TYPE_DENIED")
        if context.channel == "ONLINE" and not entity["online_enabled"]:
            return CheckResult(False, "CARD_ONLINE_DISABLED")
        return CheckResult(True)
    raise ValueError(method)


from app.support.types import Repository

def new_service(repository=None):
    return _new_legacy_service(repository if repository is not None else Repository("card_id"))
