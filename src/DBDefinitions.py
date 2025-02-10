import sqlalchemy
import datetime
from sqlalchemy import Column, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass, Mapped, mapped_column

def UUIDFKey(ForeignKeyArg=None, **kwargs):
    newkwargs = {
        **kwargs,
        "index": True, 
        "primary_key": False, 
        "default": None,
        "nullable": True,
        "comment": "foreign key"
    }
    return mapped_column(**newkwargs)

def UUIDColumn(**kwargs):
    newkwargs = {
        **kwargs,
        "index": True, 
        "primary_key": True, 
        "default_factory": uuid.uuid4, 
        "comment": "primary key"
    }
    return mapped_column(**newkwargs)

class BaseModel(MappedAsDataclass, DeclarativeBase):
    id: Mapped[uuid.UUID] = UUIDColumn(index=True, primary_key=True, default_factory=uuid.uuid4)
    created: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True, server_default=sqlalchemy.sql.func.now(), comment="date time of creation")
    lastchange: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True, server_default=sqlalchemy.sql.func.now(), comment="date time stamp")
    createdby_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("users.id"), comment="id of user who created this entity")
    changedby_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("users.id"), comment="id of user who changed this entity")
    rbacobject_id: Mapped[uuid.UUID] = UUIDFKey(comment="id rbacobject")

class ProgramModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence."""
    __tablename__ = "acprograms"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Matematika")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="Mathematics")
    type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("acprogramtypes.id"), index=True, default=None, nullable=True, comment="defines a type (Cyber defence, ...)")
    group_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("acgroups.id"), comment="Garants of the program")
    licenced_group_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("acgroups.id"), index=True, default=None, nullable=True, comment="Identifier for the faculty or school")

class ProgramTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence."""
    __tablename__ = "acprogramtypes"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Matematika")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="Mathematics")
    form_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("acprogramforms.id"), index=True, default=None, nullable=True, comment="defines a form (distant, present)")
    language_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("acprogramlanguages.id"), index=True, default=None, nullable=True, comment="defines a language (Czech, English)")
    level_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("acprogramlevels.id"), index=True, default=None, nullable=True, comment="defines a level (Bachelor, Master, Doctoral, ... )")
    title_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("acprogramtitles.id"), index=True, default=None, nullable=True, comment="defined a title (Bc., MSc., Ph.D., ...)")

class ProgramStudentMessageModel(BaseModel):
    """Represents a message associated with a student in a specific program."""
    __tablename__ = "acprograms_studentmessages"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Name of the message")
    description: Mapped[str] = mapped_column(nullable=True, default=None, comment="Description of the message")
    student_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("acstudents.id"), comment="the student to which message belongs")
    program_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("acprograms.id"), index=True, default=None, nullable=True, comment="the program to which message belongs")
    date: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, server_default=sqlalchemy.sql.func.now())

class ProgramStudentModel(BaseModel):
    """Represents a student enrolled in a specific program."""
    __tablename__ = "acprograms_students"

    student_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("acstudents.id"), comment="Identifier for the student")
    state_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("acstudentstates.id"), comment="State of the program")
    program_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("acprograms.id"), index=True, default=None, nullable=True, comment="Identifier for the program")
    semester: Mapped[int] = mapped_column(nullable=True, default=None, comment="Current semester")
    valid: Mapped[bool] = mapped_column(nullable=True, default=None, comment="Is the student valid for the program")

class ProgramStudentStateModel(BaseModel):
    """Represents a state of a student in a specific program."""
    __tablename__ = "acprograms_studentstates"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Name of the state")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="Name of the state in English")

class ProgramFormTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence."""
    __tablename__ = "acprogramforms"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Presenční, dálkové, kombinované")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="Present, distant, hybrid")

class ProgramLanguageTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence."""
    __tablename__ = "acprogramlanguages"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Čeština, Angličtina")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="Czech, English")

class ProgramLevelTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence."""
    __tablename__ = "acprogramlevels"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Bakalář, Magist, Doktorant")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="Bachelor, Magister, Doctoral")
    length: Mapped[int] = mapped_column(nullable=True, default=None, comment="length of study")
    priority: Mapped[int] = mapped_column(nullable=True, default=None, comment="allows to compare two programs and derive appropriate order... # 1 for Bc., 2 for Mgr. or NMgr., 3 for Ph.D.")

class ProgramTitleTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence."""
    __tablename__ = "acprogramtitles"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Bc., Mgr., Ing, ...")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="Bc., Mgr., Ing, ...")

class SubjectModel(BaseModel):
    """Could be a Mathematics."""
    __tablename__ = "acsubjects"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Matematika")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="Mathematics")
    program_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("acprograms.id"), index=True, default=None, nullable=True, comment="the program to which subject belongs")
    group_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("acgroups.id"), comment="Garants of the subject")

class SemesterModel(BaseModel):
    """Aka Mathematics, 2nd semester."""
    __tablename__ = "acsemesters"

    order: Mapped[int] = mapped_column(nullable=True, default=None, comment="the semester to which subject belongs")
    credits: Mapped[int] = mapped_column(nullable=True, default=None, comment="number of credits for subject")
    subject_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("acsubjects.id"), index=True, default=None, nullable=True, comment="the subject to which semester belongs")
    classificationtype_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("acclassificationtypes.id"), index=True, default=None, nullable=True, comment="Exam, Classified credit, Credit")

class TopicModel(BaseModel):
    """Represents a topic within a semester."""
    __tablename__ = "actopics"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Name of the topic")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="Name of the topic in English")
    order: Mapped[int] = mapped_column(nullable=True, default=None, comment="Order of the topic")
    semester_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("acsemesters.id"), index=True, default=None, nullable=True, comment="the semester to which topic belongs")

class LessonModel(BaseModel):
    """Lecture, 2h, 1st semester, Mathematics."""
    __tablename__ = "aclessons"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Name of the lesson")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="Name of the lesson in English")
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("actopics.id"), index=True, default=None, nullable=True, comment="the topic to which lesson belongs")
    type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("aclessontypes.id"), index=True, default=None, nullable=True, comment="Lecture, Excercise, Laboratory, ...")
    count: Mapped[int] = mapped_column(nullable=True, default=None, comment="number of lessons")

class ClassificationModel(BaseModel):
    """Holds a particular classification for a student."""
    __tablename__ = "acclassifications"

    order: Mapped[int] = mapped_column(nullable=True, default=None, comment="number for every attempt")
    semester_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("acsemesters.id"), index=True, default=None, nullable=True, comment="the semester to which classification belongs")
    student_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("acstudents.id"), comment="the student to which classification belongs")
    classificationlevel_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("acclassificationlevels.id"), index=True, default=None, nullable=True, comment="A, B, C, D, E, F")
    date: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, server_default=sqlalchemy.sql.func.now())

class ClassificationLevelModel(BaseModel):
    """Holds a particular classification level (A, B, C, ...)."""
    __tablename__ = "acclassificationlevels"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="A, B, C, D, E, F")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="A, B, C, D, E, F")
    ordervalue: Mapped[int] = mapped_column(nullable=True, default=None, comment="1, 2, 3, ...")

class ClassificationTypeModel(BaseModel):
    """Holds a particular classification type (Zkouška, Klasifikovaný zápočet, Zápočet)."""
    __tablename__ = "acclassificationtypes"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Zkouška, Klasifikovaný zápočet, Zápočet")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="Exam, Classified credit, Credit")

class LessonTypeModel(BaseModel):
    """Holds a particular lesson type (Lecture, Excercise, Laboratory, ...)."""
    __tablename__ = "aclessontypes"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Lecture, Exercise, Laboratory, ...")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="Lecture, Exercise, Laboratory, ...")
    abbr: Mapped[str] = mapped_column(nullable=True, default=None, comment="P, C, L, ... (shortcuts)")

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

    return sessionmaker(asyncEngine, expire_on_commit=False, class_=AsyncSession)

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