import pytest
import logging
from .gt_utils import (
    createByIdTest2,
    createUpdateTest2,
    createTest2,
    createDeleteTest2,
    getQuery
)

# Initial Environment Validation
myquery = """
{
  me {
    id
    fullname
    email
    roles {
      valid
      group { id name }
      roletype { id name }
    }
  }
}"""

# @pytest.mark.asyncio
# async def test_result_test(NoRole_UG_Server):
#     response = await NoRole_UG_Server(query=myquery, variables={})
#     assert "data" in response, f"Expected 'data' in response, got: {response}"
#     data = response["data"]
#     assert data is not None, f"Expected 'data' in response, got: {response}"
#     assert response["data"].get("me", None) is not None, f"Expected 'me' field in response data {response}"
#     logging.info(f"User data: {response}")

######################################################################### ClassificationLevel CRUD Tests

# Create ClassificationLevel
test_classification_level_create = createTest2(
    tableName="acclassificationlevels",
    queryName="create",
    variables={
        "name": "Test Classification Level",
        "nameEn": "Test Classification Level EN"
    }
)

# Read ClassificationLevel by ID
test_classification_level_by_id = createByIdTest2(
    tableName="acclassificationlevels"
)

# Update ClassificationLevel
test_classification_level_update = createUpdateTest2(
    tableName="acclassificationlevels",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "name": "Updated Classification Level",
        "nameEn": "Updated Classification Level EN"
    }
)

# Delete ClassificationLevel
test_classification_level_delete = createDeleteTest2(
    tableName="acclassificationlevels",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "name": "Delete Classification Level",
        "nameEn": "Delete Classification Level EN"
    }
)

######################################################################### Classification CRUD Tests

# Read Classification by ID
test_classification_by_id = createByIdTest2(
    tableName="acclassifications"
)

# Create Classification
test_classification_create = createTest2(
    tableName="acclassifications",
    queryName="create",
    variables={
        "name": "Test Classification",
        "nameEn": "Test Classification EN",
        "classificationlevel_id": "5faea332-b095-11ed-9bd8-0242ac110002",
        "student_id": "6eea946f-7695-4580-90df-7b32e224fc3d",
        "order": 1,
        "date": "2024-07-10T00:00:00",
        "semester_id": "5486f84e-2d3a-47c1-87ab-1a54590950db"
    }
)

# Update Classification
test_classification_update = createUpdateTest2(
    tableName="acclassifications",
    variables={
        "name": "Updated Classification",
        "nameEn": "Updated Classification EN",
        "lastchange": "2024-09-08T15:27:11.855854",
        "classificationlevel_id": "5faea332-b095-11ed-9bd8-0242ac110002",
        "student_id": "6eea946f-7695-4580-90df-7b32e224fc3d",
        "order": 2,
        "date": "2024-07-11T00:00:00",
        "semester_id": "5486f84e-2d3a-47c1-87ab-1a54590950db"
    }
)

# Delete Classification
test_classification_delete = createDeleteTest2(
    tableName="acclassifications",
    variables={
        "name": "Delete Classification",
        "order": 0,
        "date": "2024-07-10T00:00:00",
        "semester_id": "5486f84e-2d3a-47c1-87ab-1a54590950db",
        "classificationlevel_id": "5faea332-b095-11ed-9bd8-0242ac110002",
        "student_id": "6eea946f-7695-4580-90df-7b32e224fc3d",
        "lastchange": "2024-09-08T15:27:11.855854",
    }
)

######################################################################### ClassificationType CRUD Tests

# Read ClassificationType by ID
test_classification_type_by_id = createByIdTest2(
    tableName="acclassificationtypes"
)

# Create ClassificationType
test_classification_type_create = createTest2(
    tableName="acclassificationtypes",
    queryName="create",
    variables={
        "name": "Test Classification Type",
        "nameEn": "Test Classification Type EN"
    }
)

# Update ClassificationType
test_classification_type_update = createUpdateTest2(
    tableName="acclassificationtypes",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "name": "Updated Classification Type",
        "nameEn": "Updated Classification Type EN"
    }
)

