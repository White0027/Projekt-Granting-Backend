import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

tableName='acprogramtypes'
gqltype = 'AcProgramTypeGQLModel'
endpointPrefix = "acProgramType"
attributeNames=["id", "name"]
test_reference_program_type = createResolveReferenceTest(
    tableName=tableName, gqltype=gqltype, attributeNames=attributeNames)
test_page_program_type = createPageTest(queryEndpoint=endpointPrefix + "Page", 
    tableName=tableName, attributeNames=attributeNames)
test_by_id_program_type = createByIdTest(queryEndpoint=endpointPrefix + "ById", 
    tableName=tableName, attributeNames=attributeNames)


test_insert_program_type = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!, $name_en: String, 
        $title_id: UUID!, $form_id: UUID!, $language_id: UUID!, $level_id: UUID!) {
        result: programTypeInsert(programType: 
            {
                id: $id, name: $name, nameEn: $name_en
                titleId: $title_id, formId: $form_id, 
                languageId: $language_id, levelId: $level_id
            }) {
            id
            msg
            result: programType {
                id
                name
                nameEn
                level { id }
                form { id }
                language { id }
                title { id }
            }
        }
    }""",
    variables={
        "id": "b8f58e3e-3e05-4dbc-b84e-86a3ea08f949", 
        "name": "new name",
        "title_id": "d1431d9c-930e-11ed-9b95-0242ac110002",
        "form_id": "19018d2c-930e-11ed-9b95-0242ac110002",
        "language_id": "36e9a40a-930e-11ed-9b95-0242ac110002",
        "level_id": "5c549cae-930e-11ed-9b95-0242ac110002"
    }
)

test_program_update = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String, $name_en: String, $lastchange: DateTime!) {
        result: programTypeUpdate(programType: {id: $id, name: $name, nameEn: $name_en, lastchange: $lastchange}) {
            id
            msg
            result: programType {
                id
                name
            }
        }
    }""",
    variables={"id": "fd4f0980-9315-11ed-9b95-0242ac110002", "name": "new name"},
    tableName=tableName
)