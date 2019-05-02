import datetime
import uuid
from mongoengine import *

connect('mongoengine_test', host='localhost', port=27017)

        
class UserSession(Document):
    user_code = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    is_expired = BooleanField(default=False)

    def find_session(self,session_code):
        return UserSession.objects.get(id=session_code)

    def create_user_session(self,user_code):
        return UserSession(user_code=user_code).save()

    def destroy_user_session(self,session_code):
        user_session = UserSession.objects.get(id=session_code)
        user_session.update(is_expired=True)
