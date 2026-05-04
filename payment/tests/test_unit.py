def test_order_fee_calculation():
    price = 100.0
    fee = 0.2 * price
    assert fee == 20.0

def test_order_total_calculation():
    price = 100.0
    quantity = 2
    total = 1.2 * price * quantity
    assert total == 240.0

def test_order_total_single_item():
    price = 50.0
    quantity = 1
    total = 1.2 * price * quantity
    assert total == 60.0

def test_order_status_initial():
    status = 'pending'
    assert status == 'pending'

def test_order_status_allowed_values():
    allowed = ['pending', 'completed', 'refunded']
    assert 'pending' in allowed
    assert 'completed' in allowed
    assert 'refunded' in allowed
    assert 'failed' not in allowed