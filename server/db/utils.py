from models.UserModels import User, UserSong
from db.dbConnect import Session_Local

db = Session_Local()

def create_new_user(spotify_id, spotify_display_name, spotify_refresh_token):
    new_user = User(spotify_id=spotify_id, spotify_display_name=spotify_display_name, spotify_refresh_token=spotify_refresh_token)
    db.add(new_user)
    db.commit()
    
def query_user(spotify_id):
    user = db.query(User).filter_by(spotify_id=spotify_id).first()
    return user

def user_exists(spotify_id):
    user = db.query(User).filter_by(spotify_id=spotify_id).first()
    if user != None:
        return True
    return False

def query_user_refresh_token(spotify_id):
    id = db.query(User).filter_by(spotify_id=spotify_id).first().spotify_id
    return id


