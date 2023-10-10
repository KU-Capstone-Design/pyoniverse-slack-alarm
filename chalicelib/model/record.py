import typing
from dataclasses import dataclass
from typing import List

from marshmallow import EXCLUDE, Schema, fields, types


@dataclass
class Record:
    type: str
    message: str
    ps: list
    cc: list


    class __RecordSchema(Schema):
        type: str = fields.Str(required=True)
        message: str = fields.Str(required=True)
        ps: List[str] = fields.List(fields.Str(), required=True, allow_none=True, default=[])
        cc: List[str] = fields.List(fields.Str(), required=True, validate=lambda x: len(x) > 0)


        class Meta:
            unknown = EXCLUDE


        def load(
                self,
                data: (
                        typing.Mapping[str, typing.Any]
                        | typing.Iterable[typing.Mapping[str, typing.Any]]
                ),
                *,
                many: bool | None = None,
                partial: bool | types.StrSequenceOrSet | None = None,
                unknown: str | None = None,
        ):
            res = super().load(data, many=many, partial=partial, unknown=unknown)
            return Record(**res)


    @classmethod
    def load(cls, data: dict) -> "Record":
        return cls.__RecordSchema().load(data)
