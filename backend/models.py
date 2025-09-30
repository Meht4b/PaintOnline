from config import db



class Users(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class Rooms(db.Model):
    
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    name = db.Column(db.String(80), nullable = False)
    user0 = db.Column(db.Integer, nullable = True)
    user1 = db.Column(db.Integer, nullable = True,default=None)
    user2 = db.Column(db.Integer, nullable = True,default=None)
    user3 = db.Column(db.Integer, nullable = True,default=None)
    user4 = db.Column(db.Integer, nullable = True,default=None)
    user5 = db.Column(db.Integer, nullable = True,default=None)
    user6 = db.Column(db.Integer, nullable = True,default=None)
    user7 = db.Column(db.Integer, nullable = True,default=None)

    user0_name = db.Column(db.String(80), nullable = True, default=None)
    user1_name = db.Column(db.String(80), nullable = True, default=None)
    user2_name = db.Column(db.String(80), nullable = True, default=None)
    user3_name = db.Column(db.String(80), nullable = True, default=None)
    user4_name = db.Column(db.String(80), nullable = True, default=None)
    user5_name = db.Column(db.String(80), nullable = True, default=None)
    user6_name = db.Column(db.String(80), nullable = True, default=None)
    user7_name = db.Column(db.String(80), nullable = True, default=None)


    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'user1': self.user0,
            'user2': self.user1,
            'user3': self.user2,
            'user4': self.user3,
            'user5': self.user4,
            'user6': self.user5,
            'user7': self.user6,
            'user8': self.user7,
            'user1_name': self.user0_name,
            'user2_name': self.user1_name,
            'user3_name': self.user2_name,
            'user4_name': self.user3_name,
            'user5_name': self.user4_name,
            'user6_name': self.user5_name,      
            'user7_name': self.user6_name,
            'user8_name': self.user7_name,
        }

class Strokes(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    
    fromX = db.Column(db.Integer, nullable = False)
    fromY = db.Column(db.Integer, nullable = False)
    toX = db.Column(db.Integer, nullable = False)
    toY = db.Column(db.Integer, nullable = False)
    opacity = db.Column(db.Float, nullable = True, default=1.0)
    lineWidth = db.Column(db.Integer, nullable = True, default=1)
    color = db.Column(db.String(20), nullable = True, default="#000000")



    room = db.relationship('Rooms', backref='strokes')
    user = db.relationship('Users', backref='strokes')

    def to_json(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'user_id': self.user_id,
            'fromX': self.fromX,
            'fromY': self.fromY,
            'toX': self.toX,
            'toY': self.toY,
        }
    

