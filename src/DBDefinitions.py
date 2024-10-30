import sqlalchemy
import datetime
from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    DateTime,
    ForeignKey,
    Sequence,
    Table,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
import uuid
from .uuid import UUIDColumn, UUIDFKey

BaseModel = declarative_base()

# id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
# primarni klice pojmenujte vzdy jako id
# cizi klice pojmenujte vzdy jako neco_id
# soucasti datove struktury by mely byt nejake polozky
# - lastchange
# - created
# - createdby
# - changedby
# - rbacobject
#

class ProgramModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence.
    
    Args:
            id: An primary key
    """
    
    __tablename__ = "acprograms"
    id = UUIDColumn()
    name = Column(String, comment="Matematika")
    name_en = Column(String, comment="Mathematics")
    type_id = Column(ForeignKey("acprogramtypes.id"), index=True)
    group_id = UUIDFKey(nullable=True, comment="Garants of the program")
    licenced_group_id = UUIDFKey(nullable=True, comment="Identifier for the faculty or school")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class ProgramTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence.
    
    Args:
            id: An primary key
    """
    
    __tablename__ = "acprogramtypes"
    id = UUIDColumn()
    name = Column(String, comment="Matematika")
    name_en = Column(String, comment=" Mathematics")
    form_id = Column(ForeignKey("acprogramforms.id"), index=True, comment="defines a form (distant, present)")
    language_id = Column(ForeignKey("acprogramlanguages.id"), index=True, comment="defines a language (Czech, English)")
    level_id = Column(ForeignKey("acprogramlevels.id"), index=True, comment="defines a level (Bacelor, Master, Doctoral, ... )")
    title_id = Column(ForeignKey("acprogramtitles.id"), index=True, comment="defined a title (Bc., MSc., Ph.D., ...)")
    # combination

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class ProgramStudentMessageModel(BaseModel):
    
    __tablename__ = "acprograms_studentmessages"
    id = UUIDColumn()
    name = Column(String)
    description = Column(String)
    student_id = UUIDFKey(nullable=False)
    program_id = Column(ForeignKey("acprograms.id"), index=True)
    date = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class ProgramStudentModel(BaseModel):
    
    __tablename__ = "acprograms_students"
    id = UUIDColumn()
    student_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    # state_id = Column(ForeignKey("acprograms_studentstates.id"), index=True)
    state_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    program_id = Column(ForeignKey("acprograms.id"), index=True)
    semester = Column(Integer)

    valid = Column(Boolean, default=lambda item: True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class ProgramStudentStateModel(BaseModel):
    
    __tablename__ = "acprograms_studentstates"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)
    
