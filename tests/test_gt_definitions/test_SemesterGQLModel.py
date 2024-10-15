import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

tableName='acsemesters'
gqltype = 'AcSemesterGQLModel'
endpointPrefix = "acSemester"
attributeNames=["id"]
test_reference_semester = createResolveReferenceTest(
    tableName=tableName, gqltype=gqltype, attributeNames=attributeNames)
test_page_semester = createPageTest(queryEndpoint=endpointPrefix + "Page", 
    tableName=tableName, attributeNames=attributeNames)
test_by_id_semester = createByIdTest(queryEndpoint=endpointPrefix + "ById", 
    tableName=tableName, attributeNames=attributeNames)


test_insert_program_semester = createFrontendQuery(
    query="""mutation ($id: UUID!, $subject_id: UUID!, $classificationtype_id: UUID!) {
        result: programSemesterInsert(semester: {
                id: $id, subjectId: $subject_id,
                classificationtypeId: $classificationtype_id
            }) {
            id
            msg
            result: semester {
                id
                lastchange
                order

                subject { id }
                classifications { id }
                classificationType { id }
                topics { id }

            }
        }
    }""",
    variables={
        "id": "b8f58e3e-3e05-4dbc-b84e-86a3ea08f949", 
        "subject_id": "ce250a68-b095-11ed-9bd8-0242ac110002",
        "classificationtype_id": "a00a0642-b095-11ed-9bd8-0242ac110002",

    }
)

test_update_program_semester = createUpdateQuery(
    query="""mutation ($id: UUID!, $lastchange: DateTime!, $order: Int) {
        result: programSemesterUpdate(semester: {id: $id, order: $order, lastchange: $lastchange}) {
            id
            msg
            result: semester {
                id
            }
        }
    }""",
    variables={"id": "ce250af4-b095-11ed-9bd8-0242ac110002", "order": 2},
    tableName=tableName
)