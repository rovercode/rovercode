from app import app

if __name__ == "__main__":
    init_rover_service()
    socketio.run(app, host='0.0.0.0', debug=True)
