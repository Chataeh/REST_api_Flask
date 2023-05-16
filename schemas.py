#유효성 검사를 간단하게 하기위함
from marshmallow import Schema, fields

class PlainItemSchema(Schema): #store에 대한 정보 없음
    id = fields.Int(dump_only=True) #리턴 데이터만 사용
    name = fields.Str(required=True) #요청으로 오는 데이터
    price =fields.Float(required=True)
    

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True) 
    name = fields.Str(required=True) 

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True) 
    name = fields.Str()

class ItemUpdateSchema(Schema):
    name = fields.Str() 
    price =fields.Float()
    store_id =fields.Int()


class ItemSchema(PlainItemSchema):
    store_id =fields.Int(required=True, load_only=True) # load_only  데이터 형식을 변환하는 작업무시 민감한 정보
    store = fields.Nested(PlainStoreSchema(),dump_only=True)
    tags =fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class StoreSchema(PlainStoreSchema):
    items =fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags =fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    store_id =fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(),dump_only=True)
    items =fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id =fields.Int(dump_only=True)
    username =fields.Str(required=True)
    password =fields.Str(required=True, load_only=True)