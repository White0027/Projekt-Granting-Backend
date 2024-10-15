import pytest
from .gt_utils import (
    createFrontendQuery
)


test_insert_program_classification = createFrontendQuery(
    query="""{ sayHelloGranting }""",
    variables={ }
)

