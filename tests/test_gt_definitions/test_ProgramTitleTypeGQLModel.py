import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

tableName='acprogramtitles'
gqltype = 'AcProgramTitleTypeGQLModel'
endpointPrefix = "acProgramTitleType"
attributeNames=["id", "name"]
test_reference_program_type = createResolveReferenceTest(
    tableName=tableName, gqltype=gqltype, attributeNames=attributeNames)
test_page_program_type = createPageTest(queryEndpoint=endpointPrefix + "Page", 
    tableName=tableName, attributeNames=attributeNames)
test_by_id_program_type = createByIdTest(queryEndpoint=endpointPrefix + "ById", 
    tableName=tableName, attributeNames=attributeNames)


test_insert_program_title = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!, $name_en: String) {
        result: programTitleTypeInsert(titleType: {id: $id, name: $name, nameEn: $name_en}) {
            id
            msg
            result: programTitleType {
                id
                lastchange
                name
                nameEn
            }
        }
    }""",
    variables={
        "id": "b8f58e3e-3e05-4dbc-b84e-86a3ea08f949", 
        "name": "new name",
    }
)

test_update_program_title = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String, $name_en: String, $lastchange: DateTime!) {
        result: programTitleTypeUpdate(titleType: {id: $id, name: $name, nameEn: $name_en, lastchange: $lastchange}) {
            id
            msg
            result: programTitleType {
                id
                name
            }
        }
    }""",
    variables={"id": "d1431d9c-930e-11ed-9b95-0242ac110002", "name": "new name"},
    tableName=tableName
)