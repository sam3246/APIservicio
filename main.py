from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Servicio
from shemas import ServicioCreate, ServicioResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicios API")


@app.get("/servicios", response_model=list[ServicioResponse])
def get_servicios(db: Session = Depends(get_db)):
    return db.query(Servicio).all()


@app.post("/servicios", response_model=ServicioResponse, status_code=201)
def create_servicio(
    data: ServicioCreate,
    db: Session = Depends(get_db),
):
    servicio = Servicio(
        name=data.name,
        price=data.price,
        description=data.description,
    )

    db.add(servicio)
    db.commit()
    db.refresh(servicio)

    return servicio


@app.put("/servicios/{servicio_id}", response_model=ServicioResponse)
def update_servicio(
    servicio_id: int,
    data: ServicioCreate,
    db: Session = Depends(get_db),
):
    servicio = db.query(Servicio).filter(
        Servicio.id == servicio_id
    ).first()

    if servicio is None:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado",
        )

    servicio.name = data.name
    servicio.price = data.price
    servicio.description = data.description

    db.commit()
    db.refresh(servicio)

    return servicio
