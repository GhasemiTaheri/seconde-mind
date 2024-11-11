from typing import TypeVar, Generic

from pydantic import BaseModel
from pydantic.generics import GenericModel

ResultType = TypeVar("ResultType", bound=BaseModel)


class PaginatedResponse(GenericModel, Generic[ResultType]):
    total: int
    results: list[ResultType]
