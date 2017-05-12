from app import db

class Video(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	videoid = db.Column(db.String(20), index=True, unique=True)
	title = db.Column(db.String(100))
	description = db.Column(db.String(4850))
	published = db.Column(db.DateTime()) 
	thumbnail_url = db.Column(db.String(60))
	
	def __repr__(self):
		return '<Video %r>' % (self.title)