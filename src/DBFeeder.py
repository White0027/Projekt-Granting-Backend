import os
from uoishelpers.feeders import ImportModels
from uoishelpers.dataloaders import readJsonFile
import datetime
import json
import uuid

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

def get_demodata(filename="./systemdata.json"):
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["date", "startdate", "enddate", "lastchange", "created"]:
                if value is None:
                    dateValueWOtzinfo = None
                else:
                    try:
                        dateValue = datetime.datetime.fromisoformat(value)
                        dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                    except Exception:
                        print("jsonconvert Error", key, value, flush=True)
                        dateValueWOtzinfo = None
                        
                json_dict[key] = dateValueWOtzinfo
                
            if (key in ["id", "changedby", "createdby", "rbacobject"]) or ("_id" in key):

                if key == "outer_id":
                    json_dict[key] = value
                elif value not in ["", None]:
                    json_dict[key] = uuid.UUID(value)
                else:
                    print(key, value)

        return json_dict

    with open(filename, "r", encoding="utf-8") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData

async def initDB(asyncSessionMaker, filename="./systemdata.json"):
    dbModels = [
        ProgramFormTypeModel, ProgramLanguageTypeModel, ProgramLevelTypeModel, ProgramTitleTypeModel, ProgramTypeModel,
        LessonTypeModel, ClassificationLevelModel, ClassificationTypeModel, ProgramModel, SubjectModel, SemesterModel,
        TopicModel, LessonModel, ClassificationModel, ProgramStudentStateModel, ProgramStudentModel, ProgramStudentMessageModel
    ]

    DEMODATA = os.environ.get("DEMODATA", None) in ["True", "true"]    
    if DEMODATA:
        dbModels.extend([
        ProgramFormTypeModel, ProgramLanguageTypeModel, ProgramLevelTypeModel, ProgramTitleTypeModel, ProgramTypeModel,
        LessonTypeModel, ClassificationLevelModel, ClassificationTypeModel, ProgramModel, SubjectModel, SemesterModel,
        TopicModel, LessonModel, ClassificationModel, ProgramStudentStateModel, ProgramStudentModel, ProgramStudentMessageModel
        ])
        
    jsonData = get_demodata(filename=filename)
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass