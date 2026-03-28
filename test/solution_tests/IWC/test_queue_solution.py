from __future__ import annotations



from .utils import call_dequeue, call_enqueue, call_size, iso_ts, run_queue


def test_enqueue_size_dequeue_flow() -> None:
    run_queue([
        call_enqueue("credit_check", 1, iso_ts(delta_minutes=0)).expect(2),
        call_size().expect(2),
        call_dequeue().expect("companies_house", 1),
        call_dequeue().expect("credit_check", 1)
    ])


def test_three() -> None:
    run_queue([
        call_enqueue("logs", 1, iso_ts(delta_minutes=0)).expect(1),
        call_enqueue("banks", 5, iso_ts(delta_minutes=0)).expect(2),
        call_enqueue("loans", 1, iso_ts(delta_minutes=0)).expect(3),
        call_enqueue("users", 1, iso_ts(delta_minutes=0)).expect(4),
        call_size().expect(4),
        call_dequeue().expect("logs", 1),
        call_dequeue().expect("loans", 1),
        call_dequeue().expect("users", 1),
        call_dequeue().expect("banks", 5),
    ])

def test_timestamp() -> None:
    run_queue([
        call_enqueue("logs", 1, iso_ts(delta_minutes=10)).expect(1),
        call_enqueue("logs", 3, iso_ts(delta_minutes=0)).expect(2),
        call_size().expect(2),
        call_dequeue().expect("logs", 3),
        call_dequeue().expect("logs", 1),
    ])

def test_dependency() -> None:
    run_queue([
        call_enqueue(provider="credit_check", user_id=1, timestamp=iso_ts(delta_minutes=0)).expect(2),
        call_dequeue().expect(provider="companies_house", user_id=1),
        call_dequeue().expect(provider="credit_check", user_id=1)
    ])

def test_unique() -> None:
    run_queue([
        call_enqueue(provider="companies_house", user_id=1, timestamp=iso_ts(delta_minutes=0)).expect(1),
        call_enqueue(provider="companies_house", user_id=1, timestamp=iso_ts(delta_minutes=0)).expect(1),
        call_size().expect(1),
    ])

def test_unique_with_timestamp() -> None:
    run_queue([
        call_enqueue(provider="credit_check", user_id=1, timestamp=iso_ts(delta_minutes=0)).expect(2),
        call_enqueue(provider="credit_check", user_id=1, timestamp=iso_ts(delta_minutes=2)).expect(2),
        call_size().expect(2),
    ])

def test_bank_statement_three_deprio() -> None:
    run_queue([
        call_enqueue(provider="companies_house", user_id=1, timestamp=iso_ts(delta_minutes=0)).expect(1),
        call_enqueue(provider="bank_statements", user_id=1, timestamp=iso_ts(delta_minutes=0)).expect(2),
        call_enqueue(provider="id_verification", user_id=1, timestamp=iso_ts(delta_minutes=0)).expect(3),
        call_size().expect(3),
        call_dequeue().expect(provider="companies_house", user_id=1),
        call_dequeue().expect(provider="id_verification", user_id=1),
        call_dequeue().expect(provider="bank_statements", user_id=1),
    ])

def test_bank_statement_deprio() -> None:
    run_queue([
        call_enqueue(provider="companies_house", user_id=1, timestamp=iso_ts(delta_minutes=0)).expect(1),
        call_enqueue(provider="bank_statements", user_id=1, timestamp=iso_ts(delta_minutes=0)).expect(2),
        call_enqueue(provider="id_verification", user_id=5, timestamp=iso_ts(delta_minutes=0)).expect(3),
        call_size().expect(3),
        call_dequeue().expect(provider="companies_house", user_id=1),
        call_dequeue().expect(provider="id_verification", user_id=5),
        call_dequeue().expect(provider="bank_statements", user_id=1),
    ])