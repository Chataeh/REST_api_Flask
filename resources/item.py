from flask.views import MethodView
from flask_smorest import Blueprint,abort  # 블루프린트 연관있는 여러개의 뷰를 그룹으로 처리 각각의 뷰를 블루프린트에 등록후 블루프린트를 앱에 등록
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import ItemModel
from schemas import ItemSchema,ItemUpdateSchema

blp = Blueprint("Items","items",description ="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()#jwt가 있어야 접근가능 패킷 header에 넣어줌
    @blp.response(200, ItemSchema)
    def get(self,item_id):
        item = ItemModel.query.get_or_404(item_id) #기본키로 찾기기본키 없을시 오류
        return item

    @jwt_required()#jwt가 있어야 접근가능 패킷 header에 넣어줌
    def delete(self,item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"): #False일시 실행불가
            abort(401, message="Admin privilege required.")
        item = ItemModel.query.get_or_404(item_id) #기본키로 찾기기본키 없을시 오류
        db.session.delete(item)
        db.session.commit()

        return {"message":"Item deleted"}

    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data,item_id):
        item = ItemModel.query.get(item_id) #기본키로 찾기기본키 없을시 오류
        if item: #아이템 존재시 업데이트
            item.price = item_data["price"]
            item.name = item_data["name"]
        else: #없으면 기존
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()#jwt가 있어야 접근가능 header에 넣어줌
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)#jwt가 있어야 접근가능 header에 넣어줌
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,item_data):
        item =ItemModel(**item_data)

        try:
            db.session.add(item) #데이터베이스에 데이터 쓰고
            db.session.commit()#커밋
        except SQLAlchemyError: 
            abort(500,message="An error occurred while inserting the item.")

        return item
