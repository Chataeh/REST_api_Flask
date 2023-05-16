#블루프린팅
import os
import secrets
from flask import Flask,jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

from db import db
from blocklist import BLOCKLIST #토큰저장할 장소
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

def create_app(db_url=None):
    app = Flask(__name__, instance_path=os.getcwd())
    #load_dotenv()#.env 위치 

    app.config["PROPGATE_EXCEPTIONS"] = True #예외처리
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] =  db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)

    migrate =Migrate(app,db)
    
    api = Api(app)


    app.config["JWT_SECRET_KEY"] = "163702755017996228350073067859438992819" #secrets.SystemRandom().getrandbits(128) # 128비트 비밀키
    jwt =JWTManager(app) #jwt 인스턴스 jwt : json 포맷을 이용하여 사용사에대한 속성을 저장하는 웹 토큰

    @jwt.token_in_blocklist_loader #jwt받을때마다 실행
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST #jti는 jwt 고유 식별자

    @jwt.revoked_token_loader #토큰이 없을시 오류
    def revoked_token_callback(jwt_header,jwt_payload):
        return(
            jsonify(
            {"description": "The token has been revoked.","error":"token_revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header,jwt_payload):
        return(
            jsonify(
            {
                "description":"The token is not fresh.",
                "error":"fresh_token_required"
            }
            ),
            401,
        )


    @jwt.additional_claims_loader #claim 추가 잘 쓰진 않음
    def add_claims_to_jwt(identity):
        if identity ==1:
            return {"is_admin" :True}
        return {"is_admin":False}
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (jsonify({"message":"The token has expired.","error":"token_expired"}),401,)


    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify({"message":"Signature verification failed.","error":"invalid_token"}),401,)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({"description":"Request does not contain an access token.","error":"authorization_token"}),401,)



    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint) #리소스 파일에서 정의한 blp변수
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app