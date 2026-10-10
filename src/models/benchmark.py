from pydantic import BaseModel


class BenchmarkItem(BaseModel):
    query: str
    expected: str