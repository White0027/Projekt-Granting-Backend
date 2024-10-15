import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

tableName='actopics'
gqltype = 'AcTopicGQLModel'
endpointPrefix = "acTopic"
attributeNames=["id"]
test_reference_topic = createResolveReferenceTest(
    tableName=tableName, gqltype=gqltype, attributeNames=attributeNames)
test_page_topic = createPageTest(queryEndpoint=endpointPrefix + "Page", 
    tableName=tableName, attributeNames=attributeNames)
test_by_id_topic = createByIdTest(queryEndpoint=endpointPrefix + "ById", 
    tableName=tableName, attributeNames=attributeNames)


test_insert_program_topic = createFrontendQuery(
    query="""mutation ($id: UUID!, $semester_id: UUID!, $name: String!, $name_en: String) {
        result: programTopicInsert(topic: {
                id: $id, name: $name, nameEn: $name_en,
                semesterId: $semester_id
            }) {
            id
            msg
            result: topic {
                id
                lastchange
                name
                nameEn

                order
                semester { id }
                lessons { id }
            }
        }
    }""",
    variables={
        "id": "b8f58e3e-3e05-4dbc-b84e-86a3ea08f949", 
        "semester_id": "ce250af4-b095-11ed-9bd8-0242ac110002",
        "name": "new name"

    }
)

test_update_program_topic = createUpdateQuery(
    query="""mutation ($id: UUID!, $lastchange: DateTime!, $order: Int, $name: String) {
        result: programTopicUpdate(topic: {
                id: $id, order: $order, lastchange: $lastchange
                name: $name
            }) {
            id
            msg
            result: topic {
                id
                name
            }
        }
    }""",
    variables={
        "id": "ce250b44-b095-11ed-9bd8-0242ac110002", 
        "name": "new name",
        "order": 2},
    tableName=tableName
)