import dateutil
import jsonpointer
from six import with_metaclass


class JsonApiMapperMeta(type):
    def __init__(cls, name, bases, clsdict):
        if len(cls.mro()) > 2:
            cls.register(cls.type_)
        super(JsonApiMapperMeta, cls).__init__(name, bases, clsdict)


class JsonApiMapper(with_metaclass(JsonApiMapperMeta, object)):
    registry = {}

    def map_json(self, json):
        result = {}
        result.update(json["attributes"])
        result["id"] = json["id"]
        result["type"] = json["type"]
        if "relationships" in json:
            result["relationships"] = json["relationships"]

        for attr, spec in type(self).__dict__.items():
            if isinstance(spec, dict) and "type" in spec:
                if spec["type"] == "jsonpointer":
                    value = jsonpointer.resolve_pointer(json, spec["pointer"], None)
                elif spec["type"] == "from_attribute":
                    value = jsonpointer.resolve_pointer(json, "/attributes/" + spec["attribute"])
                    del result[spec["attribute"]]
                elif spec["type"] == "datetime" and attr in result:
                    value = dateutil.parser.parse(result[attr])

                result[attr] = value

        return result

    @classmethod
    def register(cls, type_):
        cls.registry[type_] = cls

    @classmethod
    def from_json(cls, json):
        def do(data):
            if data["type"] not in cls.registry:
                raise ValueError("{} is not mapped to a JsonApiMapper".format(data["type"]))
            return cls.registry[data["type"]]().map_json(data)

        data = {}
        for key in ["data", "included"]:
            if key in json:
                data[key] = cls._apply_once_or_many(json[key], do)
        key_mapper = {(item["type"], item["id"]): item for item in data.get("included", [])}
        for key, value in data.items():
            if key in ["data", "included"]:
                cls._apply_once_or_many(value, lambda item: cls._link_relationships(item, key_mapper))

        for key in ["data", "included"]:
            cls._apply_once_or_many(data.get(key, []), lambda item: item.pop('type', None))
        return data["data"]

    @classmethod
    def _link_relationships(cls, item, key_mapper):
        relationships = item.pop("relationships", {})
        for key, value in relationships.items():
            def do(data):
                relationsship_data = data.get('data', {})
                related_type = relationsship_data.get("type", None)
                related_id = relationsship_data.get("id", None)
                return key_mapper.get((related_type, related_id), relationsship_data)

            item[key] = cls._apply_once_or_many(value, do)

    @classmethod
    def _apply_once_or_many(cls, data, func):
        if isinstance(data, list):
            return [func(item) for item in data]
        else:
            return func(data)
