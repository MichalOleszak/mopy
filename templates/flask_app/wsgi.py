from templates.flask_app.start_model_server import app, setup_model

setup_model()

if __name__ == "__main__":
    app.run()
