# tests/test_hugging_face.py
from app.services.hugging_face_filter import articles_analyses

def test_articles_analyses(mocker):
    mock_client = mocker.patch('app.services.hugging_face_filter.client')
    
    class FakeResult:
        def __init__(self, label, score):
            self.label = label
            self.score = score
        
        def __getitem__(self, key):
            return getattr(self, key)
    
    fake_response = [
        FakeResult('Finance', 0.85),
        FakeResult('Marketing et Communication', 0.10)
    ]
    
    mock_client.zero_shot_classification.return_value = fake_response
    
    result = articles_analyses("test text")
    
    assert result['label'] == 'Finance'
    assert result['score'] == 0.85