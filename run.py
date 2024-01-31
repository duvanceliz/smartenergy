from app import app, db, mail, mqtt, login_manager
mqtt.init_app(app)
db.create_all() 
if __name__=='__main__':
    app.run()
    mail.init_app(app)
    db.create_all() 
    login_manager.init_app(app)
    
   
    

