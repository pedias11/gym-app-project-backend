import mongoengine as me
from werkzeug.security import generate_password_hash


class User(me.Document):
    firstname = me.StringField(required=True)
    lastname = me.StringField(required=True)
    email = me.StringField(required=True, unique=True)
    password = me.StringField(required=True)
    subscription = me.StringField()
    role = me.StringField(default='user', choices=['user', 'admin'])
    meta = {"collection": "users", "db_alias": "gym-app-project"}

    def save(self, *args, **kwargs):
        self.password = generate_password_hash(self.password)
        super(User, self).save(*args, **kwargs)

    
    