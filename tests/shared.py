import sqlalchemy
import asyncio
import pytest

async def prepare_in_memory_sqllite():
    # Vytvoří asynchronní SQLite engine a inicializuje databázi v paměti
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker

    from src.DBDefinitions import BaseModel

    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


async def prepare_demodata(async_session_maker):
    # Naplní databázi testovacími daty
    from src.DBFeeder import get_demodata
    from src.DBDefinitions import (
        ProgramFormTypeModel,
        ProgramLanguageTypeModel,
        ProgramLevelTypeModel,
        ProgramTitleTypeModel,
        ProgramTypeModel,
        ProgramModel,
        SubjectModel,
        SemesterModel,
        TopicModel,
        LessonModel,
        LessonTypeModel,
        ClassificationLevelModel,
        ClassificationModel,
        ClassificationTypeModel,
        ProgramStudentStateModel,
        ProgramStudentModel,
        ProgramStudentMessageModel
    )

    data = get_demodata()

    from uoishelpers.feeders import ImportModels

    dbModels = [
        ProgramFormTypeModel,
        ProgramLanguageTypeModel,
        ProgramLevelTypeModel,
        ProgramTitleTypeModel,
        ProgramTypeModel,
        ProgramModel,
        SubjectModel,
        SemesterModel,
        TopicModel,
        LessonModel,
        LessonTypeModel,
        ClassificationLevelModel,
        ClassificationModel,
        ClassificationTypeModel,
        ProgramStudentStateModel,
        ProgramStudentModel,
        ProgramStudentMessageModel
        ]

    await ImportModels(
        async_session_maker,
        dbModels,
        data,
    )
    # from src.DBFeeder import initDB
    # await initDB(asyncSessionMaker=async_session_maker)


async def createContext(asyncSessionMaker):
    # Vytvoří kontext s asynchronními session a dataloadery
    from Dataloaders import createLoaders_3
    return {
        "asyncSessionMaker": asyncSessionMaker,
        "all": await createLoaders_3(asyncSessionMaker),
    }