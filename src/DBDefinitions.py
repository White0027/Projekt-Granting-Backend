import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase
from .uuid import UUIDColumn, UUIDFKey


class BaseModel(DeclarativeBase):
    """Base class for all models."""
    __abstract__ = True

    id = UUIDColumn()
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby_id = UUIDFKey(nullable=True, comment="Reference to the UUID of the user who created this record")
    changedby_id = UUIDFKey(nullable=True, comment="Reference to the UUID of the user who changed this record")
    rbacobject_id = UUIDFKey(nullable=True, comment="id rbacobject")

class ProgramModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence."""
    __tablename__ = "acprograms"

    name = Column(String, comment="Matematika")
    name_en = Column(String, comment="Mathematics")
    type_id = Column(ForeignKey("acprogramtypes.id"), index=True)
    group_id = UUIDFKey(nullable=True, comment="Garants of the program")
    licenced_group_id = UUIDFKey(nullable=True, comment="Identifier for the faculty or school")

class ProgramTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence."""
    __tablename__ = "acprogramtypes"

    name = Column(String, comment="Matematika")
    name_en = Column(String, comment="Mathematics")
    form_id = Column(ForeignKey("acprogramforms.id"), index=True, comment="defines a form (distant, present)")
    language_id = Column(ForeignKey("acprogramlanguages.id"), index=True, comment="defines a language (Czech, English)")
    level_id = Column(ForeignKey("acprogramlevels.id"), index=True, comment="defines a level (Bacelor, Master, Doctoral, ... )")
    title_id = Column(ForeignKey("acprogramtitles.id"), index=True, comment="defined a title (Bc., MSc., Ph.D., ...)")

class ProgramStudentMessageModel(BaseModel):
    """Represents a message associated with a student in a specific program."""
    __tablename__ = "acprograms_studentmessages"

    name = Column(String, comment="Name of the message") 
    description = Column(String, comment="Description of the message")
    student_id = UUIDFKey(nullable=True, comment="the student to which message belongs")
    program_id = Column(ForeignKey("acprograms.id"), index=True, comment="the program to which message belongs")
    date = Column(DateTime, server_default=sqlalchemy.sql.func.now())

class ProgramStudentModel(BaseModel):
    """Represents a student enrolled in a specific program."""
    __tablename__ = "acprograms_students"

    student_id = UUIDFKey(nullable=True, comment="Identifier for the student")
    state_id = UUIDFKey(nullable=True, comment="State of the program")
    program_id = Column(ForeignKey("acprograms.id"), index=True, comment="Identifier for the program")
    semester = Column(Integer, comment="Current semester")
    valid = Column(Boolean, default=lambda item: True)

class ProgramStudentStateModel(BaseModel):
    """Represents a state of a student in a specific program."""
    __tablename__ = "acprograms_studentstates"

    name = Column(String, comment="Name of the state")
    name_en = Column(String, comment="Name of the state in English")

class ProgramFormTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence."""
    __tablename__ = "acprogramforms"

    name = Column(String, comment="Presenční, dálkové, kombinované")
    name_en = Column(String, comment="Present, distant, hybrid")

class ProgramLanguageTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence."""
    __tablename__ = "acprogramlanguages"

    name = Column(String, comment="Čeština, Angličtina")
    name_en = Column(String, comment="Czech, English")

class ProgramLevelTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence."""
    __tablename__ = "acprogramlevels"

    name = Column(String, comment="Bakalář, Magist, Doktorant")
    name_en = Column(String, comment="Bachelor, Magister, Doctoral")
    length = Column(Integer, comment="leght of study")
    priority = Column(Integer, comment="allows to compare two programs and derive appropriate order... # 1 for Bc., 2 for Mgr. or NMgr., 3 for Ph.D.")  

class ProgramTitleTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence."""
    __tablename__ = "acprogramtitles"

    name = Column(String, comment="Bc., Mgr., Ing, ...")
    name_en = Column(String, comment="Bc., Mgr., Ing, ...")

