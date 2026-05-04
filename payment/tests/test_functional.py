from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def test_get_order_not_found():
    response = client.get('/orders/nepostojeci-pk')
    assert response.status_code == 404

def test_get_order_success():
    import main as m
    order = m.Order(
        product_id="func-product-1",
        price=100,
        fee=20,
        total=120,
        quantity=1,
        status="pending"
    )
    order.save()
    response = client.get(f'/orders/{order.pk}')
    assert response.status_code == 200
    assert response.json()['product_id'] == "func-product-1"

def test_create_order_product_not_found():
    mock_response = MagicMock()
    mock_response.status_code = 404
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__ = AsyncMock(
            return_value=MagicMock(
                get=AsyncMock(return_value=mock_response)
            )
        )
        response = client.post('/orders', json={'id': 'bad-id', 'quantity': 1})
        assert response.status_code == 400