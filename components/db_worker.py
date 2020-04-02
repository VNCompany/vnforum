import sqlalchemy as sql
from sqlalchemy.orm import Session
import db_session


class DataBaseWorker:
    def __init__(self, session: Session):
        self.session = session


dbw = DataBaseWorker(db_session.create_session())
