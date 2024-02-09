from flask import Blueprint

main = Blueprint('main', __name__)
from ..models import Permission

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


from . import views, errors
#modules are imported at the bottom of the app/main/__init__.py script to avoid errors due to circular dependencies.