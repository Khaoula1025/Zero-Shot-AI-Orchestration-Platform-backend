from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app
from app.services.auth_services import get_current_user

client = TestClient(app)


def test_text_analyze_endpoint(mocker):
    app.dependency_overrides[get_current_user] = lambda: "test_user"
    mock_hf = mocker.patch('app.routers.analyzeRouter.articles_analyses')
    mock_hf.return_value = {'label': 'Finance', 'score': 0.85}
    mock_gemini = mocker.patch('app.routers.analyzeRouter.gemini_analyse')

    mock_gemini.return_value = {
        'resume': 'Test summary',
        'tone': 'positif',
        'categorie': 'Finance',
        'score': 0.85
    }

    response = client.post('/analyse', json={
        'article_text': 'This is a test article about finance'
    })

    assert response.status_code == 200
    data = response.json()

    assert data['resume'] == 'Test summary'
    assert data['tone'] == 'positif'
    assert data['categorie'] == 'Finance'
    assert data['score'] == 0.85

    mock_hf.assert_called_once_with('This is a test article about finance')
    mock_gemini.assert_called_once_with(
        'This is a test article about finance', 'Finance', 0.85
    )

    app.dependency_overrides.clear()


def test_text_analyze_endpoint_unauthorized():
    app.dependency_overrides[get_current_user] = lambda: (_ for _ in ()).throw(
        HTTPException(status_code=401)
    )

    response = client.post('/analyse', json={"article_text": "text"})
    assert response.status_code == 401

    app.dependency_overrides.clear()


def test_text_analyze_endpoint_invalid_input():
    app.dependency_overrides[get_current_user] = lambda: "test_user"

    response = client.post('/analyse', json={})
    assert response.status_code == 422

    app.dependency_overrides.clear()
