from app import db,Blog

db.drop_all()
db.create_all()

b1 = Blog("python","flask")
b2 = Blog("榜一","乔碧罗")
b3 = Blog("唱,跳,rap,篮球","蔡徐坤")

db.session.add_all([b1,b2,b3])

db.session.commit()