import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

tableName='aclessons'
gqltype = 'AcLessonGQLModel'
endpointPrefix = "acLesson"
attributeNames=["id"]
test_reference_lesson = createResolveReferenceTest(
    tableName=tableName, gqltype=gqltype, attributeNames=attributeNames)
test_page_lesson = createPageTest(queryEndpoint=endpointPrefix + "Page", 
    tableName=tableName, attributeNames=attributeNames)
test_by_id_lesson = createByIdTest(queryEndpoint=endpointPrefix + "ById", 
    tableName=tableName, attributeNames=attributeNames)


test_insert_program_lesson = createFrontendQuery(
    query="""mutation ($id: UUID!, $topic_id: UUID!, $type_id: UUID! ) {
        result: programLessonInsert(lesson: {
                id: $id, 
                topicId: $topic_id, typeId: $type_id
            }) {
            id
            msg
            result: lesson {
                id
                lastchange

                count
                topic { id }
                type { id }
            }
        }
    }""",
    variables={
        "id": "b8f58e3e-3e05-4dbc-b84e-86a3ea08f949", 
        "topic_id" : "ce250b44-b095-11ed-9bd8-0242ac110002",
        "type_id": "e2b7cbf6-95e1-11ed-a1eb-0242ac120002",
        "count": 2

    }
)

test_update_program_lesson = createUpdateQuery(
    query="""mutation ($id: UUID!, $lastchange: DateTime!, 
        $type_id: UUID, $count: Int) {
        result: programLessonUpdate(lesson: {
                id: $id, lastchange: $lastchange
                typeId: $type_id, count: $count
            }) {
            id
            msg
            result: lesson {
                id
                
            }
        }
    }""",
    variables={
        "id": "ce250b8a-b095-11ed-9bd8-0242ac110002", 
        
        "count": 2},
    tableName=tableName
)