import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

tableName='acprograms_students'
gqltype = 'AcProgramStudentGQLModel'
endpointPrefix = "acProgramStudent"
attributeNames=["id"]
test_reference_program_type = createResolveReferenceTest(
    tableName=tableName, gqltype=gqltype, attributeNames=attributeNames)
# test_page_program_type = createPageTest(queryEndpoint=endpointPrefix + "Page", 
#     tableName=tableName, attributeNames=attributeNames)
# test_by_id_program_type = createByIdTest(queryEndpoint=endpointPrefix + "ById", 
#     tableName=tableName, attributeNames=attributeNames)


test_insert_program_student = createFrontendQuery(
    query="""mutation (
            $id: UUID!, $student_id: UUID!, $program_id: UUID!,
                $state_id: UUID!, $semester: Int
        ) {
        result: programStudentInsert(student: {
                id: $id, studentId: $student_id, programId: $program_id,
                stateId: $state_id, semester: $semester
            }) {
            id
            msg
            result: student {
                id
                lastchange
                student { id }
                messages { id }
                state { id }
            }
        }
    }""",
    variables={
        "id": "b8f58e3e-3e05-4dbc-b84e-86a3ea08f949", 
        "student_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
        "program_id": "2766fc9a-b095-11ed-9bd8-0242ac110002",
        "state_id": "6c96b893-ca09-4b6f-9fbb-5359c589927b",
        "semester": 1
    }
)

test_update_program_student = createUpdateQuery(
    query="""mutation ($id: UUID!, $semester: Int, $lastchange: DateTime!) {
        result: programStudentUpdate(student: {id: $id, semester: $semester, lastchange: $lastchange}) {
            id
            msg
            result: student {
                id
                semester
            }
        }
    }""",
    variables={"id": "c58fbafe-01c9-42ba-9cce-dd489e77a670", "semester": 2},
    tableName=tableName
)