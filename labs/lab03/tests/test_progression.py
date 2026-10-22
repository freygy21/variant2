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