class ProgramFormTypeModel(BaseModel):
    
    """It encapsulates a study at university, like Cyber defence.
    
    Args:
            id: An primary key
    """
    __tablename__ = "acprogramforms"
    id = UUIDColumn()
    name = Column(String, comment="Presenční, dálkové, kombinované")
    name_en = Column(String, comment="Present, distant, hybrid")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class ProgramLanguageTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence.

    Args:
        id (ID): An primary key.
    """
    __tablename__ = "acprogramlanguages"
    id = UUIDColumn()
    name = Column(String, comment="Čeština, Angličtina")
    name_en = Column(String, comment="Czech, English")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class ProgramLevelTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence.

    Args:
        id (ID): An primary key.
    """
    __tablename__ = "acprogramlevels"
    id = UUIDColumn()
    name = Column(String, comment="Bakalář, Magist, Doktorant")
    name_en = Column(String, comment="Bachelor, Magister, Doctoral")
    length = Column(Integer, comment="leght of study")
    priority = Column(Integer, comment="allows to compare two programs and derive appropriate order... # 1 for Bc., 2 for Mgr. or NMgr., 3 for Ph.D.")  

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class ProgramTitleTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence.

    Args:
        id (ID): An primary key.
    """
    __tablename__ = "acprogramtitles"
    id = UUIDColumn()
    name = Column(String, comment="Bc., Mgr., Ing, ...")
    name_en = Column(String, comment="Bc., Mgr., Ing, ...")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)


class SubjectModel(BaseModel):
    """Could be a Mathematics.

    Args:
        id (ID): An primary key.
    """
    __tablename__ = "acsubjects"
    id = UUIDColumn()
    name = Column(String, comment="Matematika")
    name_en = Column(String, comment="Mathematics")
    program_id = Column(ForeignKey("acprograms.id"), index=True, comment="the program to which subject belongs")
    group_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

    # language_id = Column(ForeignKey('plan_subject_languages.id'))
    # program = relationship('StudyProgramModel', back_populates='subjects')
    # semesters = relationship('SemesterModel', back_populates='subject')
    # language = relationship('StudyLanguageModel', back_populates='subjects')

class SemesterModel(BaseModel):
    """Aka Mathematics, 2nd semester"""

    __tablename__ = "acsemesters"
    id = UUIDColumn()
    order = Column(Integer, comment="the semester to which subject belongs")
    credits = Column(Integer, comment="number of credicts for subject")
    subject_id = Column(ForeignKey("acsubjects.id"), index=True, comment="the subject to which semester belongs")
    classificationtype_id = Column(ForeignKey("acclassificationtypes.id"), index=True, comment="Zkouška, Klasifikovaný zápočet, Zápočet")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

    # subject = relationship('SubjectModel', back_populates='semesters')
    # classifications = relationship('ClassificationModel', back_populates='classificationsemesters')
    # themes = relationship('StudyThemesModel', back_populates='studysemesters')

class TopicModel(BaseModel):
    """Represents a topic within a semester.

    Args:
        id (UUID): An primary key.
    """

    __tablename__ = "actopics"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    order = Column(Integer)

    semester_id = Column(ForeignKey("acsemesters.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

    # studysemesters = relationship('SemesterModel', back_populates='themes')
    # items = relationship('StudyThemeItemModel', back_populates='theme')

class LessonModel(BaseModel):
    """Lecture, 2h,"""

    __tablename__ = "aclessons"
    id = UUIDColumn()
    topic_id = Column(ForeignKey("actopics.id"), index=True)
    type_id = Column(ForeignKey("aclessontypes.id"), index=True)
    count = Column(Integer)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

    # type = relationship('ThemeTypeModel', back_populates='items')
    # theme = relationship('StudyThemeModel', back_populates='items')

class ClassificationModel(BaseModel):
    """Holds a particular classification for a student.

    Args:
        id (ID): An primary key.
    """
    __tablename__ = "acclassifications"

    id = UUIDColumn()
    order = Column(Integer, comment="number for every attempt") #

    semester_id = Column(ForeignKey("acsemesters.id"), index=True)
    student_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True)
    #classificationtype_id = Column(ForeignKey("acclassificationtypes.id"), index=True, comment="Zkouška, Klasifikovaný zápočet, Zápočet")
    classificationlevel_id = Column(ForeignKey("acclassificationlevels.id"), index=True, comment="A, B, C, D, E, F")

    date = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class ClassificationLevelModel(BaseModel):
    """Holds a particular classification level (A, B, C, ...).

    Args:
        id (ID): An primary key.
    """
    __tablename__ = "acclassificationlevels"

    id = UUIDColumn()
    name = Column(String, comment="A, B, C, D, E, F")
    name_en = Column(String, comment="A, B, C, D, E, F")
    ordervalue = Column(Integer, comment="1, 2, 3, ...")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class ClassificationTypeModel(BaseModel):
    """ Holds a particular classification type (Zkouška, Klasifikovaný zápočet, Zápočet)."""
    
    __tablename__ = "acclassificationtypes"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    # classificationsemesters = relationship('SemesterModel', back_populates='classifications')

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class LessonTypeModel(BaseModel):
    """ Holds a particular lesson type (Lecture, Excercise, Laboratory, ...)."""
    __tablename__ = "aclessontypes"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    abbr = Column(String, comment="P, C, L, ... (shortcuts)")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of creation")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp of last update")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

    # items = relationship('StudyThemeItemModel', back_populates='type')




from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


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

    driver = "postgresql+asyncpg"  # "postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"
    connectionstring = os.environ.get("CONNECTION_STRING", connectionstring)

    return connectionstring
