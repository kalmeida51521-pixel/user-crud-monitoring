from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, Base
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

app = FastAPI(
    title="CRUD de Usuarios",
    description="API REST con FastAPI, PostgreSQL, Prometheus y Grafana",
    version="1.0.0"
)

# Métrica de Prometheus
USER_CREATED = Counter(
    "user_created",
    "Number of users created"
)

# Crear las tablas en PostgreSQL
Base.metadata.create_all(bind=engine)


# Conexión a la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# READ - Obtener todos los usuarios
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# READ - Obtener un usuario por ID
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user


# CREATE - Crear usuario
@app.post("/users")
def create_user(
    name: str,
    age: int,
    db: Session = Depends(get_db)
):
    user = User(name=name, age=age)

    db.add(user)
    db.commit()
    db.refresh(user)

    USER_CREATED.inc()

    return user


# UPDATE - Actualizar usuario
@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    name: str,
    age: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    user.name = name
    user.age = age

    db.commit()
    db.refresh(user)

    return user


# DELETE - Eliminar usuario
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "Usuario eliminado correctamente",
        "id": user_id
    }


# Métricas para Prometheus
@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )