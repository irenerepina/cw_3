from src.main import format_transactions, load_and_sort_data, mask_card


def test_load_and_sort_data():
    load = load_and_sort_data()
    assert isinstance(load, list)


def test_get_transaction():
    load = load_and_sort_data()
    transactions = format_transactions(load)
    assert len(transactions) == 5
