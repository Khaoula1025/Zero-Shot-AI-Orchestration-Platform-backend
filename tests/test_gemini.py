# tests/test_gemini.py
from app.services.gemini_api import gemini_analyse

def test_gemini_analyse(mocker):

    mock_genai = mocker.patch('app.services.gemini_api.genai')
    
    mock_response = mocker.Mock()
    mock_response.text = '{"resume": "Test summary", "ton": "positif"}'
    
    mock_model = mocker.Mock()
    mock_model.generate_content.return_value = mock_response
    mock_genai.GenerativeModel.return_value = mock_model
    
    result = gemini_analyse("test text", "Finance", 0.85)
    
    assert result['resume'] == "Test summary"
    assert result['tone'] == "positif"
    assert result['categorie'] == "Finance"
    assert result['score'] == 0.85