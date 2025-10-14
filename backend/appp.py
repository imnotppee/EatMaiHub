from flask import Flask
from routes.review_routes import bp as review_routes
from routes.favorite_routes import bp as favorite_routes
from urban_street import register_urban_street_routes

app = Flask(__name__)
register_urban_street_routes(app)
app.register_blueprint(review_routes)
app.register_blueprint(favorite_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
