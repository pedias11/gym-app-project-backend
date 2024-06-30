import mongoengine as me

class UserSessionItem (me.Document):
    email= me.StringField(required=True)
    date= me.StringField(required=True)
    time= me.StringField(required=True)
    meta = {"collection": "sessions", "db_alias": "gym-app-project"}

