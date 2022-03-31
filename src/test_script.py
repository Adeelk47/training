from flask import Flask

from init import initialize_app
from scripts import tenant_creation

app = Flask(__name__, static_folder="../static")
app.app_context().push()
initialize_app()

tenant_creation.create_tenant("tkxel")
