from fastapi import APIRouter, Depends, Response

from models.request_models import RequestTour as Request_Tour
from models.request_models import ResponseTour, PutResponseTour, PutRequestTour
from models.db_models import Tour as DB_Tour

from db.database import get_db
from sqlalchemy.orm import Session

from fastapi.responses import JSONResponse

from exceptions.CustomHTTPException import NoContent, NotFound

router = APIRouter()


@router.post('/tours')
def add_new_tour(
        tour: Request_Tour,
        data_base: Session = Depends(get_db)
):
    data_tour = DB_Tour(**tour.dict())
    data_base.add(data_tour)
    data_base.commit()
    data_base.flush()
    return JSONResponse(status_code=200, content={
        'tour_id': data_tour.id
    })


@router.get(
    '/tours/{tour_id}',
    response_model=Request_Tour
)
def get_tour(
        tour_id: int,
        data_base: Session = Depends(get_db)
):
    data_tour = data_base.query(DB_Tour).get(tour_id)
    if data_tour is not None:
        response_tour = ResponseTour(**data_tour.__dict__)
        return JSONResponse(status_code=200, content={
            **response_tour.dict()
        })
    else:
        raise NotFound


@router.get(
    '/tours',
    response_model=list[Request_Tour]
)
def get_tours(
        data_base: Session = Depends(get_db)
):
    data_tours = data_base.query(DB_Tour).all()
    if data_tours is not None:
        response_tours = [ResponseTour(**x.__dict__).dict() for x in data_tours]
        return JSONResponse(status_code=200, content={
            'tours': response_tours
        })
    else:
        raise NotFound


@router.put('/tours/{tour_id}')
def change_tour(
        tour_id,
        new_tour_data: PutRequestTour,
        data_base: Session = Depends(get_db)
):
    data_tour = data_base.query(DB_Tour).get(tour_id)
    if data_tour is not None:
        data_base.query(DB_Tour). \
            filter(DB_Tour.id == tour_id). \
            update({k: v for k, v in new_tour_data.dict().items() if v is not None})
        data_base.commit()
        data_tour = data_base.query(DB_Tour).get(tour_id)
        data_base.flush()
        response_tour = PutResponseTour(**data_tour.__dict__)
        return JSONResponse(status_code=200, content={
            **response_tour.dict()
        })
    else:
        raise NotFound


@router.delete('/tours/{tour_id}')
def delete_tour(
        tour_id,
        data_base: Session = Depends(get_db)
):
    data_tour = data_base.query(DB_Tour).get(tour_id)
    if data_tour is not None:
        data_base.query(DB_Tour).filter(DB_Tour.id == tour_id).delete()
        data_base.commit()
        return JSONResponse(status_code=200, content={
            'Message': 'Tour has been deleted'
        })
    else:
        raise NotFound