class SubjectModel(BaseModel):
    """Could be a Mathematics."""
    __tablename__ = "acsubjects"

    name = Column(String, comment="Matematika")
    name_en = Column(String, comment="Mathematics")
    program_id = Column(ForeignKey("acprograms.id"), index=True, comment="the program to which subject belongs")
    group_id = UUIDFKey(nullable=True)

class SemesterModel(BaseModel):
    """Aka Mathematics, 2nd semester."""
    __tablename__ = "acsemesters"

    order = Column(Integer, comment="the semester to which subject belongs")
    credits = Column(Integer, comment="number of credicts for subject")
    subject_id = Column(ForeignKey("acsubjects.id"), index=True, comment="the subject to which semester belongs")
    classificationtype_id = Column(ForeignKey("acclassificationtypes.id"), index=True, comment="Zkouška, Klasifikovaný zápočet, Zápočet")

class TopicModel(BaseModel):
    """Represents a topic within a semester."""
    __tablename__ = "actopics"

    name = Column(String, comment="Name of the topic")
    name_en = Column(String, comment="Name of the topic in English")
    order = Column(Integer, comment="Order of the topic")
    semester_id = Column(ForeignKey("acsemesters.id"), index=True, comment="the semester to which topic belongs")

class LessonModel(BaseModel):
    """Lecture, 2h, 1st semester, Mathematics."""
    __tablename__ = "aclessons"

    name = Column(String, comment="Name of the lesson")
    name_en = Column(String, comment="Name of the lesson in English")
    topic_id = Column(ForeignKey("actopics.id"), index=True, comment="the topic to which lesson belongs")
    type_id = Column(ForeignKey("aclessontypes.id"), index=True, comment="Lecture, Excercise, Laboratory, ...")
    count = Column(Integer, comment="number of lessons")

class ClassificationModel(BaseModel):
    """Holds a particular classification for a student."""
    __tablename__ = "acclassifications"

    order = Column(Integer, comment="number for every attempt")
    semester_id = Column(ForeignKey("acsemesters.id"), index=True)
    student_id = UUIDFKey(nullable=True)
    classificationlevel_id = Column(ForeignKey("acclassificationlevels.id"), index=True, comment="A, B, C, D, E, F")
    date = Column(DateTime, server_default=sqlalchemy.sql.func.now())

class ClassificationLevelModel(BaseModel):
    """Holds a particular classification level (A, B, C, ...)."""
    __tablename__ = "acclassificationlevels"

    name = Column(String, comment="A, B, C, D, E, F")
    name_en = Column(String, comment="A, B, C, D, E, F")
    ordervalue = Column(Integer, comment="1, 2, 3, ...")

class ClassificationTypeModel(BaseModel):
    """Holds a particular classification type (Zkouška, Klasifikovaný zápočet, Zápočet)."""
    __tablename__ = "acclassificationtypes"

    name = Column(String, comment="Zkouška, Klasifikovaný zápočet, Zápočet")
    name_en = Column(String, comment="Exam, Classified credit, Credit")

class LessonTypeModel(BaseModel):
    """Holds a particular lesson type (Lecture, Excercise, Laboratory, ...)."""
    __tablename__ = "aclessontypes"

    name = Column(String)
    name_en = Column(String)
    abbr = Column(String, comment="P, C, L, ... (shortcuts)")

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker"""
    asyncEngine = create_async_engine(connectionstring)

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print("BaseModel.metadata.drop_all finished")
        if makeUp:
            await conn.run_sync(BaseModel.metadata.create_all)
            print("BaseModel.metadata.create_all finished")

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker

import os

def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
    Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database = os.environ.get("POSTGRES_DB", "data")
    hostWithPort = os.environ.get("POSTGRES_HOST", "localhost:5432")

    driver = "postgresql+asyncpg"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"
    connectionstring = os.environ.get("CONNECTION_STRING", connectionstring)

    return connectionstring