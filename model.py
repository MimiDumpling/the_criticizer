"""Models and database functions for The Criticizer."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful represenation when printed. """

        return "<user user_id=%s email=%s>" % (self.user_id, self.email)


class Movie(db.Model):
    """Movie of ratings website."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(130), nullable=False)
    released_at = db.Column(db.DateTime, nullable=False)
    imdb_url = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        """Provide helpful represenation when printed. """

        return "<movie movie_id=%s title=%s released_at=%s imdb_url=%s>" % (self.movie_id, 
                                            self.title, self.released_at, self.imdb_url)


class Rating(db.Model):
    """Rating of ratings website."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer, nullable=False)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("ratings",
                                              order_by=rating_id))

    # Define relationship to movie
    movie = db.relationship("Movie",
                            backref=db.backref("ratings",
                                               order_by=rating_id))

    def __repr__(self):
        """Provide helpful represenation when printed. """

        return "<rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (self.rating_id, 
                                            self.movie_id, self.user_id, self.score)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to Flask app."""

    # Configure to use PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
