from functools import wraps
from flask import abort
from flask_login import current_user
from .models import  User, Follow, Role, Permission, Post, Comment,Entry,CommentLike,PostLike



# Custom decorators that check user permissions
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Custom decorators that check Admin permissions
def admin_required(f):
    return permission_required(Permission.ADMIN)(f)