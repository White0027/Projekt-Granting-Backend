import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

tableName='acprogramlanguages'
gqltype = 'AcProgramLanguageTypeGQLModel'
endpointPrefix = "acProgramLanguageType"
attributeNames=["id", "name"]
test_reference_program_type = createResolveReferenceTest(
    tableName=tableName, gqltype=gqltype, attributeNames=attributeNames)
test_page_program_type = createPageTest(queryEndpoint=endpointPrefix + "Page", 
    tableName=tableName, attributeNames=attributeNames)
test_by_id_program_type = createByIdTest(queryEndpoint=endpointPrefix + "ById", 
    tableName=tableName, attributeNames=attributeNames)


test_insert_program_language = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!, $name_en: String) {
        result: programLanguageTypeInsert(languageType: {id: $id, name: $name, nameEn: $name_en}) {
            id
            msg
            result: programLanguageType {
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

test_update_program_language = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String, $name_en: String, $lastchange: DateTime!) {
        result: programLanguageTypeUpdate(languageType: {id: $id, name: $name, nameEn: $name_en, lastchange: $lastchange}) {
            id
            msg
            result: programLanguageType {
                id
                name
            }
        }
    }""",
    variables={"id": "36e9a40a-930e-11ed-9b95-0242ac110002", "name": "new name"},
    tableName=tableName
)