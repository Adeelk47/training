from flask import Flask

from init import initialize_app

app = Flask(__name__, static_folder="../static")
app.app_context().push()
initialize_app()
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
