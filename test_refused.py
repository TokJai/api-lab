import uuid

# A second user with a name that is already taken gets status 400 and {"error": "username already taken"}.
def test_duplicate_username_refused(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    res1 = api.post("/api/users", json=user)
    assert res1.status_code == 201
    res2 = api.post("/api/users", json=user)
    assert res2.status_code == 400
    assert res2.json() == {"error": "username already taken"}

# Logging in with a wrong password gets status 401 and {"error": "authentication failed"}.
def test_wrong_password_refused(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    res1 = api.post("/api/users", json=user)
    assert res1.status_code == 201
    wrong_user = {"username": name, "password": "WrongPassword-2026"}
    res2 = api.post("/api/users/token/login", json=wrong_user)
    assert res2.status_code == 401
    assert res2.json() == {"error": "authentication failed"}

# A user with an empty name gets status 400 and {"error": "username field is empty"}.
def test_empty_username_refused(api):
    user = {"username": "", "password": "Pizza-2026"}
    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}
