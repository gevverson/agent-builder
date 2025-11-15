from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # This creates the database file (app.db) if it doesn't exist
        db.create_all() 
    app.run(debug=True, port=5000)