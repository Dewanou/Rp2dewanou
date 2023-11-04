import requests
def test_page_load():
    url = "https://dewanoupredict-9816cc161f92.herokuapp.com/"
    response = requests.get(url)
    assert response.status_code == 200, f"Failed to load page: {url}"
