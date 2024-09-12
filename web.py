from app import connexion_app, flask_app, db, setup_interfaces
import uvicorn

if __name__ == '__main__':
    setup_interfaces(connexion_flask_app=connexion_app)
    with flask_app.app_context():
        db.create_all()

    uvicorn.run('app:connexion_app', host='0.0.0.0', port=5000, reload=True)

