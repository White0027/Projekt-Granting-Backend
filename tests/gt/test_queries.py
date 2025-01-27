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
#     data= response["data"]
#     assert data is not None, f"Expected 'data' in response, got: {response}"
#     assert response["data"].get("me", None) is not None, f"Expected 'me' field in response data {response}"
#     logging.info(f"User data: {response}")
    
######################################################################### ClassificationLevel CRUD Tests

# Read ClassificationLevel by ID
test_classification_level_by_id = createByIdTest2(
    tableName="classification_levels"
)

######################################################################### Classification CRUD Tests

# Read Classification by ID
test_classification_by_id = createByIdTest2(
    tableName="classifications"
)

######################################################################### ClassificationType CRUD Tests

# Read ClassificationType by ID
test_classification_type_by_id = createByIdTest2(
    tableName="classification_types"
)

######################################################################### Lesson CRUD Tests

# Read Lesson by ID
test_lesson_by_id = createByIdTest2(
    tableName="lessons"
)

######################################################################### LessonType CRUD Tests

# Read LessonType by ID
test_lesson_type_by_id = createByIdTest2(
    tableName="lesson_types"
)

######################################################################### Program CRUD Tests

# Read Program by ID
test_program_by_id = createByIdTest2(
    tableName="programs"
)

######################################################################### ProgramFormType CRUD Tests

# Read ProgramFormType by ID
test_program_form_type_by_id = createByIdTest2(
    tableName="program_form_types"
)

######################################################################### ProgramLanguageType CRUD Tests

# Read ProgramLanguageType by ID
test_program_language_type_by_id = createByIdTest2(
    tableName="program_language_types"
)

######################################################################### ProgramLevelType CRUD Tests

# Read ProgramLevelType by ID
test_program_level_type_by_id = createByIdTest2(
    tableName="program_level_types"
)

######################################################################### ProgramMessage CRUD Tests

# Read ProgramMessage by ID
test_program_message_by_id = createByIdTest2(
    tableName="program_messages"
)

######################################################################### ProgramStudent CRUD Tests

# Read ProgramStudent by ID
test_program_student_by_id = createByIdTest2(
    tableName="program_students"
)

######################################################################### ProgramTitleType CRUD Tests

# Read ProgramTitleType by ID
test_program_title_type_by_id = createByIdTest2(
    tableName="program_title_types"
)

######################################################################### ProgramType CRUD Tests

# Read ProgramType by ID
test_program_type_by_id = createByIdTest2(
    tableName="program_types"
)

######################################################################### Semester CRUD Tests

# Read Semester by ID
test_semester_by_id = createByIdTest2(
    tableName="semesters"
)

######################################################################### StudentState CRUD Tests

# Read StudentState by ID
test_student_state_by_id = createByIdTest2(
    tableName="student_states"
)

######################################################################### Subject CRUD Tests

# Read Subject by ID
test_subject_by_id = createByIdTest2(
    tableName="subjects"
)

######################################################################### Topic CRUD Tests

# Read Topic by ID
test_topic_by_id = createByIdTest2(
    tableName="topics"
)