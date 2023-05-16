import uuid
from flask import  request
from flask.views import MethodView
from flask_smorest import Blueprint,abort  # 블루프린트 연관있는 여러개의 뷰를 그룹으로 처리 각각의 뷰를 블루프린트에 등록후 블루프린트를 앱에 등록
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores",__name__,description ="Operations on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()

        return {"message":"Store deleted"}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self,store_data):
        store =StoreModel(**store_data)

        try:
            db.session.add(store) #데이터베이스에 데이터 쓰고
            db.session.commit()#커밋
        except  IntegrityError: #무결성 오류 
            abort(400,message="A store with that name already exists")
        except SQLAlchemyError: 
            abort(500,message="An error occurred while inserting the store.")
        return store, 201 #상태코드 201 요청이 성공적처리, 자원이 생성되었음 나타냄

