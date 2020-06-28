import json

from jixin import (
    JSONDecodable,
    JSONEncodable,
    JSONEncoderDelegated,
    JSONEncoderHandler,
)


class TestJSONDecodable:
    def test_simple(self):
        class Dummy(JSONDecodable):
            foo = None

            def __init__(self, foo):
                self.foo = foo

            @classmethod
            def _decode_test(clzz, dct):
                return "foo" in dct

            @classmethod
            def _decode(clzz, dct):
                return clzz(dct["foo"])

        jsondecoder = json.JSONDecoder(object_hook=JSONDecodable.object_hook)

        result = jsondecoder.decode('{"foo": "bar"}')
        assert isinstance(result, Dummy)
        assert result.foo == "bar"

        result = jsondecoder.decode('[{"foo": "bar"},42]')
        assert isinstance(result[0], Dummy)
        assert result[0].foo == "bar"


class TestJSONEncoderDelegate:
    def test_simple(self):
        class Dummy:
            foo = None

            def __init__(self, foo):
                self.foo = foo

        class DummyHandler(JSONEncoderHandler):
            def _encode_test(self, o):
                return isinstance(o, Dummy)

            def _encode(self, o):
                print("Encoding",)
                return {"foo": o.foo}

        jsonencoder = JSONEncoderDelegated()
        jsonencoder.registry.append(DummyHandler())

        result = jsonencoder.encode(Dummy("bar"))
        assert result == '{"foo": "bar"}', result
        result = jsonencoder.encode([Dummy("bar"), 42])
        assert result == '[{"foo": "bar"}, 42]', result

    def test_simple_class(self):
        class Dummy:
            foo = None

            def __init__(self, foo):
                self.foo = foo

        class DummyHandler(JSONEncoderHandler):
            def _encode_test(self, o):
                return isinstance(o, Dummy)

            def _encode(self, o):
                return {"foo": o.foo}

        jsonencoder = JSONEncoderDelegated()
        JSONEncoderDelegated.registry.append(DummyHandler())

        result = jsonencoder.encode(Dummy("bar"))
        assert result == '{"foo": "bar"}', result
        result = jsonencoder.encode([Dummy("bar"), 42])
        assert result == '[{"foo": "bar"}, 42]', result

    def test_mixin(self):
        class Dummy(JSONEncodable):
            foo = None

            def __init__(self, foo):
                self.foo = foo

            def _encode(self):
                return {"foo": self.foo}

        jsonencoder = JSONEncoderDelegated()

        result = jsonencoder.encode(Dummy("bar"))
        assert result == '{"foo": "bar"}', result
        result = jsonencoder.encode([Dummy("bar"), 42])
        assert result == '[{"foo": "bar"}, 42]', result
