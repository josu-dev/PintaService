from src.web import create_app

app = create_app()
app.testing = True
client = app.test_client()


def test_index():
    response = client.get('/')
    assert response.status_code == 200
    assert b'Grupo 4' in response.data
