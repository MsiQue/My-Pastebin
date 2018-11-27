import random
import os
from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/pastebin'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  ####################这句话不写好像会CE
db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = "pastebin"
	id = db.Column(db.Integer, primary_key=True)
	poster = db.Column(db.String(50))
	content = db.Column(db.String(10000))
	def __init__(self, id, poster, content):
		self.id = id
		self.poster = poster
		self.content = content
	
	def __repr__(self):
		print("id:%s,username:%s"%(id,username))
		
db.create_all()
db.drop_all()
db.create_all()

@app.route('/')
def Form():
	return render_template("form.html")

@app.route('/pastebin' , methods = ['GET' , 'POST'])
def Submit():
	id = random.randint(10000000, 99999999)
	poster = request.form.get("poster")
	content = request.form.get("content")
	Item = User(id, poster, content)
	db.session.add(Item)
	db.session.commit()
	a = request.url.split('/')
	#return "Successfully!  your code are in   %s//%s/id%d"%(a[0],a[2],id)
	return redirect("%s//%s/id%d"%(a[0],a[2],id))
	

@app.route('/id<Num>')
def Query(Num):
	Item = User.query.filter_by(id=Num).first()
	#return "id = %d  poster = %s, code = %s" %(Item.id, Item.poster, Item.content)
	return'''
	<!doctype html>
	<html>
		<head>
			<title>pastebin</title>
		</head>
		
		<style>
			#a{
				font-size:50px;
				text-align:center;
			}
			#b{
				text-align:center;
			}
		</style>
		
		<body>
			<div id='a'> Pastebin </div>
			<br>
			<div id='b'>
				<form name="form" action="pastebin" method="post">
					Poster: %s 
					<br><br><br>
					Content:
					<br>
					<textarea name="content" cols="100" rows="30">%s</textarea>
			</div>
			</form>
		</body>
	</html>
	'''%(Item.poster, Item.content)

	
if __name__ == '__main__':
	app.run(debug='true')