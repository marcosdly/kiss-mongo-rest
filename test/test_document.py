import pytest
import json

url: str = "/DOCUMENT/?db=test&col=test"


@pytest.mark.order("first")
def test_create_document(client, fake, state) -> None:  # type: ignore
    for _ in range(50):
        doc = fake.json(num_rows=1)
        response = client.post(url, content=doc)
        assert response.status_code == 201
        try:
            resp_json = response.json()
            assert resp_json["id"]
            assert resp_json["document"] == json.loads(doc)
            state.new_ids.append(resp_json["id"])
        except KeyError:
            pytest.fail("Returned JSON response doesn't have the necessary keys.")
