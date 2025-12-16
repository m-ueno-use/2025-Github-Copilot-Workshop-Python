def test_index_route_ok(client):
    res = client.get("/")
    assert res.status_code == 200
    text = res.get_data(as_text=True)
    assert "ポモドーロタイマー" in text
    assert "開始" in text and "リセット" in text


def test_static_files_are_served(client):
    assert client.get("/static/js/timer.js").status_code == 200
    assert client.get("/static/css/style.css").status_code == 200
