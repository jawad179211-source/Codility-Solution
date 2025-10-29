from flask import Flask
from database import db
from routes.user_routes import user_bp
from routes.post_routes import post_routes  # import posts


app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mini_facebook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register Blueprint
app.register_blueprint(user_bp)

app.register_blueprint(post_routes)


# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to Mini-Facebook API!"

if __name__ == '__main__':
    app.run(debug=True)

