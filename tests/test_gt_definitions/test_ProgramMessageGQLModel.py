import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

tableName='acprograms_studentmessages'
gqltype = 'AcProgramMessageGQLModel'
endpointPrefix = "acProgramMessage"
attributeNames=["id", "name"]
test_reference_program_message = createResolveReferenceTest(
    tableName=tableName, gqltype=gqltype, attributeNames=attributeNames)
# test_page_program_message = createPageTest(queryEndpoint=endpointPrefix + "Page", 
#     tableName=tableName, attributeNames=attributeNames)
# test_by_id_program_message = createByIdTest(queryEndpoint=endpointPrefix + "ById", 
#     tableName=tableName, attributeNames=attributeNames)


test_insert_program_message = createFrontendQuery(
    query="""mutation (
            $id: UUID!, $name: String!, $description: String
            $student_id: UUID!, $program_id: UUID!,
            $date: DateTime!
        ) {
        result: programMessageInsert(message: 
            {
                id: $id, name: $name, description: $description
                studentId: $student_id, programId: $program_id
                date: $date
            }) {
            id
            msg
            result: message {
                id
                name
                description
                date

                student { id }
                program { id }

            }
        }
    }""",
    variables={
        "id": "806ddae6-d9c2-41aa-ad74-0b7312860db1", 
        "name": "new name",
        "student_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
        "program_id": "2766fc9a-b095-11ed-9bd8-0242ac110002",
        "date": "2023-12-24T08:00:00"

    }
)

test_program_update = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String, $name_en: String, $lastchange: DateTime!) {
        result: programMessageUpdate(message: {id: $id, name: $name, nameEn: $name_en, lastchange: $lastchange}) {
            id
            msg
            result: message {
                id
                name
            }
        }
    }""",
    variables={"id": "69f0f875-e09a-4838-b5df-4845d955575d", "name": "new name"},
    tableName=tableName
)