import strawberry
import uuid
import datetime
import typing
import logging

IDType = uuid.UUID

from ._GraphPermissions import OnlyForAuthentized

def getLoadersFromInfo(info: strawberry.types.Info):
    result = info.context.get("loaders", None)
    assert result is not None, "Loaders are asked for but not present in context, check context preparation"
    return result

def getUserFromInfo(info: strawberry.types.Info):
    result = info.context.get("user", None)
    if result is None:
        request = info.context.get("request", None)
        assert request is not None, "request should be in context, something is wrong"
        result = request.scope.get("user", None)
    assert result is not None, "User is wanted but not present in context or in request.scope, check it"
    return result

@classmethod
async def resolve_reference(cls, info: strawberry.types.Info, id: IDType):
    if id is None: return None
    if isinstance(id, str): id = IDType(id)
    loader = cls.getLoader(info)
    result = await loader.load(id)
    if result is not None:
        # result._type_definition = cls._type_definition  # little hack :)
        result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
    return result



@strawberry.field(
    description="""Entity primary key""",
    # permission_classes=[OnlyForAuthentized()]
    )
def resolve_id(self) -> IDType:
    return self.id

@strawberry.field(
    description="""Name """,
    permission_classes=[OnlyForAuthentized()]
    )
def resolve_name(self) -> str:
    return self.name

@strawberry.field(
    description="""English name""",
    permission_classes=[OnlyForAuthentized()]
    )
def resolve_name_en(self) -> str:
    result = self.name_en if self.name_en else ""
    return result

@strawberry.field(
    description="""Time of last update""",
    permission_classes=[OnlyForAuthentized()]
    )
def resolve_lastchange(self) -> datetime.datetime:
    return self.lastchange

@strawberry.field(
    description="""Time of entity introduction""",
    permission_classes=[OnlyForAuthentized()]
    )
def resolve_created(self) -> typing.Optional[datetime.datetime]:
    return self.created

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".GraphTypeDefinitionsExt")]

async def resolve_user(user_id):
    from .GraphTypeDefinitionsExt import UserGQLModel
    result = None if user_id is None else await UserGQLModel.resolve_reference(id=user_id, info=None)
    return result
    
@strawberry.field(description="""Who created entity""",
        permission_classes=[OnlyForAuthentized()])
async def resolve_createdby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.createdby_id)

@strawberry.field(description="""Who made last change""",
        permission_classes=[OnlyForAuthentized()])
async def resolve_changedby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.changedby_id)

RBACObjectGQLModel = typing.Annotated["RBACObjectGQLModel", strawberry.lazy(".GraphTypeDefinitionsExt")]
@strawberry.field(description="""Who made last change""",
        permission_classes=[OnlyForAuthentized()])
async def resolve_rbacobject(self, info: strawberry.types.Info) -> typing.Optional[RBACObjectGQLModel]:
    from .GraphTypeDefinitionsExt import RBACObjectGQLModel
    result = None if self.rbacobject_id is None else await RBACObjectGQLModel.resolve_reference(info, self.rbacobject_id)
    return result


def create_self_scalar_resolver(GQLType, **kwargs):
    items = list(kwargs.items())
    assert len(items) == 1, f"expected exactly one item in params of create_scalar_resolver, see {kwargs}"
    key, attribute = items[0]
    assert key == "id", f"expected id in params of create_scalar_resolver, see {kwargs}"
    async def resolver(self, info: strawberry.types.Info) -> typing.Optional[GQLType]:
        assert hasattr(self, attribute), f"self ({self}) has no attribute {attribute}"
        id = getattr(self, attribute)
        result = await GQLType.resolve_reference(info, id=id)
        return result
    return resolver

def create_self_vector_resolver(GQLType, **kwargs):
    items = list(kwargs.items())
    assert len(items) == 1, f"expected exactly one item in params of create_vector_resolver, see {kwargs}"
    key, attribute = items[0]
    async def resolver(self, info: strawberry.types.Info) -> typing.List[GQLType]:
        assert hasattr(self, attribute), f"self ({self}) has no attribute {attribute}"
        attributevalue = getattr(self, attribute)
        loader = GQLType.getLoader(info)
        params = {key: attributevalue}
        result = await loader.filter_by(**params)
        return result
    return resolver


resolve_result_id: IDType = strawberry.field(description="primary key of CU operation object")
resolve_result_msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")

from inspect import signature
import inspect 
from functools import wraps

