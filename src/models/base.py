from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def as_dict(self):
        return {colums.name: getattr(self, colums.name) for colums in self.__table__.columns}
