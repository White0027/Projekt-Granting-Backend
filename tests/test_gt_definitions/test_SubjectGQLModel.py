import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

tableName='acsubjects'
gqltype = 'AcSubjectGQLModel'
endpointPrefix = "acSubject"
attributeNames=["id", "name"]
test_reference_subject = createResolveReferenceTest(
    tableName=tableName, gqltype=gqltype, attributeNames=attributeNames)
test_page_subject = createPageTest(queryEndpoint=endpointPrefix + "Page", 
    tableName=tableName, attributeNames=attributeNames)
test_by_id_subject = createByIdTest(queryEndpoint=endpointPrefix + "ById", 
    tableName=tableName, attributeNames=attributeNames)


test_insert_program_subject = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!, $name_en: String, 
            $program_id: UUID!, $group_id: UUID!
        ) {
        result: programSubjectInsert(subject: {
            id: $id, name: $name, nameEn: $name_en
            programId: $program_id, groupId: $group_id
        }) {
            id
            msg
            result: subject {
                id
                lastchange
                name
                nameEn
                program { id }
                semesters { id }
                grants { id }
            }
        }
    }""",
    variables={
        "id": "b8f58e3e-3e05-4dbc-b84e-86a3ea08f949", 
        "program_id": "2766fc9a-b095-11ed-9bd8-0242ac110002",
        "name": "new name",
        "group_id": "9baf3b54-ae0f-11ed-9bd8-0242ac110002"
    }
)

test_update_program_subject = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String, $name_en: String, $lastchange: DateTime!) {
        result: programSubjectUpdate(subject: {id: $id, name: $name, nameEn: $name_en, lastchange: $lastchange}) {
            id
            msg
            result: subject {
                id
                name
            }
        }
    }""",
    variables={"id": "ce250a68-b095-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName=tableName
)