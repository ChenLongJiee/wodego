from flask import Flask
from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
DB_URI ='mysql+pymysql://root:@127.0.0.1:3306/flaskblog'

app.config['SQLALCHEMY_DATABASE_URI']=DB_URI
# 动态追踪修改设置，如未设置只会提示警告
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
#查看生成的sql语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    def __init__(self,title,text):
        self.title = title
        self.text = text

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/blogs',methods=['GET'])
def list_notes():
    blogs = Blog.query.all()
    return render_template("list_blogs.html",blogs = blogs)

@app.route('/blogs/create',methods=['GET','POST'])
def create_blog():
    if request.method == 'GET':
        return render_template('create_blog.html')
    else:
        title = request.form['title']
        text = request.form['text']
        blog = Blog(title=title,text=text)
        db.session.add(blog)
        db.session.commit()
        return redirect('/blogs')

@app.route('/blogs/<id>',methods=['GET','DELETE'])
def query_note(id):
    if request.method == 'GET':
        blog = Blog.query.filter_by(id = id).first_or_404()
        return render_template('query_blog.html',blog=blog)
    else:
        blog = Blog.query.filter_by(id=id).delete()
        db.session.commit()
        return '',204

@app.route('/blogs/update/<id>',methods=['GET','POST'])
def update_note(id):
    if request.method == 'GET':
        blog = Blog.query.filter_by(id = id).first_or_404()
        return render_template('update_blog.html',blog = blog)
    else:
        title = request.form['title']
        text = request.form['text']
        blog = Blog.query.filter_by(id=id).update({'title':title,'text':text})
        db.session.commit()
        # return redirect('/blogs/{id}'.format(id=id))
        return redirect(url_for('query_note',id=id))

if __name__ == '__main__':
    app.run(debug = True)