def asPage(field, *, extendedfilter=None):
    def decorator(field):
        # print(field.__name__, field.__annotations__)
        signatureField = signature(field)
        return_annotation = signatureField.return_annotation

        skipParameter = signatureField.parameters.get("skip", None)
        skipParameterDefault = 0
        if skipParameter:
            skipParameterDefault = skipParameter.default

        limitParameter = signatureField.parameters.get("limit", None)
        limitParameterDefault = 10
        if limitParameter:
            limitParameterDefault = limitParameter.default

        whereParameter = signatureField.parameters.get("where", None)
        whereParameterDefault = None
        whereParameterAnnotation = str
        if whereParameter:
            whereParameterDefault = whereParameter.default
            whereParameterAnnotation = whereParameter.annotation

        async def foreignkeyVectorSimple(
            self, info: strawberry.types.Info,
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signature(field).return_annotation:
            loader = await field(self, info)
            results = await loader.page(skip=skip, limit=limit, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorSimple.__name__ = field.__name__
        foreignkeyVectorSimple.__doc__ = field.__doc__

        async def foreignkeyVectorComplex(
            self, info: strawberry.types.Info, 
            where: whereParameterAnnotation = None, 
            #where: typing.Optional[whereParameterAnnotation] = whereParameterDefault, 
            #where: typing.Optional[str] = None, 
            orderby: typing.Optional[str] = None, 
            desc: typing.Optional[bool] = None, 
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signatureField.return_annotation:
            # logging.info(f"waiting for a loader {where}")
            wf = None if where is None else strawberry.asdict(where)
            loader = await field(self, info, where=wf)    
            # logging.info(f"got a loader {loader}")
            # wf = None if where is None else strawberry.asdict(where)
            results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorComplex.__name__ = field.__name__
        foreignkeyVectorComplex.__doc__ = field.__doc__
        foreignkeyVectorComplex.__module__ = field.__module__
        
        if return_annotation._name == "List":
            return foreignkeyVectorComplex if whereParameter else foreignkeyVectorSimple
        else:
            raise Exception("Unable to recognize decorated function, I am sorry")

    return decorator(field) if field else decorator


async def encapsulateInsert(info, loader, entity, result):
    actinguser = getUserFromInfo(info)
    id = uuid.UUID(actinguser["id"])
    entity.createdby = id

    row = await loader.insert(entity)
    assert result.msg is not None, "result msg must be predefined (Operation Insert)"
    result.id = row.id
    return result

async def encapsulateUpdate(info, loader, entity, result):
    actinguser = getUserFromInfo(info)
    id = uuid.UUID(actinguser["id"])
    entity.changedby = id

    row = await loader.update(entity)
    result.id = entity.id if result.id is None else result.id 
    result.msg = "ok" if row is not None else "fail"
    return result

def asForeignList(*, foreignKeyName: str):
    assert foreignKeyName is not None, "foreignKeyName must be defined"
    def decorator(field):
        print(field.__name__, field.__annotations__)
        signatureField = signature(field)
        return_annotation = signatureField.return_annotation

        skipParameter = signatureField.parameters.get("skip", None)
        skipParameterDefault = skipParameter.default if skipParameter else 0

        limitParameter = signatureField.parameters.get("limit", None)
        limitParameterDefault = limitParameter.default if limitParameter else 10

        whereParameter = signatureField.parameters.get("where", None)
        whereParameterDefault = whereParameter.default if whereParameter else None
        whereParameterAnnotation = whereParameter.annotation if whereParameter else str

        async def foreignkeyVectorSimple(
            self, info: strawberry.types.Info,
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signature(field).return_annotation:
            extendedfilter = {}
            extendedfilter[foreignKeyName] = self.id
            loader = field(self, info)
            if inspect.isawaitable(loader):
                loader = await loader
            results = await loader.page(skip=skip, limit=limit, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorSimple.__name__ = field.__name__
        foreignkeyVectorSimple.__doc__ = field.__doc__
        foreignkeyVectorSimple.__module__ = field.__module__

        async def foreignkeyVectorComplex(
            self, info: strawberry.types.Info, 
            where: whereParameterAnnotation = whereParameterDefault, 
            orderby: typing.Optional[str] = None, 
            desc: typing.Optional[bool] = None, 
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signatureField.return_annotation:
            extendedfilter = {}
            extendedfilter[foreignKeyName] = self.id
            loader = field(self, info)
            if inspect.isawaitable(loader):
                loader = await loader
            
            wf = None if where is None else strawberry.asdict(where)
            results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorComplex.__name__ = field.__name__
        foreignkeyVectorComplex.__doc__ = field.__doc__
        foreignkeyVectorComplex.__module__ = field.__module__

        async def foreignkeyVectorComplex2(
            self, info: strawberry.types.Info, 
            where: whereParameterAnnotation = whereParameterDefault, 
            orderby: typing.Optional[str] = None, 
            desc: typing.Optional[bool] = None, 
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signatureField.return_annotation: #typing.List[str]:
            extendedfilter = {}
            extendedfilter[foreignKeyName] = self.id
            loader = field(self, info)
            
            wf = None if where is None else strawberry.asdict(where)
            results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorComplex2.__module__ = field.__module__
        if return_annotation._name == "List":
            return foreignkeyVectorComplex if whereParameter else foreignkeyVectorSimple
        else:
            raise Exception("Unable to recognize decorated function, I am sorry")

    return decorator