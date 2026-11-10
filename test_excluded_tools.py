import pytest

# The pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize("excluded", [
    [],
    ["Knife"],
    ["Scissors"],
    ["Knife", "Scissors"]
])
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded

# Defect 1: Excluding all tools should return 400 with an error message, but returns 500
@pytest.mark.xfail(reason="Defect 1: excluding all tools returns 500 instead of 400 with an error message", strict=True)
def test_excluding_all_tools_refused(api, auth):
    body = {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()
