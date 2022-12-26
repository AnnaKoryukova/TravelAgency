from pydantic import BaseModel, Field


class RequestTour(BaseModel):
    city: str
    country: str
    date: str

    class Config:
        orm_mode = True


class ResponseTour(RequestTour):
    id: int


class PutRequestTour(BaseModel):
    city: str | None
    country: str | None
    date: str | None

    class Config:
        orm_mode = True


class PutResponseTour(PutRequestTour):
    id: int
