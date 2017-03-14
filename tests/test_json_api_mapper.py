import sys
sys.path.append("/home/frost/code/github/kundo/json_api_mapper/")

from unittest import TestCase
from json_api_mapper import JsonApiMapper


class TestMapper(JsonApiMapper):
    type_ = "test"
    special = {'type': 'from_attribute', 'attribute': 'some_special_value'}
    public_url = {'type': 'jsonpointer', 'pointer': '/links/public'}


class ParentMapper(JsonApiMapper):
    type_ = "parent"


class JsonApiMapperTest(TestCase):
    def test_attributes(self):
        api_json = {
            "data": {
                "id": "asd",
                "type": "test",
                "attributes": {
                    "content": "hej hej",
                    "title": "a title",
                    "some_special_value": 4711,
                },
                "links": {
                    "public": "public-link"
                }
            }
        }

        actual = JsonApiMapper.from_json(api_json)

        expected = dict(
            id="asd",
            content="hej hej",
            title="a title",
            public_url="public-link",
            special=4711,
        )
        self.assertEqual(actual, expected)

    def test_without_public_url(self):
        api_json = {
            "data": {
                "id": "asd",
                "type": "test",
                "attributes": {
                    "content": "hej hej",
                    "title": "a title",
                    "some_special_value": 4711,
                },
            }
        }

        actual = JsonApiMapper.from_json(api_json)

        expected = dict(
            id="asd",
            content="hej hej",
            title="a title",
            public_url=None,
            special=4711,
        )
        self.assertEqual(actual, expected)

    def test_with_related_obj(self):
        api_json = {
            "data": {
                "id": "asd",
                "type": "test",
                "attributes": {
                    "content": "hej hej",
                    "title": "a title",
                    "some_special_value": 4711,
                },
                "relationships": {
                    "parent": {
                        "data": {
                            "type": "parent",
                            "id": "id-parent"
                        }
                    }
                }
            },
            "included": [
                {
                    "type": "parent",
                    "id": "id-parent",
                    "attributes": {
                        "name": "Parent McParentface"
                    }

                }
            ]
        }

        actual = JsonApiMapper.from_json(api_json)

        expected = dict(
            id="asd",
            content="hej hej",
            title="a title",
            public_url=None,
            special=4711,
            parent=dict(
                id="id-parent",
                name="Parent McParentface"
            )
        )
        self.assertEqual(actual, expected)
