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

    def test_with_related_object(self):
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

    def test_with_multiple_related_objects_and_meta(self):
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
                    "parents": {
                        "data": [
                            {"type": "parent", "id": "id-parent-1"},
                            {"type": "parent", "id": "id-parent-2"},
                            {"type": "parent", "id": "id-parent-3"},
                        ],
                        "meta": {
                            "hey ho": "let's go"
                        }
                    }
                }
            },
            "included": [
                {
                    "type": "parent",
                    "id": "id-parent-1",
                    "attributes": {
                        "name": "Dad McDadFace"
                    }

                },
                {
                    "type": "parent",
                    "id": "id-parent-2",
                    "attributes": {
                        "name": "Mom McMomFace"
                    }

                },
                {
                    "type": "parent",
                    "id": "id-parent-3",
                    "attributes": {
                        "name": "Daddy McDaddyFace"
                    }

                },
            ]
        }

        actual = JsonApiMapper.from_json(api_json)

        expected = dict(
            id="asd",
            content="hej hej",
            title="a title",
            public_url=None,
            special=4711,
            parents=[
                dict(id="id-parent-1", name="Dad McDadFace"),
                dict(id="id-parent-2", name="Mom McMomFace"),
                dict(id="id-parent-3", name="Daddy McDaddyFace"),
            ],
            parents_meta={"hey ho": "let's go"}
        )
        self.assertEqual(actual, expected)
