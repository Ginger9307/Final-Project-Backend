from flaskserver import app, socketIO


app.debug= True

app.host = 'localhost'

if __name__ == "__main__":
    socketIO.run(app)