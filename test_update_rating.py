import pytest

# Changing stars to 1 or 5 succeeds, while 0 or 6 is refused and leaves stars unchanged.
@pytest.mark.parametrize("stars,expected_status", [
    (0, 400),
    (1, 200),
    (5, 200),
    (6, 400)
])
def test_update_rating_boundaries(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected_status
    if expected_status == 200:
        assert res.json()["stars"] == stars
        res_get = api.get(path, headers=auth)
        assert res_get.status_code == 200
        assert res_get.json()["stars"] == stars
    else:
        # A refused update must leave the rating as it was
        res_get = api.get(path, headers=auth)
        assert res_get.status_code == 200
        assert res_get.json()["stars"] == rating["stars"]