# Delete ClassificationType
test_classification_type_delete = createDeleteTest2(
    tableName="acclassificationtypes",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "name": "Delete Classification Type"
    }
)

######################################################################### Lesson CRUD Tests

# Read Lesson by ID
test_lesson_by_id = createByIdTest2(
    tableName="aclessons"
)

# Create Lesson
test_lesson_create = createTest2(
    tableName="aclessons",
    queryName="create",
    variables={
        "count": 2,
        "topic_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "type_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e"
    }
)

# Update Lesson
test_lesson_update = createUpdateTest2(
    tableName="aclessons",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "count": 3,
        "type_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e"
        
    }
)

# Delete Lesson
test_lesson_delete = createDeleteTest2(
    tableName="aclessons",
    variables={
        "count": 0,
        "type_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "topic_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "lastchange": "2023-01-01T00:00:00"
    }
)

######################################################################### LessonType CRUD Tests

# Read LessonType by ID
test_lesson_type_by_id = createByIdTest2(
    tableName="aclessontypes"
)

# Create LessonType
test_lesson_type_create = createTest2(
    tableName="aclessontypes",
    queryName="create",
    variables={
        "name": "Test Lesson Type",
        "nameEn": "Test Lesson Type EN"
    }
)

# Update LessonType
test_lesson_type_update = createUpdateTest2(
    tableName="aclessontypes",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "name": "Updated Lesson Type",
        "nameEn": "Updated Lesson Type EN"
    }
)

# Delete LessonType
test_lesson_type_delete = createDeleteTest2(
    tableName="aclessontypes",
    variables={
        "name": "Delete Lesson Type",
        "lastchange": "2023-01-01T00:00:00"
    }
)

######################################################################### Program CRUD Tests

# Read Program by ID
test_program_by_id = createByIdTest2(
    tableName="acprograms"
)

# Create Program
test_program_create = createTest2(
    tableName="acprograms",
    queryName="create",
    variables={
        "name": "Test Program",
        "type_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "group_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "licenced_group_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e"
    }
)

# Update Program
test_program_update = createUpdateTest2(
    tableName="acprograms",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "name": "Updated Program",
        "type_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "group_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "licenced_group_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e"
    }
)

# Delete Program
test_program_delete = createDeleteTest2(
    tableName="acprograms",
    variables={
        "name": "Delete Program",
        "type_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "group_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "licenced_group_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",        
        "lastchange": "2023-01-01T00:00:00"
    }
)

######################################################################### ProgramFormType CRUD Tests

# Read ProgramForm by ID
test_program_form_type_by_id = createByIdTest2(
    tableName="acprogramforms"
)

# Create ProgramForm
test_program_form_create = createTest2(
    tableName="acprogramforms",
    queryName="create",
    variables={
        "name": "Test Program Form",
        "description": "Test Program Form Description"
    }
)

# Update ProgramForm
test_program_form_update = createUpdateTest2(
    tableName="acprogramforms",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "name": "Updated Program Form",
        "description": "Updated Program Form Description"
    }
)

# Delete ProgramForm
test_program_form_delete = createDeleteTest2(
    tableName="acprogramforms",
    variables={
        "name": "Delete Program Form",
        "lastchange": "2023-01-01T00:00:00"
    }
)

######################################################################### ProgramLanguageType CRUD Tests

# Read ProgramLanguageType by ID
test_program_language_type_by_id = createByIdTest2(
    tableName="acprogramlanguages"
)

# Create ProgramLanguageType
test_program_language_type_create = createTest2(
    tableName="acprogramlanguages",
    queryName="create",
    variables={
        "name": "Test Program Language",
        "description": "Test Program Language Description"
    }
)

# Update ProgramLanguageType
test_program_language_type_update = createUpdateTest2(
    tableName="acprogramlanguages",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "name": "Updated Program Language",
        "description": "Updated Program Language Description"
    }
)

# Delete ProgramLanguageType
test_program_language_type_delete = createDeleteTest2(
    tableName="acprogramlanguages",
    variables={
        "name": "Delete Program Language",
        "lastchange": "2023-01-01T00:00:00"
    }
)

