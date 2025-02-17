import datetime
from typing import List, Union, Optional, Annotated, Any
from dataclasses import dataclass
import strawberry
from uoishelpers.resolvers import Insert, InsertError, Update, UpdateError, Delete, DeleteError
import typing
import uuid
from uoishelpers.resolvers import createInputs

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".GraphTypeDefinitionsExt")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".GraphTypeDefinitionsExt")]

from ._GraphPermissions import (
    OnlyForAuthentized
)
from ._GraphResolvers import (
    IDType,
    getLoadersFromInfo,
    resolve_reference,
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_lastchange,
    resolve_created,
    resolve_createdby,
    resolve_changedby,
    resolve_rbacobject,
    
    create_self_scalar_resolver,
    create_self_vector_resolver,

    asPage
    )

###########################################################################################################################
#
# zde definujte sve GQL modely
#
###########################################################################################################################

    
# region Program Model
@createInputs
@dataclass
class ProgramStudentInputFilter:
    student_id: IDType
    prorgam_id: IDType
    state_id: IDType
    semester: int
    valid: bool
    created: datetime.datetime
    lastchange: datetime.datetime


@strawberry.federation.type(
    keys=["id"], description="""Entity representing acredited study programs"""
)
class AcProgramGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).acprograms

    resolve_reference = resolve_reference
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    rbacobject = resolve_rbacobject
    _data: strawberry.Private[Any] = None

    @strawberry.field(
            description="""Bachelor, ...""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def type(self, info: strawberry.types.Info) -> Optional["AcProgramTypeGQLModel"]:
        return await AcProgramTypeGQLModel.resolve_reference(info, self.type_id)
        

    @strawberry.field(
            description="""subjects in the program""",
            permission_classes=[OnlyForAuthentized(isList=True)]
            )
    async def subjects(self, info: strawberry.types.Info) -> List["AcSubjectGQLModel"]:
        loader = AcSubjectGQLModel.getLoader(info)
        return await loader.filter_by(program_id=self.id)
        

    @strawberry.field(
            description="""subjects in the program""",
            permission_classes=[OnlyForAuthentized(isList=True)]
            )
    async def students(self, info: strawberry.types.Info, 
        skip: Optional[int] = 0,
        limit: Optional[int] = 10,
        where: Optional[ProgramStudentInputFilter] = None,
        orderby: Optional[str] = None,
        desc: Optional[bool] = None
        ) -> List["AcProgramStudentGQLModel"]:
        wheredict = None if where is None else strawberry.asdict(where)
        loader = AcProgramStudentGQLModel.getLoader(info)
        return await loader.page(skip=skip, limit=limit, where=wheredict, extendedfilter={"program_id": self.id}, orderby=orderby, desc=desc)
        # userawaitables = (UserGQLModel.resolve_reference(row.student_id) for row in rows)
        # return await asyncio.gather(*userawaitables)
        #

    @strawberry.field(
            description="""group defining grants of this program""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def grants_group(self, info: strawberry.types.Info) -> Optional["GroupGQLModel"]:
        from .GraphTypeDefinitionsExt import GroupGQLModel
        return await GroupGQLModel.resolve_reference(info=info, id=self.group_id)

    @strawberry.field(
            description="""group which has got licence to teach this program (faculty or university)""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def licenced_group(self, info: strawberry.types.Info) -> Optional["GroupGQLModel"]:
        from .GraphTypeDefinitionsExt import GroupGQLModel
        return await GroupGQLModel.resolve_reference(info=info, id=self.group_id)

# endregion
    
# region ProgramLevelType Model
@strawberry.federation.type(keys=["id"], description="bachelor, ...")
class AcProgramLevelTypeGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).acprogramlevels
        
    resolve_reference = resolve_reference
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data: strawberry.Private[Any] = None

# endregion
    
# region ProgramType Model
@strawberry.federation.type(
    keys=["id"],
    description="""Encapsulation of language, level, type etc. of program. This is intermediate entity for acredited program and its types""",
)
class AcProgramTypeGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).acprogramtypes
        
    resolve_reference = resolve_reference
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data: strawberry.Private[Any] = None

    @strawberry.field(
            description="""Bachelor, ...""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def level(self, info: strawberry.types.Info) -> Optional["AcProgramLevelTypeGQLModel"]:
        return await AcProgramLevelTypeGQLModel.resolve_reference(info, self.level_id)
        

    @strawberry.field(
            description="""Present, Distant, ...""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def form(self, info: strawberry.types.Info) -> Optional["AcProgramFormTypeGQLModel"]:
        return await AcProgramFormTypeGQLModel.resolve_reference(info, self.form_id)
        

    @strawberry.field(
            description="""Czech, ...""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def language(
        self, info: strawberry.types.Info
    ) -> Optional["AcProgramLanguageTypeGQLModel"]:
        return await AcProgramLanguageTypeGQLModel.resolve_reference(info, self.language_id)
        

    @strawberry.field(
            description="""Bc., Ing., ...""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def title(self, info: strawberry.types.Info) -> Optional["AcProgramTitleTypeGQLModel"]:
        return await AcProgramTitleTypeGQLModel.resolve_reference(info, self.title_id)
        
# endregion

# region ProgramMessage Model
@strawberry.federation.type(
    keys=["id"], description="""Entity representing acredited study programs"""
)
class AcProgramMessageGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).acprograms_studentmessages

    resolve_reference = resolve_reference
    id = resolve_id

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data: strawberry.Private[Any] = None

    name = resolve_name

    @strawberry.field(
            description="""extended content of the message""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def description(self) -> Optional[str]:
        return self.description

    @strawberry.field(
            description="""datetime of the message""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def date(self) -> Optional[datetime.datetime]:
        return self.date

    @strawberry.field(
            description="""student of the program""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def student(self, info: strawberry.types.Info) -> Optional["UserGQLModel"]:
        from .GraphTypeDefinitionsExt import UserGQLModel
        return await UserGQLModel.resolve_reference(info, id=self.student_id)

    @strawberry.field(
            description="""student of the program""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def program(self, info: strawberry.types.Info) -> Optional["AcProgramGQLModel"]:
        return await AcProgramGQLModel.resolve_reference(info, id=self.program_id)

# endregion
    
# region ProgramStudent Model
@createInputs
@dataclass
class ProgramMessagesInputFilter:
    name: str
    description: str
    date: datetime.datetime
    created: datetime.datetime
    lastchange: datetime.datetime

@strawberry.federation.type(
    keys=["id"], description="""Entity which links program and student"""
)
class AcProgramStudentGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).acprograms_students

    resolve_reference = resolve_reference
    id = resolve_id

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data = strawberry.Private[Any]


    @strawberry.field(
            description="""semester which student of the program is in""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def semester(self, info: strawberry.types.Info) -> Optional[int]:
        return self.semester or 0

    @strawberry.field(
            description="""student of the program""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def student(self, info: strawberry.types.Info) -> Optional["UserGQLModel"]:
        from .GraphTypeDefinitionsExt import UserGQLModel
        return await UserGQLModel.resolve_reference(info, id=self.student_id)
    
    @strawberry.field(
            description="""messages sent to the student regarding the program""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def messages(self, info: strawberry.types.Info, 
        skip: Optional[int] = 0,
        limit: Optional[int] = 10,
        where: Optional[ProgramMessagesInputFilter] = None,
        orderby: Optional[str] = None,
        desc: Optional[bool] = None
        ) -> List["AcProgramMessageGQLModel"]:

        wheredict = None if where is None else strawberry.asdict(where)
        loader = AcProgramMessageGQLModel.getLoader(info)
        results = await loader.page(
            skip=skip, limit=limit, orderby=orderby, desc=desc,
            where=wheredict, 
            extendedfilter={"program_id": self.program_id, "student_id": self.student_id} 
        )
        
        return results
    
    @strawberry.field(
            description="""student state in this program""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def state(self, info: strawberry.types.Info) -> Optional["AcProgramStudentStateGQLModel"]:
        return await AcProgramStudentStateGQLModel.resolve_reference(info=info, id=self.state_id)

    @strawberry.field(
            description="""program""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def program(self, info: strawberry.types.Info) -> Optional["AcProgramGQLModel"]:
        return await AcProgramGQLModel.resolve_reference(info=info, id=self.program_id)

# endregion
    
# region ProgramStudentState Model
@strawberry.federation.type(
    keys=["id"], description="""Entity which links program and student"""
)
class AcProgramStudentStateGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).acprograms_studentstates

    resolve_reference = resolve_reference
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data: strawberry.Private[Any] = None
# endregion
    
# region FormType Model
@strawberry.federation.type(
    keys=["id"], description="Program form type (Present, distant, ...)"
)
class AcProgramFormTypeGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).acprogramforms
        
    resolve_reference = resolve_reference
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data: strawberry.Private[Any] = None

# endregion
    
# region LanguageType Model
@strawberry.federation.type(keys=["id"], description="Study program language")
class AcProgramLanguageTypeGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).acprogramlanguages
        
    resolve_reference = resolve_reference
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data: strawberry.Private[Any] = None

# endregion
    
# region TitleType Model
@strawberry.federation.type(keys=["id"], description="Bc., Ing., ...")
class AcProgramTitleTypeGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).acprogramtitles
        
    resolve_reference = resolve_reference
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data: strawberry.Private[Any] = None

# endregion

# region ClassificationType Model
@strawberry.federation.type(
    keys=["id"], description="Classification at the end of semester"
)
class AcClassificationTypeGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).acclassificationtypes
        
    resolve_reference = resolve_reference
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data: strawberry.Private[Any] = None

# endregion
    
# region LessonType Model
@strawberry.federation.type(keys=["id"], description="P, C, LC, S, ...")
class AcLessonTypeGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).aclessontypes
        
    resolve_reference = resolve_reference
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data: strawberry.Private[Any] = None

# endregion
    
# region Subject Model
@strawberry.federation.type(
    keys=["id"],
    description="""Entity which connects programs and semesters, includes informations about subjects (divided into semesters)""",
)
class AcSubjectGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).acsubjects
        
    resolve_reference = resolve_reference
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    rbacobject = resolve_rbacobject
    
    _data: strawberry.Private[Any] = None

    @strawberry.field(
            description="""Program owing this subjects""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def program(self, info: strawberry.types.Info) -> "AcProgramGQLModel":
        return await AcProgramGQLModel.resolve_reference(info, self.program_id)
        

    @strawberry.field(
            description="""Semesters which the subjects in divided into""",
            permission_classes=[OnlyForAuthentized(isList=True)]
            )
    async def semesters(
        self, info: strawberry.types.Info
    ) -> List["AcSemesterGQLModel"]:
        loader = AcSemesterGQLModel.getLoader(info)
        return await loader.filter_by(subject_id=self.id)
        

    @strawberry.field(
            description="""group defining grants of this subject""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def grants(self, info: strawberry.types.Info) -> Optional["GroupGQLModel"]:
        from .GraphTypeDefinitionsExt import GroupGQLModel
        return await GroupGQLModel.resolve_reference(info=info, id=self.group_id)
        

# endregion
    
# region Semester Model
@createInputs
@dataclass
class ClassificationInputFilter:
    order: int
    semester_id: IDType
    user_id: IDType
    classificationlevel_id: IDType
    date: datetime.datetime
    pass

@strawberry.federation.type(
    keys=["id"], description="""Entity representing each semester in study subject"""
)
class AcSemesterGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).acsemesters
        
    resolve_reference = resolve_reference
    id = resolve_id

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data: strawberry.Private[Any] = None

    @strawberry.field(
            description="""semester number""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    def order(self) -> int:
        return self.order

    @strawberry.field(
            description="""Subject related to the semester (semester owner)""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def subject(self, info: strawberry.types.Info) -> Optional["AcSubjectGQLModel"]:
        return await AcSubjectGQLModel.resolve_reference(info, self.subject_id)
        

    @strawberry.field(
            description="""Subject related to the semester (semester owner)""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def classification_type(self, info: strawberry.types.Info) -> Optional["AcClassificationTypeGQLModel"]:
        return await AcClassificationTypeGQLModel.resolve_reference(info, self.classificationtype_id)
        

    @strawberry.field(
            description="""Final classification of the semester""",
            permission_classes=[OnlyForAuthentized(isList=True)]
            )
    async def classifications(
        self, info: strawberry.types.Info,
        skip: Optional[int] = 0,
        limit: Optional[int] = 10,
        where: Optional[ClassificationInputFilter] = None,
        orderby: Optional[str] = None,
        desc: Optional[bool] = None
    ) -> List["AcClassificationGQLModel"]:
        #loader = getLoadersFromInfo(info).acclassification_for_semester
        wheredict = None if where is None else strawberry.asdict(where)
        loader = AcClassificationGQLModel.getLoader(info)
        return await loader.page(
            skip = skip, limit = limit, orderby = orderby, desc = desc,
            where = wheredict, extendedfilter={"semester_id": self.id}
        )
        

    @strawberry.field(
            description="""topics""",
            permission_classes=[OnlyForAuthentized(isList=True)]
            )
    async def topics(self, info: strawberry.types.Info) -> List["AcTopicGQLModel"]:
        loader = AcTopicGQLModel.getLoader(info)
        return await loader.filter_by(semester_id=self.id)
        


# endregion
    
# region Topic Model
@strawberry.federation.type(
    keys=["id"],
    description="""Entity which represents a theme included in semester of subject""",
)
class AcTopicGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).actopics
        
    resolve_reference = resolve_reference
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data: strawberry.Private[Any] = None

    @strawberry.field(
            description="""order (1)""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    def order(self) -> Union[int, None]:
        return self.order

    @strawberry.field(
            description="""Semester of subject which owns the topic""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def semester(self, info: strawberry.types.Info) -> Optional["AcSemesterGQLModel"]:
        return await AcSemesterGQLModel.resolve_reference(info, self.semester_id)
        

    @strawberry.field(
            description="""Lessons for a topic""",
            permission_classes=[OnlyForAuthentized(isList=True)]
            )
    async def lessons(self, info: strawberry.types.Info) -> List["AcLessonGQLModel"]:
        loader = AcLessonGQLModel.getLoader(info)
        return await loader.filter_by(topic_id=self.id)
        

# endregion
    
# region Lesson Model
@strawberry.federation.type(
    keys=["id"],
    description="""Entity which represents single lesson included in a topic""",
)
class AcLessonGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).aclessons
        
    resolve_reference = resolve_reference
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data: strawberry.Private[Any] = None

    @strawberry.field(
            description="""Lesson type""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def type(self, info: strawberry.types.Info) -> Optional["AcLessonTypeGQLModel"]:
        return await AcLessonTypeGQLModel.resolve_reference(info, self.type_id)
        

    @strawberry.field(
            description="""Number of hour of this lesson in the topic""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    def count(self) -> int:
        return self.count

    @strawberry.field(
            description="""The topic which owns this lesson""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def topic(self, info: strawberry.types.Info) -> Optional["AcTopicGQLModel"]:
        return await AcTopicGQLModel.resolve_reference(info, self.topic_id)
        

# endregion
    
# region Classification
@strawberry.federation.type(
    keys=["id"],
    description="""Entity which holds a exam result for a subject semester and user / student""",
)
class AcClassificationGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).acclassifications
        
    resolve_reference = resolve_reference
    id = resolve_id

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data: strawberry.Private[Any] = None

    @strawberry.field(
            description="""datetime of classification""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    def date(self) -> datetime.datetime:
        return self.date

    @strawberry.field(
            description="""ORDER OF CLASSI""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    def order(self) -> Optional[int]:
        return self.order

    @strawberry.field(
            description="""User""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def student(self, info: strawberry.types.Info) -> Optional["UserGQLModel"]:
        from .GraphTypeDefinitionsExt import UserGQLModel
        return await UserGQLModel.resolve_reference(info=info, id=self.student_id)

    @strawberry.field(
            description="""Semester""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def semester(self, info: strawberry.types.Info) -> Optional["AcSemesterGQLModel"]:
        return await AcSemesterGQLModel.resolve_reference(info, id=self.semester_id)
        

    @strawberry.field(
            description="""Level""",
            permission_classes=[OnlyForAuthentized(isList=False)]
            )
    async def level(self, info: strawberry.types.Info) -> Optional["AcClassificationLevelGQLModel"]:
        return await AcClassificationLevelGQLModel.resolve_reference(info, id=self.classificationlevel_id)
        

# endregion
    
# region ClassificationLevel 
@strawberry.federation.type(
    keys=["id"],
    description="""Mark which student could get as an exam evaluation""",
)
class AcClassificationLevelGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).acclassificationlevels
        
    resolve_reference = resolve_reference
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    createdby = resolve_createdby
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    _data: strawberry.Private[Any] = None

# endregion

###########################################################################################################################
#
# zde definujte resolvery pro svuj Query model
#
###########################################################################################################################


# region ProgramTitleType ById, Page
@createInputs
@dataclass
class ProgramTitleTypeInputFilter:
    name: str
    name_en: str

@strawberry.field(
    description="""Gets program paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def program_title_type_page(self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10, 
                       where: Optional[ProgramTitleTypeInputFilter] = None) -> List["AcProgramTitleTypeGQLModel"]:
    return AcProgramTitleTypeGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets program by id""",
    permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_title_type_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcProgramTitleTypeGQLModel"]:
    return await AcProgramTitleTypeGQLModel.resolve_reference(info=info, id=id)

# endregion

# region ProgramLevelType ById, Page
@createInputs
@dataclass
class ProgramLevelTypeInputFilter:
    name: str
    name_en: str

@strawberry.field(
    description="""Gets program paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=False)]
    )
@asPage
async def program_level_type_page(self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10, 
                       where: Optional[ProgramLevelTypeInputFilter] = None) -> List["AcProgramLevelTypeGQLModel"]:
    return AcProgramLevelTypeGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets program by id""",
    permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_level_type_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcProgramLevelTypeGQLModel"]:
    return await AcProgramLevelTypeGQLModel.resolve_reference(info=info, id=id)

# endregion

# region ProgramFormType ById, Page
@createInputs
@dataclass
class ProgramFormTypeInputFilter:
    name: str
    name_en: str

@strawberry.field(
    description="""Gets program paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def program_form_type_page(self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10, 
                       where: Optional[ProgramFormTypeInputFilter] = None) -> List["AcProgramFormTypeGQLModel"]:
    return AcProgramFormTypeGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets program by id""",
    permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_form_type_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcProgramFormTypeGQLModel"]:
    return await AcProgramFormTypeGQLModel.resolve_reference(info=info, id=id)

# endregion

# region ProgramLanguageType ById, Page
@createInputs
@dataclass
class ProgramLanguageTypeInputFilter:
    name: str
    name_en: str

@strawberry.field(
    description="""Gets program paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def program_language_type_page(self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10, 
                       where: Optional[ProgramLanguageTypeInputFilter] = None) -> List["AcProgramLanguageTypeGQLModel"]:
    return AcProgramLanguageTypeGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets program by id""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
async def program_language_type_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcProgramLanguageTypeGQLModel"]:
    return await AcProgramLanguageTypeGQLModel.resolve_reference(info=info, id=id)

# endregion

# region ProgramType ById, Page
@createInputs
@dataclass
class ProgramTypeInputFilter:
    name: str
    name_en: str

@strawberry.field(
    description="""Gets program paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def program_type_page(self, info: strawberry.types.Info, 
                       skip: Optional[int] = 0, limit: Optional[int] = 10, where: Optional[ProgramTypeInputFilter] = None) -> List["AcProgramTypeGQLModel"]:
    return AcProgramTypeGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets program paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
async def program_type_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcProgramTypeGQLModel"]:
    return await AcProgramTypeGQLModel.resolve_reference(info=info, id=id)

# endregion

# region Program ById, Page
@createInputs
@dataclass
class ProgramInputFilter:
    name: str
    name_en: str

@strawberry.field(
    description="""Gets program paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def program_page(self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10, where: Optional[ProgramInputFilter] = None) -> List["AcProgramGQLModel"]:
    return AcProgramGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets program paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
async def program_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcProgramGQLModel"]:
    return await AcProgramGQLModel.resolve_reference(info=info, id=id)
# endregion

# region Subject ById, Page

@createInputs
@dataclass
class SubjectInputFilter:
    name: str
    name_en: str

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def subject_page(self, info: strawberry.types.Info, 
                       skip: Optional[int] = 0, limit: Optional[int] = 10, 
                       where: Optional[SubjectInputFilter] = None) -> List["AcSubjectGQLModel"]:
    return AcSubjectGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
async def subject_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcSubjectGQLModel"]:
    return await AcSubjectGQLModel.resolve_reference(info=info, id=id)

# endregion

# region Semester ById, Page
@createInputs
@dataclass
class SemesterInputFilter:
    pass

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def semester_page(self, info: strawberry.types.Info, 
                       skip: Optional[int] = 0, limit: Optional[int] = 10, 
                       where: Optional[SemesterInputFilter] = None) -> List["AcSemesterGQLModel"]:
    return AcSemesterGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
async def semester_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcSemesterGQLModel"]:
    return await AcSemesterGQLModel.resolve_reference(info=info, id=id)

# endregion

# region Topic ById, Page
@createInputs
@dataclass
class TopicInputFilter:
    name: str
    pass

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def topic_page(self, info: strawberry.types.Info, 
                       skip: Optional[int] = 0, limit: Optional[int] = 10, 
                       where: Optional[TopicInputFilter] = None) -> List["AcTopicGQLModel"]:
    return AcTopicGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
async def topic_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcTopicGQLModel"]:
    return await AcTopicGQLModel.resolve_reference(info=info, id=id)

# endregion

# region Lesson ById, Page
@createInputs
@dataclass
class LessonInputFilter:
    name: str
    pass

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def lesson_page(self, info: strawberry.types.Info, 
                       skip: Optional[int] = 0, limit: Optional[int] = 10, 
                       where: Optional[LessonInputFilter] = None) -> List["AcLessonGQLModel"]:
    return AcLessonGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
async def lesson_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcLessonGQLModel"]:
    return await AcLessonGQLModel.resolve_reference(info=info, id=id)

# endregion

# region Classification ById, Page

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def classification_page(self, info: strawberry.types.Info, 
                       skip: Optional[int] = 0, limit: Optional[int] = 10, 
                       where: Optional[ClassificationInputFilter] = None) -> List["AcClassificationGQLModel"]:
    return AcClassificationGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
async def classification_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcClassificationGQLModel"]:
    return await AcClassificationGQLModel.resolve_reference(info=info, id=id)

# endregion

# region ClassificationLevel ById, Page

@createInputs
@dataclass
class ClassificationLevelInputFilter:
    # name: str
    pass

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def classification_level_page(self, info: strawberry.types.Info, 
                       skip: Optional[int] = 0, limit: Optional[int] = 10, 
                       where: Optional[TopicInputFilter] = None) -> List["AcClassificationLevelGQLModel"]:
    return AcClassificationLevelGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
async def classification_level_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcClassificationLevelGQLModel"]:
    return await AcClassificationLevelGQLModel.resolve_reference(info=info, id=id)
# endregion

# region ClassificationType ById, Page

@createInputs
@dataclass
class ClassificationTypeInputFilter:
    # name: str
    pass

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def classification_type_page(self, info: strawberry.types.Info, 
                       skip: Optional[int] = 0, limit: Optional[int] = 10, 
                       where: Optional[TopicInputFilter] = None) -> List["AcClassificationTypeGQLModel"]:
    return AcClassificationTypeGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
async def classification_type_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcClassificationTypeGQLModel"]:
    return await AcClassificationTypeGQLModel.resolve_reference(info=info, id=id)
# endregion

# region LessonType ById, Page

@createInputs
@dataclass
class LessonTypeInputFilter:
    # name: str
    pass

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def lesson_type_page(self, info: strawberry.types.Info, 
        skip: Optional[int] = 0, limit: Optional[int] = 10, 
        where: Optional[LessonTypeInputFilter] = None) -> List["AcLessonTypeGQLModel"]:
    return AcLessonTypeGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
async def lesson_type_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcLessonTypeGQLModel"]:
    return await AcLessonTypeGQLModel.resolve_reference(info=info, id=id)
# endregion

# region StudentState ById, Page

@createInputs
@dataclass
class StudentStateInputFilter:
    # name: str
    pass

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def student_state_page(self, info: strawberry.types.Info, 
                       skip: Optional[int] = 0, limit: Optional[int] = 10, 
                       where: Optional[StudentStateInputFilter] = None) -> List["AcProgramStudentStateGQLModel"]:
    return AcProgramStudentStateGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
async def student_state_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcProgramStudentStateGQLModel"]:
    return await AcProgramStudentStateGQLModel.resolve_reference(info=info, id=id)
# endregion


# region ProgramStudentState ById, Page

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def student_page(self, info: strawberry.types.Info, 
                       skip: Optional[int] = 0, limit: Optional[int] = 10, 
                       where: Optional[ProgramStudentInputFilter] = None) -> List["AcProgramStudentGQLModel"]:
    return AcProgramStudentGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
async def student_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcProgramStudentGQLModel"]:
    return await AcProgramStudentGQLModel.resolve_reference(info=info, id=id)
# endregion

# region ProgramMessage ById, Page

@createInputs
@dataclass
class ProgramMessageInputFilter:
    student_id: IDType

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
@asPage
async def message_page(self, info: strawberry.types.Info, 
                       skip: Optional[int] = 0, limit: Optional[int] = 10, 
                       where: Optional[ProgramMessageInputFilter] = None) -> List["AcProgramMessageGQLModel"]:
    return AcProgramMessageGQLModel.getLoader(info)

@strawberry.field(
    description="""Gets subjects paged / filtered""",
    permission_classes=[OnlyForAuthentized(isList=True)]
    )
async def message_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["AcProgramMessageGQLModel"]:
    return await AcProgramMessageGQLModel.resolve_reference(info=info, id=id)
# endregion


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

# region Query Class
@strawberry.type(description="""Type for query root""")
class Query:

    ac_program_by_id = program_by_id
    ac_program_page = program_page
    
    ac_program_type_by_id = program_type_by_id
    ac_program_type_page = program_type_page

    ac_program_title_type_by_id = program_title_type_by_id
    ac_program_title_type_page = program_title_type_page

    ac_program_language_type_by_id = program_language_type_by_id
    ac_program_language_type_page = program_language_type_page

    ac_program_level_type_by_id = program_level_type_by_id
    ac_program_level_type_page = program_level_type_page

    ac_program_form_type_by_id = program_form_type_by_id
    ac_program_form_type_page = program_form_type_page

    ac_subject_by_id = subject_by_id
    ac_subject_page = subject_page

    ac_semester_by_id = semester_by_id
    ac_semester_page = semester_page

    ac_topic_by_id = topic_by_id
    ac_topic_page = topic_page

    ac_lesson_by_id = lesson_by_id
    ac_lesson_page = lesson_page

    ac_classification_by_id = classification_by_id
    ac_classification_page = classification_page

    ac_classification_level_by_id = classification_level_by_id
    ac_classification_level_page = classification_level_page

    ac_classification_type_by_id = classification_type_by_id
    ac_classification_type_page = classification_type_page

    ac_lesson_type_by_id = lesson_type_by_id
    ac_lesson_type_page = lesson_type_page

    ac_program_student_state_by_id = student_state_by_id
    ac_program_student_state_page = student_state_page

    ac_program_student_by_id = student_by_id
    ac_program_student_page = student_page

    ac_program_message_page = message_page
    ac_program_message_by_id = message_by_id

    @strawberry.field(description="""Just container gql test""")
    async def say_hello_granting(self, info: strawberry.types.Info, id: Optional[str] = "Unknown User") -> Union[str, None]:
        return f"Hello {id} from granting"
# endregion

###########################################################################################################################
#
#
# Mutations - resolvers
#
#
###########################################################################################################################

# region Program CU
@strawberry.input(description="Model for initialization during C operation")
class ProgramInsertGQLModel:
    name: str
    type_id: IDType
    group_id: IDType = strawberry.field(description="group of / for grants, mastergroup must be licenced_group_id")
    licenced_group_id: IDType = strawberry.field(description="faculty / university")
    id: Optional[IDType] = None
    name_en: Optional[str] = ""
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None
    pass

@strawberry.input(description="Model for definition of D operation")
class ProgramUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    type_id: Optional[IDType] = None
    changedby: strawberry.Private[IDType] = None

@strawberry.input(description="Attributes for deletion")
class ProgramDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

@strawberry.type(description="Result of CUD operations")
class ProgramResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Object of operations""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def program(self, info: strawberry.types.Info) -> Union[AcProgramGQLModel, None]:
        return await AcProgramGQLModel.resolve_reference(info, self.id)
    
@strawberry.mutation(
        description="""Adds new study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_insert(self, info: strawberry.types.Info, program: ProgramInsertGQLModel) -> Union[AcProgramGQLModel, InsertError[AcProgramGQLModel]]:
    program.rbacobject = program.group_id
    return await Insert [AcProgramGQLModel].DoItSafeWay(info=info, entity=program)

@strawberry.mutation(
        description="""Update the study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_update(self, info: strawberry.types.Info, program: ProgramUpdateGQLModel) -> Union[AcProgramGQLModel, UpdateError[AcProgramGQLModel]]:
    return await Update [AcProgramGQLModel].DoItSafeWay(info=info, entity=program)

@strawberry.mutation(
        description="""Delete the program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_delete(self, info: strawberry.types.Info, program: ProgramDeleteGQLModel) -> typing.Optional[DeleteError[AcProgramGQLModel]]:
    return await Delete[AcProgramGQLModel].DoItSafeWay(info=info, entity= program)


# endregion

# region ProgramType CU
@strawberry.input(description="Model for initialization during C operation")
class ProgramTypeInsertGQLModel:
    name: str
    name_en: Optional[str] = ""
    language_id: IDType
    level_id: IDType
    form_id: IDType
    title_id: IDType
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of D operation")
class ProgramTypeUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    language_id: Optional[IDType] = None
    level_id: Optional[IDType] = None
    form_id: Optional[IDType] = None
    title_id: Optional[IDType] = None
    changedby: strawberry.Private[IDType] = None
    
@strawberry.input(description="Attributes for deletion")
class ProgramTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")   

@strawberry.type(description="Result of CUD operations")
class ProgramTypeResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Result of user operation""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def program_type(self, info: strawberry.types.Info) -> Union[AcProgramTypeGQLModel, None]:
        return await AcProgramTypeGQLModel.resolve_reference(info, self.id)
        

@strawberry.mutation(
        description="""Insert the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_type_insert(self, info: strawberry.types.Info, program_type: ProgramTypeInsertGQLModel) -> Union[AcProgramTypeGQLModel, InsertError[AcProgramTypeGQLModel]]:
    return await Insert[AcProgramTypeGQLModel].DoItSafeWay(info=info, entity=program_type)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_type_update(self, info: strawberry.types.Info, program_type: ProgramTypeUpdateGQLModel) -> Union[AcProgramTypeGQLModel, UpdateError[AcProgramTypeGQLModel]]:
    return await Update[AcProgramTypeGQLModel].DoItSafeWay(info=info, entity=program_type)
    

@strawberry.mutation(
        description="""Delete the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_type_delete(self, info: strawberry.types.Info, program_type: ProgramTypeDeleteGQLModel) -> typing.Optional[DeleteError[AcProgramTypeGQLModel]]:
    return await Delete[AcProgramTypeGQLModel].DoItSafeWay(info=info, entity=program_type)

# endregion

# region ProgramLanguageType CU

@strawberry.input(description="Model for initialization during C operation")
class ProgramLanguageTypeInsertGQLModel:
    name: str
    name_en: Optional[str] = ""
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of D operation")
class ProgramLanguageTypeUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None  

@strawberry.input(description="Attributes for deletion")
class ProgramLanguageTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

@strawberry.type(description="Result of CUD operations")
class ProgramLanguageTypeResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Result of user operation""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def program_language_type(self, info: strawberry.types.Info) -> Optional[AcProgramLanguageTypeGQLModel]:
        return await AcProgramLanguageTypeGQLModel.resolve_reference(info, self.id)
    
@strawberry.mutation(
        description="""Insert the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_language_type_insert(self, info: strawberry.types.Info, language_type: ProgramLanguageTypeInsertGQLModel) -> Union[AcProgramLanguageTypeGQLModel, InsertError[AcProgramLanguageTypeGQLModel]]:
    return await Insert[AcProgramLanguageTypeGQLModel].DoItSafeWay(info=info, entity=language_type)

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_language_type_update(self, info: strawberry.types.Info, language_type: ProgramLanguageTypeUpdateGQLModel) -> Union[AcProgramLanguageTypeGQLModel, UpdateError[AcProgramLanguageTypeGQLModel]]:
    return await Update[AcProgramLanguageTypeGQLModel].DoItSafeWay(info=info, entity=language_type)
    

@strawberry.mutation(
        description="""Delete the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_language_type_delete(self, info: strawberry.types.Info, language_type: ProgramLanguageTypeDeleteGQLModel) -> typing.Optional[DeleteError[AcProgramLanguageTypeGQLModel]]:
    return await Delete[AcProgramLanguageTypeGQLModel].DoItSafeWay(info=info, entity=language_type)
    

# endregion

# region ProgramTitleType CU
@strawberry.input(description="Model for initialization during C operation")
class ProgramTitleTypeInsertGQLModel:
    name: str
    name_en: Optional[str] = ""
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of D operation")
class ProgramTitleTypeUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None
    
@strawberry.input(description="Attributes for deletion")
class ProgramTitleTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")   

@strawberry.type(description="Result of CUD operations")
class ProgramTitleTypeResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Result of user operation""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def program_title_type(self, info: strawberry.types.Info) -> Optional[AcProgramTitleTypeGQLModel]:
        return await AcProgramTitleTypeGQLModel.resolve_reference(info, self.id)
        

@strawberry.mutation(
        description="""Insert the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_title_type_insert(self, info: strawberry.types.Info, title_type: ProgramTitleTypeInsertGQLModel) -> Union[AcProgramTitleTypeGQLModel, InsertError[AcProgramTitleTypeGQLModel]]:
    return await Insert[AcProgramTitleTypeGQLModel].DoItSafeWay(info=info, entity=title_type)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_title_type_update(self, info: strawberry.types.Info, title_type: ProgramTitleTypeUpdateGQLModel) -> Union[AcProgramTitleTypeGQLModel, UpdateError[AcProgramTitleTypeGQLModel]]:
    return await Update[AcProgramTitleTypeGQLModel].DoItSafeWay(info=info, entity=title_type)
    

@strawberry.mutation(
        description="""Delete the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_title_type_delete(self, info: strawberry.types.Info, title_type: ProgramTitleTypeDeleteGQLModel) -> typing.Optional[DeleteError[AcProgramTitleTypeGQLModel]]:
    return await Delete[AcProgramTitleTypeGQLModel].DoItSafeWay(info=info, entity=title_type)
    

# endregion

# region ProgramLevelType CU

@strawberry.input(description="Model for initialization during C operation")
class ProgramLevelTypeInsertGQLModel:
    name: str
    name_en: Optional[str] = ""
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of D operation")
class ProgramLevelTypeUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None 

@strawberry.input(description="Attributes for deletion")
class ProgramLevelTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")  

@strawberry.type(description="Result of CUD operations")
class ProgramLevelTypeResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Result of user operation""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def program_level_type(self, info: strawberry.types.Info) -> Optional[AcProgramLevelTypeGQLModel]:
        return await AcProgramLevelTypeGQLModel.resolve_reference(info, self.id)
        

@strawberry.mutation(
        description="""Insert the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_level_type_insert(self, info: strawberry.types.Info, level_type: ProgramLevelTypeInsertGQLModel) -> Union[AcProgramLevelTypeGQLModel, InsertError[AcProgramLevelTypeGQLModel]]:
    return await Insert[AcProgramLevelTypeGQLModel].DoItSafeWay(info=info, entity=level_type)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_level_type_update(self, info: strawberry.types.Info, level_type: ProgramLevelTypeUpdateGQLModel) -> Union[AcProgramLevelTypeGQLModel, UpdateError[AcProgramLevelTypeGQLModel]]:
    return await Update[AcProgramLevelTypeGQLModel].DoItSafeWay(info=info, entity=level_type)
    

@strawberry.mutation(
        description="""Delete the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_level_type_delete(self, info: strawberry.types.Info, level_type: ProgramLevelTypeDeleteGQLModel) -> typing.Optional[DeleteError[AcProgramLevelTypeGQLModel]]:
    return await Delete[AcProgramLevelTypeGQLModel].DoItSafeWay(info=info, entity=level_type)
    

# endregion

# region ProgramFormType CU

@strawberry.input(description="Model for initialization during C operation")
class ProgramFormTypeInsertGQLModel:
    name: str
    name_en: Optional[str] = ""
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of D operation")
class ProgramFormTypeUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None
    
@strawberry.input(description="Attributes for deletion")
class ProgramFormTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")   

@strawberry.type(description="Result of CUD operations")
class ProgramFormTypeResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Result of user operation""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def program_form_type(self, info: strawberry.types.Info) -> Optional[AcProgramFormTypeGQLModel]:
        return await AcProgramFormTypeGQLModel.resolve_reference(info, self.id)
        

@strawberry.mutation(
        description="""Insert the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_form_type_insert(self, info: strawberry.types.Info, form_type: ProgramFormTypeInsertGQLModel) -> Union[AcProgramFormTypeGQLModel, InsertError[AcProgramFormTypeGQLModel]]:
    return await Insert[AcProgramFormTypeGQLModel].DoItSafeWay(info=info, entity=form_type)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_form_type_update(self, info: strawberry.types.Info, form_type: ProgramFormTypeUpdateGQLModel) -> Union[AcProgramFormTypeGQLModel, UpdateError[AcProgramFormTypeGQLModel]]:
    return await Update[AcProgramFormTypeGQLModel].DoItSafeWay(info=info, entity=form_type)
    

@strawberry.mutation(
        description="""Delete the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_form_type_delete(self, info: strawberry.types.Info, form_type: ProgramFormTypeDeleteGQLModel) -> typing.Optional[DeleteError[AcProgramFormTypeGQLModel]]:
    return await Delete[AcProgramFormTypeGQLModel].DoItSafeWay(info=info, entity=form_type)
    

# endregion

# region ProgramStudentMessage CU

@strawberry.input(description="Model for initialization during C operation")
class ProgramMessageInsertGQLModel:
    name: str
    student_id: IDType
    program_id: IDType
    date: datetime.datetime
    description: Optional[str] = "Popis"
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of D operation")
class ProgramMessageUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    date: Optional[datetime.datetime] = None
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None
    
@strawberry.input(description="Attributes for deletion")
class ProgramMessageDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")   

@strawberry.type(description="Result of CUD operations")
class ProgramMessageResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Result of user operation""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def message(self, info: strawberry.types.Info) -> Optional[AcProgramMessageGQLModel]:
        return await AcProgramMessageGQLModel.resolve_reference(info, self.id)
        

@strawberry.mutation(
        description="""Insert the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_message_insert(self, info: strawberry.types.Info, message: ProgramMessageInsertGQLModel) -> Union[AcProgramMessageGQLModel, InsertError[AcProgramMessageGQLModel]]:
    return await Insert[AcProgramMessageGQLModel].DoItSafeWay(info=info, entity=message)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_message_update(self, info: strawberry.types.Info, message: ProgramMessageUpdateGQLModel) -> Union[AcProgramMessageGQLModel, UpdateError[AcProgramMessageGQLModel]]:
    return await Update[AcProgramMessageGQLModel].DoItSafeWay(info=info, entity=message)
    

@strawberry.mutation(
        description="""Delete the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_message_delete(self, info: strawberry.types.Info, message: ProgramMessageDeleteGQLModel) -> typing.Optional[DeleteError[AcProgramMessageGQLModel]]:
    return await Delete[AcProgramMessageGQLModel].DoItSafeWay(info=info, entity=message)
    

# endregion

# region ProgramStudent CU

@strawberry.input(description="Model for initialization during C operation")
class ProgramStudentInsertGQLModel:
    student_id: IDType
    program_id: IDType
    state_id: IDType
    semester: Optional[int] = 1
    valid: Optional[bool] = True
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of D operation")
class ProgramStudentUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    state_id: Optional[IDType] = None
    semester: Optional[int] = None
    valid: Optional[bool] = None
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None  
    
@strawberry.input(description="Attributes for deletion")
class ProgramStudentDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking") 

@strawberry.type(description="Result of CUD operations")
class ProgramStudentResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Result of user operation""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def student(self, info: strawberry.types.Info) -> Optional[AcProgramStudentGQLModel]:
        return await AcProgramStudentGQLModel.resolve_reference(info, self.id)
        

@strawberry.mutation(
        description="""Insert the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_student_insert(self, info: strawberry.types.Info, student: ProgramStudentInsertGQLModel) -> Union[AcProgramStudentGQLModel, InsertError[AcProgramStudentGQLModel]]:
    return await Insert[AcProgramStudentGQLModel].DoItSafeWay(info=info, entity=student)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_student_update(self, info: strawberry.types.Info, student: ProgramStudentUpdateGQLModel) -> Union[AcProgramStudentGQLModel, UpdateError[AcProgramStudentGQLModel]]:
    return await Update[AcProgramStudentGQLModel].DoItSafeWay(info=info, entity=student)
    

@strawberry.mutation(
        description="""Delete the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_student_delete(self, info: strawberry.types.Info, student: ProgramStudentDeleteGQLModel) -> typing.Optional[DeleteError[AcProgramStudentGQLModel]]:
    return await Delete[AcProgramStudentGQLModel].DoItSafeWay(info=info, entity=student)
    

# endregion

# region Subject CU

@strawberry.input(description="Model for initialization during C operation")
class SubjectInsertGQLModel:
    name: str
    program_id: IDType
    group_id: IDType = strawberry.field(description="group of / for grants, its mastergroup must be group of grants for program")
    name_en: Optional[str] = ""
    id: Optional[IDType] = None
    valid: Optional[bool] = True
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of D operation")
class SubjectUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    valid: Optional[bool] = None
    changedby: strawberry.Private[IDType] = None
    
@strawberry.input(description="Attributes for deletion")
class SubjectDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

@strawberry.type(description="Result of CUD operations")
class SubjectResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Result of subject operation""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def subject(self, info: strawberry.types.Info) -> Union[AcSubjectGQLModel, None]:
        return await AcSubjectGQLModel.resolve_reference(info, self.id)
        

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_subject_insert(self, info: strawberry.types.Info, subject: SubjectInsertGQLModel) -> Union[AcSubjectGQLModel, InsertError[AcSubjectGQLModel]]:
    return await Insert[AcSubjectGQLModel].DoItSafeWay(info=info, entity=subject)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_subject_update(self, info: strawberry.types.Info, subject: SubjectUpdateGQLModel) -> Union[AcSubjectGQLModel, UpdateError[AcSubjectGQLModel]]:
    return await Update[AcSubjectGQLModel].DoItSafeWay(info=info, entity=subject)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_subject_delete(self, info: strawberry.types.Info, subject: SubjectDeleteGQLModel) -> typing.Optional[DeleteError[AcSubjectGQLModel]]:
    return await Delete[AcSubjectGQLModel].DoItSafeWay(info=info, entity=subject)
    

# endregion

# region Semester CU
@strawberry.input(description="Model for initialization during C operation")
class SemesterInsertGQLModel:
    subject_id: IDType
    classificationtype_id: IDType
    order: Optional[int] = 0
    credits: Optional[int] = 0
    id: Optional[IDType] = None
    valid: Optional[bool] = True
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of D operation")
class SemesterUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    valid: Optional[bool] = None
    order: Optional[int] = None
    credits: Optional[int] = None
    classificationtype_id: Optional[IDType] = None
    changedby: strawberry.Private[IDType] = None   

@strawberry.input(description="Attributes for deletion")
class SemesterDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

@strawberry.type(description="Result of CUD operations")
class SemesterResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Result of semester operation""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def semester(self, info: strawberry.types.Info) -> Union[AcSemesterGQLModel, None]:
        return await AcSemesterGQLModel.resolve_reference(info, self.id)
        
    
@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_semester_insert(self, info: strawberry.types.Info, semester: SemesterInsertGQLModel) -> Union[AcSemesterGQLModel, InsertError[AcSemesterGQLModel]]:
    return await Insert[AcSemesterGQLModel].DoItSafeWay(info=info, entity=semester)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_semester_update(self, info: strawberry.types.Info, semester: SemesterUpdateGQLModel) -> Union[AcSemesterGQLModel, UpdateError[AcSemesterGQLModel]]:
    return await Update[AcSemesterGQLModel].DoItSafeWay(info=info, entity=semester)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_semester_delete(self, info: strawberry.types.Info, semester: SemesterDeleteGQLModel) -> typing.Optional[DeleteError[AcSemesterGQLModel]]:
    return await Delete[AcSemesterGQLModel].DoItSafeWay(info=info, entity=semester)
    
# endregion

# region LessonType CU
@strawberry.input(description="Model for initialization during C operation")
class LessonTypeInsertGQLModel:
    name: str
    id: Optional[IDType] = None
    name_en: Optional[str] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of U operation")
class LessonTypeUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None   
    
@strawberry.input(description="Attributes for deletion")
class LessonTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

@strawberry.type(description="Result of CUD operations")
class LessonTypeResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Result of lessontype operation""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def lesson_type(self, info: strawberry.types.Info) -> Optional[AcLessonTypeGQLModel]:
        return await AcLessonTypeGQLModel.resolve_reference(info, self.id)
        

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_lesson_type_insert(self, info: strawberry.types.Info, lesson_type: LessonTypeInsertGQLModel) -> Union[AcLessonTypeGQLModel, InsertError[AcLessonTypeGQLModel]]:
    return await Insert[AcLessonTypeGQLModel].DoItSafeWay(info=info, entity=lesson_type)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_lesson_type_update(self, info: strawberry.types.Info, lesson_type: LessonTypeUpdateGQLModel) -> Union[AcLessonTypeGQLModel, UpdateError[AcLessonTypeGQLModel]]:
    return await Update[AcLessonTypeGQLModel].DoItSafeWay(info=info, entity=lesson_type)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_lesson_type_delete(self, info: strawberry.types.Info, lesson_type: LessonTypeDeleteGQLModel) -> typing.Optional[DeleteError[AcLessonTypeGQLModel]]:
    return await Delete[AcLessonTypeGQLModel].DoItSafeWay(info=info, entity=lesson_type)
    

# endregion

# region ClassificationType CU
@strawberry.input(description="Model for initialization during C operation")
class ClassificationTypeInsertGQLModel:
    name: str
    id: Optional[IDType] = None
    name_en: Optional[str] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of U operation")
class ClassificationTypeUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None   
    
@strawberry.input(description="Attributes for deletion")
class ClassificationTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

@strawberry.type(description="Result of CUD operations")
class ClassificationTypeResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Result of classificationtype operation""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def classification_type(self, info: strawberry.types.Info) -> Union[AcClassificationTypeGQLModel, None]:
        return await AcClassificationTypeGQLModel.resolve_reference(info, self.id)
        

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_classification_type_insert(self, info: strawberry.types.Info, classification_type: ClassificationTypeInsertGQLModel) -> Union[AcClassificationTypeGQLModel, InsertError[AcClassificationTypeGQLModel]]:
    return await Insert[AcClassificationTypeGQLModel].DoItSafeWay(info=info, entity=classification_type)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_classification_type_update(self, info: strawberry.types.Info, classification_type: ClassificationTypeUpdateGQLModel) -> Union[AcClassificationTypeGQLModel, UpdateError[AcClassificationTypeGQLModel]]:
    return await Update[AcClassificationTypeGQLModel].DoItSafeWay(info=info, entity=classification_type)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_classification_type_delete(self, info: strawberry.types.Info, classification_type: ClassificationTypeDeleteGQLModel) -> typing.Optional[DeleteError[AcClassificationTypeGQLModel]]:
    return await Delete[AcClassificationTypeGQLModel].DoItSafeWay(info=info, entity=classification_type)
    
# endregion

# region Classification CU
@strawberry.input(description="Model for initialization during C operation")
class ClassificationInsertGQLModel:
    semester_id: IDType
    student_id: IDType
    classificationlevel_id: IDType
    date: datetime.datetime
    order: int
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of D operation")
class ClassificationUpdateGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime
    classificationlevel_id: Optional[IDType] = None
    date: Optional[datetime.datetime] = None
    order: Optional[int] = None
    changedby: strawberry.Private[IDType] = None   
    
@strawberry.input(description="Attributes for deletion")
class ClassificationDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

@strawberry.type(description="Result of CUD operations")
class ClassificationResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Result of classification operation""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def classification(self, info: strawberry.types.Info) -> Union[AcClassificationGQLModel, None]:
        return await AcClassificationGQLModel.resolve_reference(info, self.id)
        
    
@strawberry.mutation(
        description="""Insert the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_classification_insert(self, info: strawberry.types.Info, classification: ClassificationInsertGQLModel) -> Union[AcClassificationGQLModel, InsertError[AcClassificationGQLModel]]:
    return await Insert[AcClassificationGQLModel].DoItSafeWay(info=info, entity=classification)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_classification_update(self, info: strawberry.types.Info, classification: ClassificationUpdateGQLModel) -> Union[AcClassificationGQLModel, UpdateError[AcClassificationGQLModel]]:
    return await Update[AcClassificationGQLModel].DoItSafeWay(info=info, entity=classification)
    

@strawberry.mutation(
        description="""Delete the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_classification_delete(self, info: strawberry.types.Info, classification: ClassificationDeleteGQLModel) -> typing.Optional[DeleteError[AcClassificationGQLModel]]:
    return await Delete[AcClassificationGQLModel].DoItSafeWay(info=info, entity=classification)
    

# endregion

# region ClassificationLevel

@strawberry.input(description="Model for initialization during C operation")
class ClassificationLevelInsertGQLModel:
    name: str
    name_en: Optional[str] = ""
    id: typing.Optional[uuid.UUID] = strawberry.field(description="Primary key", default=None)
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of D operation")
class ClassificationLevelUpdateGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None

@strawberry.input(description="set of updateable attributes")
class ClassificationLevelDeleteGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="timestamp")
    id: IDType = strawberry.field(description="Primary key")
    
@strawberry.type(description="Result of CUD operations")
class ClassificationLevelResultGQLModel:
    id: IDType = None
    msg: str = None

@strawberry.mutation(
    description="""Insert a new classification level""",
    permission_classes=[OnlyForAuthentized(isList=False)]
)
async def program_classification_level_insert(self, info: strawberry.types.Info, classification_level: ClassificationLevelInsertGQLModel) -> Union[AcClassificationLevelGQLModel, InsertError[AcClassificationLevelGQLModel]]:
    return await Insert[AcClassificationLevelGQLModel].DoItSafeWay(info=info, entity=classification_level)
    

@strawberry.mutation(
    description="""Update an existing classification level""",
    permission_classes=[OnlyForAuthentized(isList=False)]
)
async def program_classification_level_update(self, info: strawberry.types.Info, classification_level: ClassificationLevelUpdateGQLModel) -> Union[AcClassificationLevelGQLModel, UpdateError[AcClassificationLevelGQLModel]]:
    return await Update[AcClassificationLevelGQLModel].DoItSafeWay(info=info, entity=classification_level)
    

@strawberry.mutation(
    description="""Delete an existing classification level""",
    permission_classes=[OnlyForAuthentized(isList=False)]
)
async def program_classification_level_delete(self, info: strawberry.types.Info, classification_level: ClassificationLevelDeleteGQLModel) -> typing.Optional[DeleteError[AcClassificationLevelGQLModel]]:
    return await Delete[AcClassificationLevelGQLModel].DoItSafeWay(info=info, entity=classification_level)
    

# endregion

# region Topic CU
@strawberry.input(description="Model for initialization during C operation")
class TopicInsertGQLModel:
    semester_id: IDType
    order: Optional[int] = 0
    name: Optional[str] = "Nové téma"
    name_en: Optional[str] = "New Topic"
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of U operation")
class TopicUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    order: Optional[int] = None
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None   
    
@strawberry.input(description="Attributes for deletion")
class TopicDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

@strawberry.type(description="Result of CUD operations")
class TopicResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Result of topic operation""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def topic(self, info: strawberry.types.Info) -> Union[AcTopicGQLModel, None]:
        return await AcTopicGQLModel.resolve_reference(info, self.id)
        

@strawberry.mutation(
        description="""Insert the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_topic_insert(self, info: strawberry.types.Info, topic: TopicInsertGQLModel) -> Union[AcTopicGQLModel, InsertError[AcTopicGQLModel]]:
    return await Insert[AcTopicGQLModel].DoItSafeWay(info=info, entity=topic)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_topic_update(self, info: strawberry.types.Info, topic: TopicUpdateGQLModel) -> Union[AcTopicGQLModel, UpdateError[AcTopicGQLModel]]:
    return await Update[AcTopicGQLModel].DoItSafeWay(info=info, entity=topic)
    

@strawberry.mutation(
        description="""Delete the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_topic_delete(self, info: strawberry.types.Info, topic: TopicDeleteGQLModel) -> typing.Optional[DeleteError[AcTopicGQLModel]]:
    return await Delete[AcTopicGQLModel].DoItSafeWay(info=info, entity=topic)
    

# endregion

# region Lesson CU
@strawberry.input(description="Model for initialization during C operation")
class LessonInsertGQLModel:
    topic_id: IDType
    type_id: IDType = strawberry.field(description="type of the lesson")
    count: Optional[int] = strawberry.field(description="count of the lessons", default=2)
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of U operation")
class LessonUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")
    type_id: Optional[IDType] = None
    count: Optional[int] = None
    changedby: strawberry.Private[IDType] = None   
    
@strawberry.input(description="Attributes for deletion")
class LessonDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

@strawberry.type(description="Result of CUD operations")
class LessonResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(
            description="""Result of lesson operation""",
            permission_classes=[OnlyForAuthentized(isList=False)]
    )
    async def lesson(self, info: strawberry.types.Info) -> Union[AcLessonGQLModel, None]:
        return await AcLessonGQLModel.resolve_reference(info, self.id)
        

@strawberry.mutation(
        description="""Insert the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_lesson_insert(self, info: strawberry.types.Info, lesson: LessonInsertGQLModel) -> Union[AcLessonGQLModel, InsertError[AcLessonGQLModel]]:
    return await Insert[AcLessonGQLModel].DoItSafeWay(info=info, entity=lesson)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_lesson_update(self, info: strawberry.types.Info, lesson: LessonUpdateGQLModel) -> Union[AcLessonGQLModel, UpdateError[AcLessonGQLModel]]:
    return await Update[AcLessonGQLModel].DoItSafeWay(info=info, entity=lesson)
    

@strawberry.mutation(
        description="""Delete the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_lesson_delete(self, info: strawberry.types.Info, lesson: LessonDeleteGQLModel) -> typing.Optional[DeleteError[AcLessonGQLModel]]:
    return await Delete[AcLessonGQLModel].DoItSafeWay(info=info, entity=lesson)
    

# endregion

# region StudentState CU
@strawberry.input(description="Model for initialization during C operation")
class StudentStateInsertGQLModel:
    name: str
    name_en: Optional[str] = ""
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Model for definition of D operation")
class StudentStateUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str]
    name_en: Optional[str] = ""
    changedby: strawberry.Private[IDType] = None   
    
@strawberry.input(description="Attributes for deletion")
class StudentStateDeleteGQLModel:
    id: IDType = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

@strawberry.type(description="Result of CUD operations")
class StudentStateResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of studentstate operation""")
    async def student_state(self, info: strawberry.types.Info) -> Optional[AcProgramStudentStateGQLModel]:
        return await AcProgramStudentStateGQLModel.resolve_reference(info, self.id)
        

@strawberry.mutation(
        description="""Insert the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_student_state_insert(self, info: strawberry.types.Info, student_state: StudentStateInsertGQLModel) -> Union[AcProgramStudentStateGQLModel, InsertError[AcProgramStudentStateGQLModel]]:
    return await Insert[AcProgramStudentStateGQLModel].DoItSafeWay(info=info, entity=student_state)
    

@strawberry.mutation(
        description="""Update the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_student_state_update(self, info: strawberry.types.Info, student_state: StudentStateUpdateGQLModel) -> Union[AcProgramStudentStateGQLModel, UpdateError[AcProgramStudentStateGQLModel]]:
    return await Update[AcProgramStudentStateGQLModel].DoItSafeWay(info=info, entity=student_state)
    

@strawberry.mutation(
        description="""Delete the type of study program""",
        permission_classes=[OnlyForAuthentized(isList=False)]
    )
async def program_student_state_delete(self, info: strawberry.types.Info, student_state: StudentStateDeleteGQLModel) -> typing.Optional[DeleteError[AcProgramStudentStateGQLModel]]:
    return await Delete[AcProgramStudentStateGQLModel].DoItSafeWay(info=info, entity=student_state)
    

# endregion


###########################################################################################################################
#
#
# Mutations - Object
#
#
###########################################################################################################################

# region Mutation Class
@strawberry.federation.type(extend=True)
class Mutation:

    program_insert = program_insert
    program_update = program_update
    program_delete = program_delete

    program_type_insert = program_type_insert
    program_type_update = program_type_update
    program_type_delete = program_type_delete

    program_language_type_insert = program_language_type_insert
    program_language_type_update = program_language_type_update
    program_language_type_delete = program_language_type_delete

    program_form_type_insert = program_form_type_insert
    program_form_type_update = program_form_type_update
    program_form_type_delete = program_form_type_delete

    program_title_type_insert = program_title_type_insert
    program_title_type_update = program_title_type_update
    program_title_type_delete = program_title_type_delete

    program_level_type_insert = program_level_type_insert
    program_level_type_update = program_level_type_update
    program_level_type_delete = program_level_type_delete

    program_student_insert = program_student_insert
    program_student_update = program_student_update
    program_student_delete = program_student_delete

    program_message_insert = program_message_insert
    program_message_update = program_message_update
    program_message_delete = program_message_delete

    program_student_state_insert = program_student_state_insert
    program_student_state_update = program_student_state_update
    program_student_state_delete = program_student_state_delete

    program_classification_insert = program_classification_insert
    program_classification_update = program_classification_update
    program_classification_delete = program_classification_delete
    
    program_classification_type_insert = program_classification_type_insert
    program_classification_type_update = program_classification_type_update
    program_classification_type_delete = program_classification_type_delete
    
    program_classification_level_insert = program_classification_level_insert
    program_classification_level_update = program_classification_level_update
    program_classification_level_delete = program_classification_level_delete

    program_lesson_type_insert = program_lesson_type_insert
    program_lesson_type_update = program_lesson_type_update
    program_lesson_type_delete = program_lesson_type_delete

    program_lesson_insert = program_lesson_insert
    program_lesson_update = program_lesson_update
    program_lesson_delete = program_lesson_delete

    program_topic_insert = program_topic_insert
    program_topic_update = program_topic_update
    program_topic_delete = program_topic_delete

    program_subject_insert = program_subject_insert
    program_subject_update = program_subject_update
    program_subject_delete = program_subject_delete
    
    program_semester_insert = program_semester_insert
    program_semester_update = program_semester_update
    program_semester_delete = program_semester_delete
# endregion

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

from .GraphTypeDefinitionsExt import GroupGQLModel as _GroupGQLModel, UserGQLModel as _UserGQLModel
schema = strawberry.federation.Schema(query=Query, mutation=Mutation, extensions=[],
    types=(
    _GroupGQLModel, 
    _UserGQLModel,
    AcClassificationLevelGQLModel, 
    AcClassificationGQLModel, 
    AcProgramTypeGQLModel, 
    AcClassificationTypeGQLModel, 
    AcProgramTitleTypeGQLModel,
    AcProgramLevelTypeGQLModel,
    AcProgramLanguageTypeGQLModel,
    AcProgramGQLModel,
    AcProgramFormTypeGQLModel))

from uoishelpers.schema import WhoAmIExtension
schema.extensions.append(WhoAmIExtension)

