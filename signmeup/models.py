from google.appengine.ext import db

class SignupTopic(db.Expando):
    owner = db.UserProperty()
    name = db.StringProperty(required = True)
    description = db.TextProperty()
    timestamp = db.DateTimeProperty(auto_now_add = True)

class UserSignup(db.Model):
    user = db.UserProperty()
    topic = db.ReferenceProperty(SignupTopic, collection_name = 'signed_up')
