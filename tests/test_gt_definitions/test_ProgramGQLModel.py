import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

tableName='acprograms'
gqltype = 'AcProgramGQLModel'
attributeNames=["id", "name"]
test_reference_program = createResolveReferenceTest(
    tableName=tableName, gqltype=gqltype, attributeNames=attributeNames)
test_program_page = createPageTest(queryEndpoint="acProgramPage", 
    tableName=tableName, attributeNames=attributeNames)
test_program_by_id = createByIdTest(queryEndpoint="acProgramById", 
    tableName=tableName, attributeNames=attributeNames)


test_insert_program = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!, $type_id: UUID!, $group_id: UUID!, $licenced_group_id: UUID!) {
        result: programInsert(program: {id: $id, name: $name, typeId: $type_id, groupId: $group_id, licencedGroupId: $licenced_group_id}) {
            id
            msg
            result: program {
                id
                name
                nameEn
                type { id }
                subjects { id }
                students { id }
                grantsGroup { id }
                licencedGroup { id }
                createdby { id }
                changedby { id }
                rbacobject { id }
            }
        }
    }""",
    variables={
        "id": "460229f0-b100-4b90-bd9a-c37ab4322756", 
        "name": "new name",
        "type_id": "fd4f0980-9315-11ed-9b95-0242ac110002",
        "group_id": "2d9dced0-a4a2-11ed-b9df-0242ac120003",
        "licenced_group_id": "2d9dced0-a4a2-11ed-b9df-0242ac120003"
    }
)

test_update_program = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: programUpdate(program: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            result: program {
                id
                name
            }
        }
    }""",
    variables={"id": "2766fc9a-b095-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName=tableName
)