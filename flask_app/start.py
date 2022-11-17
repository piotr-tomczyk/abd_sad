from app import app
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import relationship
from app.database.database import db
from datetime import datetime
import pandas as pd

class Media(db.Model):
    __tablename__ = "Media"
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    language = db.Column(db.String(128), unique=False, nullable=False)
    localisation = db.Column(db.String(128), unique=False, nullable=False)

class Genre(db.Model):
    __tablename__ = "Genres"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(128), unique=False, nullable=False)

    def __init__(
        self,
        name,
    ):
        self.name = name

genre_table = db.Table('genre_table',
                    db.Column('grenre_id', db.Integer, db.ForeignKey('Genres.id')),
                    db.Column('movie_id', db.Integer, db.ForeignKey('Movies.id'))
                    )
class Movie(Media):
    __tablename__ = "Movies"
    members = relationship('Roles', lazy='select')
    genres = relationship('Genres', secondary=genre_table, backref='Movies')
    def __init__(
        self,
        title,
        year,
        language,
        localisation,
    ):
        self.title = title
        self.year = year
        self.language = language
        self.localisation = localisation

class Series(Media):
    __tablename__ = "Series"
    start_date = db.Column(db.DateTime, unique=False, nullable=False)
    end_date = db.Column(db.DateTime, unique=False, nullable=True)
    seasons = relationship('Seasons', lazy='select')


    def __init__(
        self,
        title,
        year,
        language,
        localisation,
        start_date,
        end_date
    ):
        self.title = title
        self.year = year
        self.language = language
        self.localisation = localisation
        self.start_date = start_date
        self.end_date = end_date
 
class Episode(Movie):
    __tablename__ = "Episodes"
    episode_number = db.Column(db.Integer, unique=False, nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('Seasons.id'))

    def __init__(
        self,
        title,
        year,
        language,
        localisation,
        episode_number,
        season_id
    ):
        self.title = title
        self.year = year
        self.language = language
        self.localisation = localisation
        self.episode_number = episode_number
        self.season_id = season_id

class Season(db.Model):
    __tablename__ = "Seasons"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    season_number = db.Column(db.Integer, unique=False, nullable=False)
    series_id = db.Column(db.Integer, db.ForeignKey('Series.id'))
    episodes = relationship('Episodes', lazy='select')


    def __init__(
        self,
        season_number,
        series_id,
    ):
        self.season_number = season_number
        self.series_id = series_id
class Role(db.Model):
    __tablename__ = "Roles"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    surname = db.Column(db.String(128), unique=False, nullable=False)
    role_name = db.Column(db.String(128), unique=False, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movies.id'))


    def __init__(
        self,
        name,
        surname,
        role_name,
        movie_id
    ):
        self.name = name
        self.surname = surname
        self.role_name = role_name
        self.movie_id = movie_id



def load_data_from_csv():
    print("START LOADINAAAAAAAAAAAAAAa")
    doctors_csv = pd.read_csv(r"./sample_data/doctors.csv", delimiter=";")
    global doctors_df
    doctors_df = pd.DataFrame(
        doctors_csv,
        columns=[
            "pesel",
            "name",
            "surname",
            "email",
            "phone_num",
            "born",
            "address",
            "disability",
            "medical_specialization",
        ],
    )

    patients_csv = pd.read_csv(r"./sample_data/patients.csv", delimiter=";")
    global patients_df
    patients_df = pd.DataFrame(
        patients_csv,
        columns=[
            "pesel",
            "name",
            "surname",
            "email",
            "phone_num",
            "born",
            "address",
            "disability",
            "medical_offer",
        ],
    )

    medical_interviews_csv = pd.read_csv(
        r"./sample_data/medicalInterviews.csv", delimiter=";"
    )
    global medical_interviews_df
    medical_interviews_df = pd.DataFrame(
        medical_interviews_csv,
        columns=[
            "id_meeting",
            "hygiene",
            "treatment_story",
            "email",
            "interview_description",
        ],
    )

    meetings_csv = pd.read_csv(r"./sample_data/meetings.csv", delimiter=";")
    global meetings_df
    meetings_df = pd.DataFrame(
        meetings_csv,
        columns=["id_doctor", "id_patient", "meeting_time", "meeting_description"],
    )

    print(doctors_df)
    print(patients_df)
    print(medical_interviews_df)
    print(meetings_df)

    print("STOP LOADINGGGGGGGGGGGGGGGGGGGGGGGGGGGG")


def create_db_schema():
    with app.app_context():
        db.drop_all()
    with app.app_context():
        db.create_all()
        db.session.commit()


def load_doctors_to_database_from_global_df():
    with app.app_context():
        for index, row in doctors_df.iterrows():
            db.session.add(
                Doctor(
                    pesel=row["pesel"],
                    name=row["name"],
                    surname=row["surname"],
                    email=row["email"],
                    phone_num=row["phone_num"],
                    born=datetime.strptime(str(row["born"]), "%b %d %Y"),
                    address=row["address"],
                    disablity=bool(row["disability"]),
                    medical_specialization=row["medical_specialization"],
                )
            )
        db.session.commit()


def load_patients_to_database_from_global_df():
    with app.app_context():
        for index, row in patients_df.iterrows():
            db.session.add(
                Patient(
                    pesel=row["pesel"],
                    name=row["name"],
                    surname=row["surname"],
                    email=row["email"],
                    phone_num=row["phone_num"],
                    born=datetime.strptime(str(row["born"]), "%b %d %Y"),
                    address=row["address"],
                    disablity=bool(row["disability"]),
                    medical_offer=row["medical_offer"],
                )
            )
        db.session.commit()


def load_meetings_to_database_from_global_df():
    with app.app_context():
        for index, row in meetings_df.iterrows():
            db.session.add(
                Meeting(
                    id_doctor=row["id_doctor"],
                    id_patient=row["id_patient"],
                    meeting_time=datetime.strptime(
                        str(row["meeting_time"]), "%b %d %Y %I:%M%p"
                    ),
                    meeting_description=row["meeting_description"],
                )
            )
        db.session.commit()


def load_medical_interviews_to_database_from_global_df():
    with app.app_context():
        for index, row in medical_interviews_df.iterrows():
            db.session.add(
                Medical_interview(
                    id_meeting=row["id_meeting"],
                    hygiene=row["hygiene"],
                    treatment_story=row["treatment_story"],
                    interview_description=row["interview_description"],
                )
            )
        db.session.commit()



app = Flask(__name__, template_folder="app/templates")
app.config.from_object("app.config.Config")
db.init_app(app)
migrate = Migrate(app, db)
create_db_schema()
# setup_database_and_load_small_data()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


# def configure_dependencies(binder):
#     binder.bind(SQLAlchemy, to=db, scope=flask_injector.singleton)

# flask_injector.FlaskInjector(app=app, modules=[configure_dependencies])
# print("DONE")
