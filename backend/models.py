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

class Channels(db.Model):
    
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    name = db.Column(db.String(80), nullable = False)
    user0 = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = True)
    user1 = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = True,default=None)
    user2 = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = True,default=None)
    user3 = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = True,default=None)

    user0_name = db.Column(db.String(80), nullable = True, default=None)
    user1_name = db.Column(db.String(80), nullable = True, default=None)
    user2_name = db.Column(db.String(80), nullable = True, default=None)
    user3_name = db.Column(db.String(80), nullable = True, default=None)



    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'user1': self.user0,
            'user2': self.user1,
            'user3': self.user2,
            'user4': self.user3,
            'user1_name': self.user0_name,
            'user2_name': self.user1_name,
            'user3_name': self.user2_name,
            'user4_name': self.user3_name
        }

class Messages(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    
    message = db.Column(db.String(500), nullable = False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), nullable = False)

    server_msg = db.Column(db.Boolean, default=False)

    channel = db.relationship('Channels', backref='messages')
    user = db.relationship('Users', backref='messages')

    def to_json(self):
        return {
            'id': self.id,
            'channel_id': self.channel_id,
            'user_id': self.user_id,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'server_msg': self.server_msg
        }
    

