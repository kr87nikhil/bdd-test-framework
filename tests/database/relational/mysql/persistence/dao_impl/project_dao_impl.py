from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.expression import insert, select

from relational.mysql.business_logic.model.project import Project
from relational.mysql.business_logic.dao.project_dao import ProjectDao
from relational.mysql.persistence.model.project import Project as ProjectDB


class ProjectDaoImpl(ProjectDao):
    __engine: Engine

    def __init__(self, database_engine) -> None:
        self.__engine = database_engine

    def get_project(self, title: str) -> Project:
        select_project = select(ProjectDB).filter_by(title=title)
        with Session(self.__engine) as session:
            result = session.execute(select_project).first()
        return Project(title, result[0].description) if result != None else None

    def get_project_id(self, title: str) -> int:
        select_project = select(ProjectDB).filter_by(title=title)
        with Session(self.__engine) as session:
            result = session.execute(select_project).first()
        return result[0].projectId

    def save_record(self, project: Project) -> int:
        insert_project = insert(ProjectDB).values(
            title = project.title, description = project.description
        )
        with Session(self.__engine) as session:
            result = session.execute(insert_project)
            session.commit()
        return result.inserted_primary_key[0]
