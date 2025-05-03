import os
import tempfile
import pytest
from app import app, session_logs
from io import BytesIO

def setup_module(module):
    # 清空 session_logs，避免测试间干扰
    session_logs.clear()

def teardown_module(module):
    session_logs.clear()

def test_upload_and_grouping(client):
    # 上传两条同一天的记录和一条不同天的记录
    data1 = {
        'grade': 'V3',
        'note': 'Nice move!',
        'date': '2024-06-01',
        'image': (BytesIO(b'mockdata1'), 'test1.jpg')
    }
    data2 = {
        'grade': 'V4',
        'note': 'Crux at the top',
        'date': '2024-06-01',
        'image': (BytesIO(b'mockdata2'), 'test2.jpg')
    }
    data3 = {
        'grade': 'V2',
        'note': 'Easy warmup',
        'date': '2024-06-02',
        'image': (BytesIO(b'mockdata3'), 'test3.jpg')
    }
    client.post('/session-log', data=data1, content_type='multipart/form-data', follow_redirects=True)
    client.post('/session-log', data=data2, content_type='multipart/form-data', follow_redirects=True)
    client.post('/session-log', data=data3, content_type='multipart/form-data', follow_redirects=True)

    # 检查 session_logs 是否正确
    assert len(session_logs) == 3
    days = [log['date'].split(' ')[0] for log in session_logs]
    assert days.count('2024-06-01') == 2
    assert days.count('2024-06-02') == 1

    # 检查页面分组渲染
    response = client.get('/session-log')
    html = response.data.decode()
    assert '2024-06-01' in html
    assert '2024-06-02' in html
    assert 'Nice move!' in html
    assert 'Crux at the top' in html
    assert 'Easy warmup' in html

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
    with app.test_client() as client:
        yield client
    os.close(db_fd)
    os.remove(db_path) 