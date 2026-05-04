import main

def test_order_can_be_saved_and_loaded_from_redis():
    order = main.Order(
        product_id="integration-product-1",
        price=50,
        fee=10,
        total=120,
        quantity=2,
        status="pending"
    )
    order.save()
    loaded = main.Order.get(order.pk)
    assert loaded.product_id == "integration-product-1"
    assert loaded.price == 50
    assert loaded.fee == 10
    assert loaded.total == 120
    assert loaded.quantity == 2
    assert loaded.status == "pending"

def test_order_status_can_be_updated():
    order = main.Order(
        product_id="integration-product-2",
        price=100,
        fee=20,
        total=240,
        quantity=2,
        status="pending"
    )
    order.save()
    order.status = "completed"
    order.save()
    loaded = main.Order.get(order.pk)
    assert loaded.status == "completed"

def test_order_completed_event_is_written_to_redis_stream():
    order = main.Order(
        product_id="stream-product-1",
        price=30,
        fee=6,
        total=36,
        quantity=1,
        status="completed"
    )
    event_id = main.redis.xadd("order_completed", order.model_dump(), "*")
    assert event_id is not None
    events = main.redis.xread({"order_completed": "0-0"}, count=1)
    assert len(events) > 0

def test_refund_event_is_written_to_redis_stream():
    order = main.Order(
        product_id="stream-product-2",
        price=50,
        fee=10,
        total=60,
        quantity=1,
        status="refunded"
    )
    event_id = main.redis.xadd("refund_order", order.model_dump(), "*")
    assert event_id is not None
    events = main.redis.xread({"refund_order": "0-0"}, count=1)
    assert len(events) > 0