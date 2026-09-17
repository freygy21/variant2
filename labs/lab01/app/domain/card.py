# ЛР1: поля, конструктор и служебные проверки даны преподавателем.
# Завершите отмеченные методы; API пока использует старые функции.
from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError


class Card:
    def __init__(self, card_id, customer_id, account_id, expiration_date, card_type, online_enabled=True, contactless_enabled=True):
        identifier(card_id)
        identifier(customer_id)
        identifier(account_id)
        date_only(expiration_date)
        choice(card_type, ("STANDARD", "VIRTUAL"), "INVALID_CATEGORY")
        boolean(online_enabled)
        boolean(contactless_enabled)
        self._card_id = card_id
        self._customer_id = customer_id
        self._account_id = account_id
        self._expiration_date = expiration_date
        self._card_type = card_type
        self._online_enabled = online_enabled
        self._contactless_enabled = contactless_enabled
        self._status = "NEW"

    @property
    def card_id(self):
        return self._card_id

    @property
    def customer_id(self):
        return self._customer_id

    @property
    def account_id(self):
        return self._account_id

    @property
    def expiration_date(self):
        return self._expiration_date

    @property
    def card_type(self):
        return self._card_type

    @property
    def online_enabled(self):
        return self._online_enabled

    @property
    def contactless_enabled(self):
        return self._contactless_enabled

    @property
    def status(self):
        return self._status

    def activate(self):
        raise NotImplementedError("ЛР1: завершите Card.activate")

    def block(self):
        raise NotImplementedError("ЛР1: завершите Card.block")

    def unblock(self):
        raise NotImplementedError("ЛР1: завершите Card.unblock")

    def close(self):
        if self.status not in ('NEW', 'ACTIVE', 'BLOCKED'):
            raise DomainError("INVALID_STATE")
        self._status = "CLOSED"

    def is_expired(self, as_of):
        date_only(as_of)
        return as_of > self.expiration_date

    def availability(self, as_of):
        raise NotImplementedError("ЛР1: завершите Card.availability")