######################################################################### ProgramLevelType CRUD Tests

# Read ProgramLevelType by ID
test_program_level_type_by_id = createByIdTest2(
    tableName="acprogramlevels"
)

# Create ProgramLevelType
test_program_level_type_create = createTest2(
    tableName="acprogramlevels",
    queryName="create",
    variables={
        "name": "Test Program Level Type",
        "nameEn": "Test Program Level Type EN"
    }
)

# Update ProgramLevelType
test_program_level_type_update = createUpdateTest2(
    tableName="acprogramlevels",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "name": "Updated Program Level Type",
        "nameEn": "Updated Program Level Type EN"
    }
)

# Delete ProgramLevelType
test_program_level_type_delete = createDeleteTest2(
    tableName="acprogramlevels",
    variables={
        "name": "Delete Program Level Type",
        "lastchange": "2023-01-01T00:00:00"
    }
)

######################################################################### ProgramStudentMessage CRUD Tests

# Read ProgramStudentMessage by ID
test_program_message_by_id = createByIdTest2(
    tableName="acprograms_studentmessages"
)

# Create ProgramStudentMessage
test_program_student_message_create = createTest2(
    tableName="acprograms_studentmessages",
    queryName="create",
    variables={
        "name": "Test Program Student Message",
        "description": "Test Program Student Message Description",
        "date": "2023-01-01T00:00:00",
        "student_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "program_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e"
    }
)

# Update ProgramStudentMessage
test_program_student_message_update = createUpdateTest2(
    tableName="acprograms_studentmessages",
    variables={
        "name": "Updated Program Student Message",
        "date": "2023-01-01T00:00:00",
        "lastchange": "2023-01-01T00:00:00"
    }
)

# Delete ProgramStudentMessage
test_program_student_message_delete = createDeleteTest2(
    tableName="acprograms_studentmessages",
    variables={
        "name": "Delete Program Student Message",
        "date": "2023-01-01T00:00:00",
        "student_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "program_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "lastchange": "2023-01-01T00:00:00"
    }
)

######################################################################### ProgramStudent CRUD Tests

# Read ProgramStudent by ID
test_program_student_by_id = createByIdTest2(
    tableName="acprograms_students"
)

# Create ProgramStudent
test_program_student_create = createTest2(
    tableName="acprograms_students",
    queryName="create",
    variables={
        "student_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "program_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "state_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "semester": 3,
    }
)

# Update ProgramStudent
test_program_student_update = createUpdateTest2(
    tableName="acprograms_students",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "semester": 4,
        "state_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "name": "Updated Program Student"
    }
)

# Delete ProgramStudent
test_program_student_delete = createDeleteTest2(
    tableName="acprograms_students",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "program_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "student_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "state_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e"
    }
)

######################################################################### ProgramTitleType CRUD Tests

# Read ProgramTitleType by ID
test_program_title_type_by_id = createByIdTest2(
    tableName="acprogramtitles"
)

# Create ProgramTitleType
test_program_title_type_create = createTest2(
    tableName="acprogramtitles",
    queryName="create",
    variables={
        "name": "Test Program Title Type",
        "nameEn": "Test Program Title Type EN"

    }
)

# Update ProgramTitleType
test_program_title_type_update = createUpdateTest2(
    tableName="acprogramtitles",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "name": "Updated Program Title Type",
        "nameEn": "Updated Program Title Type EN"

    }
)

# Delete ProgramTitleType
test_program_title_type_delete = createDeleteTest2(
    tableName="acprogramtitles",
    variables={
        "name": "Delete Program Title Type",
        "lastchange": "2023-01-01T00:00:00"
    }
)

######################################################################### ProgramType CRUD Tests

# Read ProgramType by ID
test_program_type_by_id = createByIdTest2(
    tableName="acprogramtypes"
)

# Create ProgramType
test_program_type_create = createTest2(
    tableName="acprogramtypes",
    queryName="create",
    variables={
        "name": "Test Program Type",
        "nameEn": "Test Program Type EN",
        "form_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "language_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "level_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "title_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e"
    }
)

