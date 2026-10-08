# Проверка исходного кода

Успешных обязательных проверок: **11**. С ошибками: **13**.

Эти ошибки связаны с заданием. После выполнения обязательной части все проверки должны пройти.

## Проверки, которые пока не проходят

- `tests.test_contract::test_closed_is_terminal`
- `tests.test_contract::test_expiry_is_inclusive_and_does_not_change_status`
- `tests.test_contract::test_repeat_pause_does_not_change_status`
- `tests.test_review_contract::test_review_transition_table_and_atomic_refusal[ACTIVE-activate-None]`
- `tests.test_review_contract::test_review_transition_table_and_atomic_refusal[ACTIVE-unblock-None]`
- `tests.test_review_contract::test_review_transition_table_and_atomic_refusal[BLOCKED-activate-None]`
- `tests.test_review_contract::test_review_transition_table_and_atomic_refusal[BLOCKED-block-None]`
- `tests.test_review_contract::test_review_transition_table_and_atomic_refusal[CLOSED-activate-None]`
- `tests.test_review_contract::test_review_transition_table_and_atomic_refusal[CLOSED-block-None]`
- `tests.test_review_contract::test_review_transition_table_and_atomic_refusal[CLOSED-close-None]`
- `tests.test_review_contract::test_review_transition_table_and_atomic_refusal[CLOSED-unblock-None]`
- `tests.test_review_contract::test_review_transition_table_and_atomic_refusal[NEW-block-None]`
- `tests.test_review_contract::test_review_transition_table_and_atomic_refusal[NEW-unblock-None]`

Если список отличается или тесты не запускаются из-за ошибки установки или импорта, сообщите преподавателю. Не отключайте проверки.
