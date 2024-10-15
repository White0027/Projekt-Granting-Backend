import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

tableName='aclessontypes'
gqltype = 'AcLessonTypeGQLModel'
endpointPrefix = "acLessonType"
attributeNames=["id", "name"]
test_reference_lesson_type = createResolveReferenceTest(
    tableName=tableName, gqltype=gqltype, attributeNames=attributeNames)
test_page_lesson_type = createPageTest(queryEndpoint=endpointPrefix + "Page", 
    tableName=tableName, attributeNames=attributeNames)
test_by_id_lesson_type = createByIdTest(queryEndpoint=endpointPrefix + "ById", 
    tableName=tableName, attributeNames=attributeNames)


test_insert_lesson_type = createFrontendQuery(
    query="""mutation (
            $id: UUID!, $name: String!, $name_en: String
            ) {
        result: programLessonTypeInsert(lessonType: 
            {
                id: $id, name: $name, nameEn: $name_en
            }) {
            id
            msg
            result: lessonType {
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

test_lesson_update = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String, $name_en: String, $lastchange: DateTime!) {
        result: programLessonTypeUpdate(
            lessonType: {id: $id, name: $name, nameEn: $name_en, lastchange: $lastchange}) {
            id
            msg
            result: lessonType {
                id
                name
            }
        }
    }""",
    variables={"id": "e2b7c66a-95e1-11ed-a1eb-0242ac120002", "name": "new name"},
    tableName=tableName
)