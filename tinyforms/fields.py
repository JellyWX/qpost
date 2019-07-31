import typing
from tinyforms import Field
from werkzeug.security import generate_password_hash, check_password_hash

class Field():
    class FieldLengthExceeded(Exception):
        pass

    class MissingFieldData(Exception):
        pass

    def __init__(self, name: str, *, strict: bool=False, max_length: int=1024):
        self.name: str = name
        self._raw_value: typing.Optional[str] = None
        self._strict: bool = strict
        self._max_length: int = max_length

    @property
    def value(self) -> typing.Optional[str]:
        return self._value
    
    @value.setter
    def value(self, value):
        if value is not None and len(value) > self._max_length:
            raise self.FieldLengthExceeded
        else:
            self._value = value

    def validate(self):
        if self._raw_value is None and self._strict:
            raise self.MissingFieldData
        elif self._value is not None:
            self._type_specific_validation()

    def _type_specific_validation(self):
        pass


class IntegerField(Field):
    class InvalidInteger(Exception):
        pass

    def _type_specific_validation(self):
        if not all([x in '0123456789' for x in self._value]):
            raise self.InvalidInteger

    @Field.value.getter
    def value(self) -> typing.Optional[int]:
        return self._value if self._value is None else int(self._value)


class PasswordField(Field):
    class Password(str):
        def __eq__(self, comparator):
            return check_password_hash(self, comparator)

    @Field.value.getter
    def value(self) -> typing.Optional[Password]:
        return self._value if self._value is None else self.Password(generate_password_hash(self._value))


class EmailField(Field):
    class InvalidEmail(Exception):
        pass

    def _type_specific_validation(self):
        if '@' not in self._value:
            raise self.InvalidEmail
