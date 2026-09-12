from datetime import datetime, timezone
from typing import Any, Annotated
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from bson import ObjectId
import uuid

def _to_str(v: Any) -> str:
    return str(v) if not isinstance(v, ObjectId) else str(v)
PyObjectId = Annotated[str, BeforeValidator(_to_str)]
def gen_id() -> str: return str(uuid.uuid4())
def now_utc() -> datetime: return datetime.now(timezone.utc)
class BaseDocument(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, extra="ignore")
    id: str = Field(default_factory=gen_id)
    def to_mongo(self) -> dict:
        d = self.model_dump()
        for k, v in list(d.items()):
            if isinstance(v, datetime): d[k] = v.isoformat()
        return d
    @classmethod
    def from_mongo(cls, doc: dict):
        if not doc: return None
        d = dict(doc); d.pop("_id", None); return cls(**d)
