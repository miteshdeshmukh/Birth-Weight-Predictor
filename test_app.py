from app import app

def test_hello_route_success():
    tester=app.test_client()
    response=tester.get('/hello')
    assert response.status_code==200

# def test_hello_route_faliure():
#     tester=app.test_client()
#     response=tester.get('/hello')
#     assert response.status_code==500

