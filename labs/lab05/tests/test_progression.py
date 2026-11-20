import pytest
from datetime import date, datetime, timezone
from decimal import Decimal
from app import api
from app.support.errors import DomainError


def code(expected, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == expected

from app.domain.card import Card
from app.support.types import CardContext

def test_progression_availability_does_not_cache_state():
    service = api.create()
    item = Card("C", "U", "A", date(2030,4,30), "STANDARD")
    item.activate()
    service.register(item)
    first = service.check("C", CardContext(date(2030,4,29)))
    assert first.allowed
    item.block()
    assert service.check("C", CardContext(date(2030,4,29))).code == "CARD_BLOCKED"
    item.unblock()
    assert service.check("C", CardContext(date(2030,4,29))).allowed
    assert first.allowed and item.status == "ACTIVE"

from app.domain.usage import CardUsageRule
from app.support.types import Repository, CheckResult
from app.services.card_service import CardService

def test_progression_dependency_called_once_and_retained():
    calls = []
    class Once(CardUsageRule):
        def check(self, item, ctx):
            calls.append(item)
            if len(calls) == 1: raise DomainError("TEMPORARY")
            return CheckResult(True)
    rules = [Once()]
    repo = Repository("card_id")
    item = Card("C", "U", "A", date(2030,4,30), "STANDARD")
    item.activate()
    repo.add(item)
    service = CardService(repo, rules)
    rules.clear()
    code("TEMPORARY", lambda: service.check("C", CardContext(date(2030,4,29))))
    assert len(calls) == 1 and item.status == "ACTIVE"
    assert service.check("C", CardContext(date(2030,4,29))).allowed and calls == [item, item]

from app.services.card_service import CardService
from app.support.types import CheckResult

def test_progression_extra_lab05(monkeypatch):
    def check(self, card_id, context):
        return CheckResult(True) if context.as_of.day < 30 else CheckResult(False, "DATE_DENIED")
    monkeypatch.setattr(CardService, "check", check)
    service = object.__new__(CardService)
    dates = (date(2030, 4, 29), date(2030, 4, 30))
    rows = service.check_dates("CARD", dates)
    assert tuple(x for x, _ in rows) == dates
    assert tuple(y.allowed for _, y in rows) == (True, False)
    assert service.allowed_dates("CARD", dates) == dates[:1]
