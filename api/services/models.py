from sqlalchemy.orm import declarative_base, mapped_column, relationship, Mapped
from sqlalchemy import LargeBinary, Integer, String, Float, DateTime, ForeignKey
from uuid import uuid4
from datetime import datetime
from typing import List

Base = declarative_base()


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String)
    file: Mapped[bytes] = mapped_column(LargeBinary)

    projects: Mapped[List["Project"]] = relationship(back_populates="file")

    def __init__(self, filename: str, file: bytes):
        self.filename = filename
        self.file = file


class Project(Base):
    __tablename__ = "projects"

    uuid: Mapped[str] = mapped_column(String, primary_key=True)
    id: Mapped[int] = mapped_column(Integer, unique=True)
    name: Mapped[str] = mapped_column(String(100))

    file_id: Mapped[int] = mapped_column(ForeignKey("files.id"))
    file: Mapped["File"] = relationship(back_populates="projects")
    values: Mapped[List["Value"]] = relationship(back_populates="project")

    def __init__(self, id: int, name: str, file: File):
        self.uuid = str(uuid4())
        self.id = id
        self.name = name
        self.file = file


class Value(Base):
    __tablename__ = "values"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plan: Mapped[float] = mapped_column(Float)
    fact: Mapped[float] = mapped_column(Float)
    date: Mapped[datetime] = mapped_column(DateTime)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship(back_populates="values")

    def __init__(self, plan: float, fact: float, date: datetime, project: Project):
        self.plan = plan
        self.fact = fact
        self.date = date
        self.project = project

    def to_dict(self, value_type: str):
        if value_type == "plan":
            return {
                "id": self.id,
                "plan": self.plan,
                "date": self.date,
                "project_id": self.project_id,
            }
        elif value_type == "fact":
            return {
                "id": self.id,
                "fact": self.fact,
                "date": self.date,
                "project_id": self.project_id,
            }
