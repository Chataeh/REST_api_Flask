from db import db

class StoreModel(db.Model): #상속 받음
    __tablename__ = "stores" #테이블 이름
    #테이블 생성
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique =True, nullable=False)
    items = db.relationship("ItemModel",back_populates="store",lazy="dynamic",cascade="all, delete")#cascade 구현
    tags = db.relationship("TagModel",back_populates="store",lazy="dynamic")#back_populates 객체간의 양방향 관계 lazy 객체 언제 가져올지 정으 어떤 조건으로 가져오는지 dynamic은 쿼리 객체반환