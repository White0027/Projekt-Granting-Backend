import os
import asyncio
import aiohttp
from functools import cache
from aiodataloader import DataLoader
from uoishelpers.dataloaders import createIdLoader, createFkeyLoader


from src.DBDefinitions import (
    BaseModel, 
    ProgramFormTypeModel,
    ProgramLanguageTypeModel,
    ProgramLevelTypeModel,
    ProgramModel,
    ProgramTitleTypeModel,
    ProgramTypeModel,
    ProgramStudentModel,
    ProgramStudentMessageModel,
    ProgramStudentStateModel,

    ClassificationLevelModel,
    ClassificationModel,
    ClassificationTypeModel,
    
    SubjectModel,
    SemesterModel,
    TopicModel,
    LessonModel,
    LessonTypeModel
)


@cache
def composeAuthUrl():
    hostname = os.environ.get("GQLUG_ENDPOINT_URL", None)
    assert hostname is not None, "undefined GQLUG_ENDPOINT_URL"
    assert "://" in hostname, "probably bad formated url, has it 'protocol' part?"
    assert "." not in hostname, "security check failed, change source code"
    return hostname

dbmodels = {
    "programforms": ProgramFormTypeModel,
    "programlanguages": ProgramLanguageTypeModel,
    "programleveltypes": ProgramLevelTypeModel,
    "programs": ProgramModel,
    "programtitletypes": ProgramTitleTypeModel,
    "programtypes": ProgramTypeModel,
    "programstudents": ProgramStudentModel,
    "programmessages": ProgramStudentMessageModel,
    "acprograms_studentstates": ProgramStudentStateModel,

    "classificationlevels": ClassificationLevelModel,
    "classifications": ClassificationModel,
    "classificationtypes": ClassificationTypeModel,
    
    "subjects": SubjectModel,
    "semesters": SemesterModel,
    "topics": TopicModel,
    "lessons": LessonModel,
    "lessontypes": LessonTypeModel
}

def createLoaders(asyncSessionMaker, models=dbmodels):
    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
    attrs = {}
    for key, DBModel in models.items():
        attrs[key] = property(cache(createLambda(key, DBModel)))
    
    attrs["authorizations"] = property(cache(lambda self: AuthorizationLoader()))
    Loaders = type('Loaders', (), attrs)   
    return Loaders()

def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }

def createLoaders(asyncSessionMaker):

    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)

    attrs = {}

    for DBModel in BaseModel.registry.mappers:
        cls = DBModel.class_
        attrs[cls.__tablename__] = property(cache(createLambda(asyncSessionMaker, cls)))
    
    # attrs["authorizations"] = property(cache(lambda self: AuthorizationLoader()))
    Loaders = type('Loaders', (), attrs)   
    return Loaders()

def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }