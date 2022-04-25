from .utils import is_spotify_authenticated


def setup_spotify():
    user_token = "7f3a8cfe4d5e9d2a5e456224f3f1f8b187c72c44"
    print(is_spotify_authenticated(user_token))  # will refresh
    return user_token
