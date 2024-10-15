import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

tableName='acclassificationlevels'
gqltype = 'AcClassificationLevelGQLModel'
endpointPrefix = "acClassificationLevel"
attributeNames=["id"]
test_reference_classificationlevel = createResolveReferenceTest(
    tableName=tableName, gqltype=gqltype, attributeNames=attributeNames)
test_page_classificationlevel = createPageTest(queryEndpoint=endpointPrefix + "Page", 
    tableName=tableName, attributeNames=attributeNames)
test_by_id_classificationlevel = createByIdTest(queryEndpoint=endpointPrefix + "ById", 
    tableName=tableName, attributeNames=attributeNames)


# test_insert_program_classificationlevel = createFrontendQuery(
#     query="""mutation ($id: UUID!, $date: DateTime!, $order: Int!
#             $student_id: UUID!, $semester_id: UUID! 
#             $classificationlevellevel_id: UUID!
#         ) {
#         result: programClassificationlevelInsert(classificationlevel: {
#                 id: $id, date: $date, order: $order
#                 studentId: $student_id, semesterId: $semester_id,
#                 classificationlevelId: $classificationlevel_id
#             }) {
#             id
#             msg
#             result: classificationlevel {
#                 id
#                 lastchange
#                 date
#                 order
#                 student { id }
#                 semester { id }
#                 level { id }


#             }
#         }
#     }""",
#     variables={
#         "id": "96737ec5-699f-420f-b8e2-143f3d68229d", 
#         "student_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
#         "semester_id": "ce250af4-b095-11ed-9bd8-0242ac110002",
#         "classificationlevel_id": "5faea396-b095-11ed-9bd8-0242ac110002",
#         "date": "2024-12-24T08:00:00",
#         "order": 1
#     }
# )

# test_update_program_classificationlevel = createUpdateQuery(
#     query="""mutation ($id: UUID!, $lastchange: DateTime!,
#             $date: DateTime, $order: Int,
#             $classificationlevel_id: UUID
#         ) {
#         result: programClassificationlevelUpdate(classificationlevel: {
#                 id: $id, lastchange: $lastchange
#                 date: $date, order: $order,
#                 classificationlevelId: $classificationlevel_id 
#             }) {
#             id
#             msg
#             result: classificationlevel {
#                 id
                
#             }
#         }
#     }""",
#     variables={
#         "id": "ce250bd0-b095-11ed-9bd8-0242ac110002", 
#         "student_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
#         "semester_id": "ce250af4-b095-11ed-9bd8-0242ac110002",
#         "classificationlevel_id": "5faea396-b095-11ed-9bd8-0242ac110002",
#         "order": 1
#     },
#     tableName=tableName
# )