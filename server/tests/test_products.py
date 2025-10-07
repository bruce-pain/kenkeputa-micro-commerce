from uuid import uuid4

from fastapi import status

from app.api.models.user import User


def _auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_create_product_requires_admin(client):
    email = f"user_{uuid4().hex}@example.com"
    password = "Testpass123!"
    register = client.post("/api/v1/auth/register", json={"email": email, "password": password})
    token = register.json()["access_token"]

    response = client.post(
        "/api/v1/products",
        json={
            "name": f"Test Product {uuid4().hex}",
            "description": "Simple description",
            "price": 10.50,
            "stock": 5,
        },
        headers=_auth_headers(token),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_can_create_and_fetch_product(client, db_session):
    admin_email = f"admin_{uuid4().hex}@example.com"
    admin_password = "Adminpass123!"
    register = client.post(
        "/api/v1/auth/register",
        json={"email": admin_email, "password": admin_password},
    )
    token = register.json()["access_token"]

    admin_user = db_session.query(User).filter_by(email=admin_email).first()
    admin_user.role = "admin"
    db_session.commit()

    product_payload = {
        "name": f"Product {uuid4().hex}",
        "description": "Premium test product",
        "price": 25.75,
        "stock": 12,
    }

    create_response = client.post(
        "/api/v1/products",
        json=product_payload,
        headers=_auth_headers(token),
    )
    assert create_response.status_code == status.HTTP_201_CREATED

    product_data = create_response.json()["data"]
    product_id = product_data["id"]
    assert product_data["name"] == product_payload["name"]

    list_response = client.get("/api/v1/products", headers=_auth_headers(token))
    assert list_response.status_code == status.HTTP_200_OK
    items = list_response.json()["data"]["items"]
    assert any(item["id"] == product_id for item in items)

    detail_response = client.get(
        f"/api/v1/products/{product_id}", headers=_auth_headers(token)
    )
    assert detail_response.status_code == status.HTTP_200_OK
    assert detail_response.json()["data"]["name"] == product_payload["name"]