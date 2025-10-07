from flask import request, jsonify,session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import app, db,jwt,socket,emit,join_room,leave_room
from models import Rooms,Users, Strokes
import os
import bcrypt



@app.route('/create_user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    if not name or not password:
        return jsonify({"error": "Name and password are required"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:

        new_user = Users(name=name, password=hashed_password.decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User added successfully", "user": new_user.to_json()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/get_users', methods=['GET'])
def get_users():
    try:
        users = Users.query.all()
        json_users = list(map(lambda x: x.to_json(), users))

        return jsonify({"users": json_users})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    if not name or not password:
        return jsonify({"error": "Name and password are required"}), 400

    user = Users.query.filter_by(name=name).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"message": "Password is correct", "access_token": create_access_token(identity=str(user.id),additional_claims={"name": user.name})
}), 200
    else:
        return jsonify({"error": "Incorrect password"}), 401

@socket.on('join_canvas')
def handle_join_canvas(data):
    user_name = data.get("user_name")
    if not user_name:
        return
    print(f"{user_name} joined the canvas")
    join_room(user_name)
    emit('user_joined', {'message': f'{user_name} has joined the canvas'}, broadcast=True)

@socket.on('draw')
def handle_draw(data):
    room = data.get('room')
    user_id = data.get('user_id')
    fromX = data.get('fromX')
    fromY = data.get('fromY')
    toX = data.get('toX')
    toY = data.get('toY')
    opacity = data.get('opacity')
    lineWidth = data.get('lineWidth')
    color = data.get('color')

    if None in (fromX, fromY, toX, toY):
        return
    if room:
        emit('draw', data, room=room)
        new_stroke = Strokes(
            room_id=room,
            user_id=user_id,
            fromX=fromX,
            fromY=fromY,
            toX=toX,
            toY=toY,
            opacity=opacity,
            lineWidth=lineWidth,
            color=color
        )
        db.session.add(new_stroke)
        db.session.commit()


@app.route('/create_room', methods=['POST'])
@jwt_required()
def create_room():
    data = request.get_json()
    name = data.get('name')
    user_ids = []
    user_names = []

    for i in range(8):
        user_name = data.get(f'user{i}')

        user = Users.query.filter_by(name=user_name).first()
        if not user and user_name:
            return jsonify({"error": f"User {user_name} not found"}), 404
        user_ids.append(user.id if user else None)
        user_names.append(user.name if user else None)

    try:
        new_room = Rooms(name=name, user0=int(get_jwt_identity()))

        for i in range(1, 8):
            if user_ids[i]:
                setattr(new_room, f'user{i}', user_ids[i])

        for i in range(8):
            if user_names[i]:
                setattr(new_room, f'user{i}_name', user_names[i])

        db.session.add(new_room)
        db.session.commit()
        
        return jsonify({"message": "Room created successfully", "room": new_room.to_json()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/update_room', methods=['PATCH'])
@jwt_required()
def update_room():
    data = request.get_json()
    room_id = data.get('room_id')
    room = Rooms.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404
    current_user_id = int(get_jwt_identity())

    room_name = data.get('name', room.name)

    users = []

    for i in range(8):
        user_name = data.get(f'user{i}')

        user = Users.query.filter_by(name=user_name).first()
        if not user and user_name:
            return jsonify({"error": f"User {user_name} not found"}), 404
        users.append(user if user else None)

    if current_user_id not in [room.user0, room.user1, room.user2, room.user3,room.user4,room.user5,room.user6,room.user7]:
        return jsonify({"error": "You are not authorized to update this room"}), 403

    if not room_id:
        return jsonify({"error": "Room ID and exactly four user IDs are required"}), 400

    try:
        room = Rooms.query.get(room_id)
        if not room:
            return jsonify({"error": "Room not found"}), 404

        room.name = room_name

        for i in range(4):
            if users[i]:
                setattr(room, f'user{i}', users[i].id)
                setattr(room, f'user{i}_name', users[i].name)
            else:
                setattr(room, f'user{i}', None)
                setattr(room, f'user{i}_name', None)

        db.session.commit()

        return jsonify({"message": "Room updated successfully", "room": room.to_json()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/get_rooms/<string:search>', methods=['GET'])
@jwt_required()
def get_rooms(search):

    user_id = int(get_jwt_identity())
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404


    try:
        if search != "NULLNULL":
            rooms = Rooms.query.filter(Rooms.name.ilike(f'%{search}%')).all()
        else:
            json_rooms = list(map(lambda x: x.to_json(),rooms))

        return jsonify({"rooms" : json_rooms})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_messages/<int:room_id>', methods=['GET'])
@jwt_required()
def get_strokes(room_id):

    user_id = int(get_jwt_identity())
    room = Rooms.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    if user_id not in [room.user1, room.user2, room.user3, room.user0]:
        return jsonify({"error": "User not in room"}), 403



    strokes = room.strokes.order_by(Strokes.id.asc()).all()


    return jsonify({"strokes": jsonify(list(map(lambda x: x.to_json(), strokes))).json})

@app.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    try:
        current_user = get_jwt_identity()  # Returns whatever you put in 'identity' during login
        return jsonify(message=f"Hello, {current_user}! This is your dashboard.")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()


    port = int(os.environ.get("PORT", 5000))
    socket.run(app,host='0.0.0.0',port=5000)