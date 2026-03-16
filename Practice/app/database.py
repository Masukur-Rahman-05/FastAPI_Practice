from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase

class Base(DeclarativeBase):
    pass

engine = create_engine(
    "sqlite:///./test.db",
    echo=True,
    future=True
)

sessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)