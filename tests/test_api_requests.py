import pytest, re
from playwright.sync_api import APIRequestContext

@pytest.fixture(scope="session")
def api_request_context(playwright) -> APIRequestContext:
    return playwright.request.new_context(base_url="https://jsonplaceholder.typicode.com")

def test_get_posts(api_request_context):
    response = api_request_context.get("/posts/1")
    assert response.status == 200
    json_data = response.json()
    assert json_data["id"] == 1
    assert json_data["userId"] == 1

def test_create_post(api_request_context):
    response = api_request_context.post("/posts", data={
        "title": "Playwright API Test",
        "body": "This is a test post.",
        "userId": 1
    })
    assert response.status == 201
    json_data = response.json()
    assert json_data["title"] == "Playwright API Test"
    assert json_data["userId"] == 1

def test_update_post(api_request_context):
    response = api_request_context.put("/posts/1", data={
        "id": 1,
        "title": "Updated Title",
        "body": "Updated content",
        "userId": 1
    })
    assert response.status == 200
    json_data = response.json()
    assert json_data["title"] == "Updated Title"

def test_delete_post(api_request_context):
    response = api_request_context.delete("/posts/1")
    assert response.status == 200

def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

def test_json_schema(api_request_context):
    response = api_request_context.get("/users/1")
    json_data = response.json()

    required_keys = ["id", "name", "email", "address"]
    for key in required_keys:
        assert key in json_data, f"Missing key: {key}"

    assert is_valid_email(json_data["email"])

def test_query_params(api_request_context):
    response = api_request_context.get("/comments?postId=1")
    json_data = response.json()
    for comment in json_data:
        assert comment["postId"] == 1

def test_non_existing_post(api_request_context):
    response = api_request_context.get("/posts/9999")
    assert response.status == 404
