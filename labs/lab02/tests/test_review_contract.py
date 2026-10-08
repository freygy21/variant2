import pytest
from decimal import Decimal
from datetime import date, datetime, timezone, timedelta
from app import api
from app.support.errors import DomainError


def assert_code(code, action):
    with pytest.raises(DomainError) as caught:
        action()
    assert caught.value.code == code

from app.support.types import money

from app.domain.card import Card

@pytest.mark.parametrize("state,action,target", [('NEW', 'activate', 'ACTIVE'), ('NEW', 'block', None), ('NEW', 'close', 'CLOSED'), ('NEW', 'unblock', None), ('ACTIVE', 'activate', None), ('ACTIVE', 'block', 'BLOCKED'), ('ACTIVE', 'close', 'CLOSED'), ('ACTIVE', 'unblock', None), ('BLOCKED', 'activate', None), ('BLOCKED', 'block', None), ('BLOCKED', 'close', 'CLOSED'), ('BLOCKED', 'unblock', 'ACTIVE'), ('CLOSED', 'activate', None), ('CLOSED', 'block', None), ('CLOSED', 'close', None), ('CLOSED', 'unblock', None)])
def test_review_transition_table_and_atomic_refusal(state, action, target):
    item = Card("CARD-1", "C1", "ACC-1", date(2030, 4, 30), "STANDARD")
    paths = {'NEW': (), 'ACTIVE': ('activate',), 'BLOCKED': ('activate', 'block'), 'CLOSED': ('close',)}
    for setup in paths[state]:
        getattr(item, setup)()
    before = api.view(item)
    if target is None:
        assert_code("INVALID_STATE", lambda: getattr(item, action)())
        assert api.view(item) == before
    else:
        getattr(item, action)()
        assert item.status == target

def test_review_expiry_does_not_override_new_or_closed():
    item = Card("C", "U", "A", date(2030, 4, 30), "STANDARD")
    assert item.availability(date(2030, 5, 1)).code == "CARD_NOT_ACTIVE"
    item.close()
    assert item.availability(date(2030, 5, 1)).code == "CARD_CLOSED"
