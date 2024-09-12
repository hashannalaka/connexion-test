
def test_user_creation(test_client):
    response = test_client.post('/users', json={'name': 'John Doe'})
    assert response.status_code == 201
    assert response.json['name'] == 'John Doe'
