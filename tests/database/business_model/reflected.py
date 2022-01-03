from sqlalchemy.ext.declarative import DeferredReflection


class Reflected(DeferredReflection):
    """It alters the declarative mapping process to be delayed until a 
    special class-level DeferredReflection.prepare() method is called, 
    which will perform the reflection process against a target database, 
    and will integrate the results with the declarative table mapping process, 
    that is, classes which use the __tablename__ attribute
    
    Reference: https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html#using-deferredreflection
    """
    __abstract__ = True
