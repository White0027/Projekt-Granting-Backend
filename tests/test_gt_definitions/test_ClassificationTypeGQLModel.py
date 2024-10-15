import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

tableName='acclassificationtypes'
gqltype = 'AcClassificationTypeGQLModel'
endpointPrefix = "acClassificationType"
attributeNames=["id", "name"]
test_reference_classification_type = createResolveReferenceTest(
    tableName=tableName, gqltype=gqltype, attributeNames=attributeNames)
test_page_classification_type = createPageTest(queryEndpoint=endpointPrefix + "Page", 
    tableName=tableName, attributeNames=attributeNames)
test_by_id_classification_type = createByIdTest(queryEndpoint=endpointPrefix + "ById", 
    tableName=tableName, attributeNames=attributeNames)


test_insert_classification_type = createFrontendQuery(
    query="""mutation (
            $id: UUID!, $name: String!, $name_en: String
            ) {
        result: programClassificationTypeInsert(classificationType: 
            {
                id: $id, name: $name, nameEn: $name_en
            }) {
            id
            msg
            result: classificationType {
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
        result: programClassificationTypeUpdate(
            classificationType: {id: $id, name: $name, nameEn: $name_en, lastchange: $lastchange}) {
            id
            msg
            result: classificationType {
                id
                name
            }
        }
    }""",
    variables={"id": "a00a0642-b095-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName=tableName
)