# Update ProgramType
test_program_type_update = createUpdateTest2(
    tableName="acprogramtypes",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "name": "Test Program Type",
        "nameEn": "Test Program Type EN",
        "form_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "language_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "level_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "title_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e"
    }
)

# Delete ProgramType
test_program_type_delete = createDeleteTest2(
    tableName="acprogramtypes",
    variables={
        "name": "Delete Program Type",
        "form_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "language_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "level_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "title_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "lastchange": "2023-01-01T00:00:00"
    }
)

######################################################################### Semester CRUD Tests

# Read Semester by ID
test_semester_by_id = createByIdTest2(
    tableName="acsemesters"
)

# Create Semester
test_semester_create = createTest2(
    tableName="acsemesters",
    queryName="create",
    variables={
        "classificationtype_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "order": 1,
        "valid": True,
        "subject_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e"
    }
)

# Update Semester
test_semester_update = createUpdateTest2(
    tableName="acsemesters",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "classificationtype_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "order": 1,
        "subject_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e"
    }
)

# Delete Semester
test_semester_delete = createDeleteTest2(
    tableName="acsemesters",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "classificationtype_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "order": 1,
        "subject_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "valid": True
        
    }
)

######################################################################### StudentState CRUD Tests

# Read StudentState by ID
test_student_state_by_id = createByIdTest2(
    tableName="acprograms_studentstates"
)

# Create StudentState
test_student_state_create = createTest2(
    tableName="acprograms_studentstates",
    queryName="create",
    variables={
        "name": "Test Student State",
        "nameEn": "Test Student State EN",
    }
)

# Update StudentState
test_student_state_update = createUpdateTest2(
    tableName="acprograms_studentstates",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "name": "Updated Student State",
        "nameEn": "Updated Student State EN"
    }
)

# Delete StudentState
test_student_state_delete = createDeleteTest2(
    tableName="acprograms_studentstates",
    variables={
        "name": "Delete Student State",
        "lastchange": "2023-01-01T00:00:00"
    }
)

######################################################################### Subject CRUD Tests

# Read Subject by ID
test_subject_by_id = createByIdTest2(
    tableName="acsubjects"
)

# Create Subject
test_subject_create = createTest2(
    tableName="acsubjects",
    queryName="create",
    variables={
        "name": "Test Subject",
        "nameEn": "Test Subject EN",
        "program_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "group_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e"
    }
)

# Update Subject
test_subject_update = createUpdateTest2(
    tableName="acsubjects",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "name": "Updated Subject",
        "nameEn": "Updated Subject EN",
        "program_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e"
    }
)

# Delete Subject
test_subject_delete = createDeleteTest2(
    tableName="acsubjects",
    variables={
        "program_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "group_id": "f5c7e1d1-7b5e-4e9b-9c1e-6a5b8b4e2c1e",
        "name": "Delete Subject",
        "lastchange": "2023-01-01T00:00:00"
    }
)

######################################################################### Topic CRUD Tests

# Read Topic by ID
test_topic_by_id = createByIdTest2(
    tableName="actopics"
)

# Create Topic
test_topic_create = createTest2(
    tableName="actopics",
    queryName="create",
    variables={
        "name": "Test Topic",
        "nameEn": "Test Topic EN",
        "order": 1,
        "semester_id": "5486f84e-2d3a-47c1-87ab-1a54590950db"
    }
)

# Update Topic
test_topic_update = createUpdateTest2(
    tableName="actopics",
    variables={
        "lastchange": "2023-01-01T00:00:00",
        "name": "Updated Topic",
        "nameEn": "Updated Topic EN",
        "order": 2,
    }
)

# Delete Topic
test_topic_delete = createDeleteTest2(
    tableName="actopics",
    variables={
        "name": "Delete Topic",
        "semester_id": "5486f84e-2d3a-47c1-87ab-1a54590950db",
        "lastchange": "2023-01-01T00:00:00"
    }
)