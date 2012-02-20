from sqlalchemy import (
    Table, Column, ForeignKey,
    Boolean, Enum, Binary, PickleType,
    Integer, SmallInteger, BigInteger, Float,
    String, Text, Unicode, UnicodeText,
    DateTime, Date, Time,
    func, TypeDecorator, )
from sqlalchemy.orm import relationship, backref, aliased
import anyjson as json


class JSONData(TypeDecorator):
    "Type representing serialized JSON data."
    impl = String
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value
    
    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class TimestampMixin(object):
    ctime = Column(DateTime, default=func.now())
    mtime = Column(DateTime, default=func.now())

