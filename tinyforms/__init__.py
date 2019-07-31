import typing
from tinyforms.fields import Field

class FormDeserializer():
    def __init__(self, data: dict):
        for attrib in dir(self):
            d = getattr(self, attrib)
            if isinstance(d, Field):
                # Get the attribute from the form data
                v: typing.Optional[str] = data.get(d.name, None)

                d.value = v

                # Check the value is valid
                d.validate()

                # Finally, rebind to the value of the field
                self.__dict__[attrib] = d.value
