
import json
from typing import List


def  test_blog(client,token_header):
    data = {'title':'nilswu11','description':'all abouts pypy modules'}
    response = client.post('/create_blog',json.dumps(data),headers=token_header)
    assert response.status_code == 200


# def get_all_blog(client):
#     response = client.get('/get_blog',response_model=List[schemas.Blog])
#     assert response.status_code == 200


def test_blog_update(client,token_header):
    data = {'title':'notvwwcss_pypy','description':'allabout new pypy'}
    response = client.put('/update_blog/31',json.dumps(data),headers=token_header)
    assert response.status_code == 200


# def test_delete_blog(client):
#     response = client.delete('delete_blog/30')
#     assert response.status_code == 200
