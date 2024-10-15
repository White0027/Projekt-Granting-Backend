import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

tableName='acprograms_studentstates'
gqltype = 'AcProgramStudentStateGQLModel'
endpointPrefix = "acProgramStudentState"
attributeNames=["id"]
test_reference_student_state = createResolveReferenceTest(
    tableName=tableName, gqltype=gqltype, attributeNames=attributeNames)
test_page_student_state = createPageTest(queryEndpoint=endpointPrefix + "Page", 
    tableName=tableName, attributeNames=attributeNames)
test_by_id_student_state = createByIdTest(queryEndpoint=endpointPrefix + "ById", 
    tableName=tableName, attributeNames=attributeNames)


test_insert_student_state = createFrontendQuery(
    query="""mutation (
            $id: UUID!, $name: String!, $name_en: String
            ) {
        result: programStudentStateInsert(studentState: 
            {
                id: $id, name: $name, nameEn: $name_en
            }) {
            id
            msg
            result: studentState {
                id
                name
                nameEn
            }
        }
    }""",
    variables={
        "id": "b8f58e3e-3e05-4dbc-b84e-86a3ea08f949", 
        "name": "new name"
    }
)

test_classification_update = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String, $name_en: String, $lastchange: DateTime!) {
        result: programStudentStateUpdate(
            studentState: {id: $id, name: $name, nameEn: $name_en, lastchange: $lastchange}) {
            id
            msg
            result: studentState {
                id
                name
            }
        }
    }""",
    variables={"id": "6c96b893-ca09-4b6f-9fbb-5359c589927b", "name": "new name"},
    tableName=tableName
)