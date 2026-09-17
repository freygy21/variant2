import pytest
from decimal import Decimal
from datetime import date, datetime, timezone, timedelta
from app import api
from app.support.errors import DomainError
from app.support.types import Repository, CheckResult, Money, money


def error(code, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == code


def invoke(service, method, *args, **kwargs):
    return api.call(service, method, *args, **kwargs)

from app.support.types import CardContext

def context():
    return CardContext(date(2030, 4, 29))

def entity(key='CARD-1'):
    return api.make(key, "C1", "ACC-1", date(2030, 4, 30), "STANDARD")

def prepared(key='CARD-1'):
    service = api.create()
    item = entity(key)
    invoke(service, "register", item)
    invoke(service, "activate", key)
    return service, item

def test_basic_lifecycle_and_isolation():
    service, item = prepared()
    other = entity("OTHER")
    invoke(service, "register", other)
    assert invoke(service, "check", 'CARD-1', context()).allowed
    invoke(service, 'block', 'CARD-1')
    assert invoke(service, "check", 'CARD-1', context()).code == 'CARD_BLOCKED'
    assert api.view(other)["status"] == 'NEW'
    invoke(service, 'unblock', 'CARD-1')
    assert invoke(service, "check", 'CARD-1', context()).allowed
    assert invoke(service, "get", 'CARD-1') is item

def test_repositories_are_independent():
    service, item = prepared()
    error("NOT_FOUND", lambda: invoke(api.create(), "get", 'CARD-1'))

def test_checks_do_not_change_entity():
    service, item = prepared()
    before = api.view(item)
    invoke(service, "check", 'CARD-1', context())
    invoke(service, "check", 'CARD-1', context())
    assert api.view(item) == before
