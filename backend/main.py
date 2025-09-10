from flask import request, jsonify,session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import app, db,jwt,socket,emit
from models import Channels,Messages, Users
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
    emit('user_joined', {'message': f'{user_name} has joined the canvas'}, broadcast=True)

@socket.on('draw')
def handle_draw(data):
    fromX = data.get('fromX')
    fromY = data.get('fromY')
    toX = data.get('toX')
    toY = data.get('toY')
    if None in (fromX, fromY, toX, toY):
        return
    emit('draw', data, broadcast=True)

@app.route('/create_channel', methods=['POST'])
@jwt_required()
def create_channel():
    data = request.get_json()
    name = data.get('name')
    user_ids = []
    user_names = []

    for i in range(4):
        user_name = data.get(f'user{i}')

        user = Users.query.filter_by(name=user_name).first()
        if not user and user_name:
            return jsonify({"error": f"User {user_name} not found"}), 404
        user_ids.append(user.id if user else None)
        user_names.append(user.name if user else None)

    try:
        new_channel = Channels(name=name, user0=int(get_jwt_identity()))

        for i in range(1, 4):
            if user_ids[i]:
                setattr(new_channel, f'user{i}', user_ids[i])

        for i in range(4):
            if user_names[i]:
                setattr(new_channel, f'user{i}_name', user_names[i])


        db.session.add(new_channel)
        db.session.commit()

        created_msg = Messages(
            channel_id=new_channel.id,
            user_id=int(get_jwt_identity()),
            message=f"Channel '{name}' created by {Users.query.get(int(get_jwt_identity())).name}",
            server_msg=True
        )
        added_messages = [created_msg]
        for i in range(1, 4):
            if user_ids[i]:
                added_messages.append(Messages(
                    channel_id=new_channel.id,
                    user_id=user_ids[i],
                    message=f"{Users.query.get(user_ids[i]).name} was added to the channel",
                    server_msg=True
                ))


        for msg in added_messages:
            db.session.add(msg)
            db.session.commit()

        return jsonify({"message": "Channel created successfully", "channel": new_channel.to_json()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/update_channel', methods=['PATCH'])
@jwt_required()
def update_channel():
    data = request.get_json()
    channel_id = data.get('channel_id')
    channel = Channels.query.get(channel_id)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404
    current_user_id = int(get_jwt_identity())
    current_user_name = Users.query.get(current_user_id).name

    channel_name = data.get('name', channel.name)

    

    prev_users = [channel.user0, channel.user1, channel.user2, channel.user3]
    new_users = []
    deleted_users = []
    users = []

    for i in range(4):
        user_name = data.get(f'user{i}')

        user = Users.query.filter_by(name=user_name).first()
        if not user and user_name:
            return jsonify({"error": f"User {user_name} not found"}), 404
        users.append(user if user else None)

    if current_user_id not in [channel.user0, channel.user1, channel.user2, channel.user3]:
        return jsonify({"error": "You are not authorized to update this channel"}), 403

    if not channel_id:
        return jsonify({"error": "Channel ID and exactly four user IDs are required"}), 400

    for i in users:
        if i:
            if i.id not in prev_users:
                new_users.append(i)

    for i in prev_users:
        if i:
            if i not in [user.id for user in users if user]:
                deleted_users.append(i)
            
    msgs = []
    for i in new_users:
        msgs.append(Messages(
            channel_id=channel_id,
            user_id=current_user_id,
            message=f"{current_user_name} added {i.name} to the channel",
            server_msg=True
        ))

    for i in deleted_users:
        msgs.append(Messages(
            channel_id=channel_id,
            user_id=current_user_id,
            message=f"{current_user_name} removed {Users.query.filter_by(id=i).first().name} from the channel",
            server_msg=True
        ))
    

    if channel_name != channel.name:
        msgs.append(Messages(
            channel_id=channel_id,
            user_id=current_user_id,
            message=f"{current_user_name} changed the channel name to '{channel_name}'",
            server_msg=True
        ))

    try:
        channel = Channels.query.get(channel_id)
        if not channel:
            return jsonify({"error": "Channel not found"}), 404

        channel.name = channel_name

        for i in range(4):
            if users[i]:
                setattr(channel, f'user{i}', users[i].id)
                setattr(channel, f'user{i}_name', users[i].name)
            else:
                setattr(channel, f'user{i}', None)
                setattr(channel, f'user{i}_name', None)

        for msg in msgs:
            db.session.add(msg)
            
        db.session.commit()

        return jsonify({"message": "Channel updated successfully", "channel": channel.to_json()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/get_channels/<string:search>', methods=['GET'])
@jwt_required()
def get_channels(search):

    user_id = int(get_jwt_identity())


    try:
        if search != "NULLNULL":
            channels = Channels.query.filter(
                ((Channels.user0 == user_id) |
                 (Channels.user1 == user_id) |
                 (Channels.user2 == user_id) |
                 (Channels.user3 == user_id))
                & (Channels.name.contains(search))
            ).all()
        else:
            channels = Channels.query.filter(
                ((Channels.user0 == user_id) |
                (Channels.user1 == user_id) |
                (Channels.user2 == user_id) |
                (Channels.user3 == user_id))

            ).all()
        json_channels = list(map(lambda x: x.to_json(),channels))

        return jsonify({"channels" : json_channels})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send_message', methods=['POST'])
@jwt_required()
def send_message():
    data = request.get_json()
    channel_id = data.get('channel_id')
    user_id = int(get_jwt_identity())
    message = data.get('message')

    # Check if the user is part of the channel
    channel = Channels.query.get(channel_id)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404

    if user_id not in [channel.user1, channel.user2, channel.user3, channel.user0]:
        return jsonify({"error": "User not in channel"}), 403

    if not channel_id or not user_id or not message:
        return jsonify({"error": "Channel ID, User ID, and message are required"}), 400

    try:
        new_message = Messages(channel_id=channel_id, user_id=user_id, message=message)
        db.session.add(new_message)
        db.session.commit()

        return jsonify({"message": "Message sent successfully", "message_data": new_message.to_json()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/get_messages/<int:channel_id>/<int:last_read>', methods=['GET'])
@jwt_required()
def get_messages(channel_id,last_read):

    user_id = int(get_jwt_identity())
    channel = Channels.query.get(channel_id)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404

    if user_id not in [channel.user1, channel.user2, channel.user3, channel.user0]:
        return jsonify({"error": "User not in channel"}), 403



    messages = Messages.query.filter(
        Messages.channel_id == channel_id,
        Messages.id > last_read
    ).all()

    json_messages = list(map(lambda x: {
        'id': x.id,
        'user_id': x.user_id,
        'message': x.message,
        'user_name': Users.query.get(x.user_id).name ,
        'timestamp': x.timestamp.isoformat(),
        'server_msg': x.server_msg
    }, messages))

    return jsonify({"messages": json_messages})

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