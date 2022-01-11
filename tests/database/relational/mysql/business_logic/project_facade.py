from relational.mysql.business_logic.model.project import Project
from relational.mysql.business_logic.dao.project_dao import ProjectDao


class ProjectFacade:
    __project_dao: ProjectDao

    def __init__(self, project_dao: ProjectDao) -> None:
        self.__project_dao = project_dao
    
    def __is_project_exist(self, project: Project):
        """Check if project exist"""
        project = self.__project_dao.get_project(project.title)
        if project == None:
            return False
        return True

    def create_project(self, project: Project):
        """Save project if not added"""
        return self.__project_dao.get_project_id(project.title) if self.__is_project_exist(project)\
            else self.__project_dao.save_record(project)
