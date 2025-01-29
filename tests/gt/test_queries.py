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

######################################################################### ClassificationType CRUD Tests

# Read ClassificationType by ID
test_classification_type_by_id = createByIdTest2(
    tableName="acclassificationtypes"
)

######################################################################### Lesson CRUD Tests

# Read Lesson by ID
test_lesson_by_id = createByIdTest2(
    tableName="aclessons"
)

######################################################################### LessonType CRUD Tests

# Read LessonType by ID
test_lesson_type_by_id = createByIdTest2(
    tableName="aclessontypes"
)

######################################################################### Program CRUD Tests

# Read Program by ID
test_program_by_id = createByIdTest2(
    tableName="acprograms"
)

######################################################################### ProgramFormType CRUD Tests

# Read ProgramForm by ID
test_program_form_type_by_id = createByIdTest2(
    tableName="acprogramforms"
)

######################################################################### ProgramLanguageType CRUD Tests

# Read ProgramLanguageType by ID
test_program_language_type_by_id = createByIdTest2(
    tableName="acprogramlanguages"
)

######################################################################### ProgramLevelType CRUD Tests

# Read ProgramLevelType by ID
test_program_level_type_by_id = createByIdTest2(
    tableName="acprogramlevels"
)

######################################################################### ProgramStudentMessage CRUD Tests

# Read ProgramStudentMessage by ID
test_program_message_by_id = createByIdTest2(
    tableName="acprograms_studentmessages"
)

######################################################################### ProgramStudent CRUD Tests

# Read ProgramStudent by ID
test_program_student_by_id = createByIdTest2(
    tableName="acprograms_students"
)

######################################################################### ProgramTitleType CRUD Tests

# Read ProgramTitleType by ID
test_program_title_type_by_id = createByIdTest2(
    tableName="acprogramtitles"
)

######################################################################### ProgramType CRUD Tests

# Read ProgramType by ID
test_program_type_by_id = createByIdTest2(
    tableName="acprogramtypes"
)

######################################################################### Semester CRUD Tests

# Read Semester by ID
test_semester_by_id = createByIdTest2(
    tableName="acsemesters"
)

######################################################################### StudentState CRUD Tests

# Read StudentState by ID
test_student_state_by_id = createByIdTest2(
    tableName="acprograms_studentstates"
)

######################################################################### Subject CRUD Tests

# Read Subject by ID
test_subject_by_id = createByIdTest2(
    tableName="acsubjects"
)

######################################################################### Topic CRUD Tests

# Read Topic by ID
test_topic_by_id = createByIdTest2(
    tableName="actopics"
)