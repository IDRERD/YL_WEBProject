import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

__factory = None
SqlAlchemyBase = dec.declarative_base()


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("You must to specify the database filename")

    conn_str = f"sqlite:///{db_file.strip()}?check_same_thread=False"
    print(f"Connecting to database by address {conn_str}")

    engine = sa.create_engine(conn_str)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()