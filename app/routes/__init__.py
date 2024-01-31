from app import app, db, mail, s, login_manager,mqtt
from flask import render_template, request, session, escape, redirect, url_for, flash, g, send_from_directory,jsonify,send_file,Response,stream_with_context,json
from flask_login import LoginManager,login_user,logout_user,login_required,current_user,UserMixin
from app.schemas.users import usuarios
from app.schemas.dispositivos import dispositivos
from app.schemas.Sensors import Sensors
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from flask_mail import Message
from itsdangerous import SignatureExpired
from pathlib import Path 

@login_manager.user_loader
def load_user(user_id):
    return usuarios.query.get(int(user_id))

@app.route('/',methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')

@app.route('/about',methods=['GET'])
def about():
   return render_template('about.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    
    if not current_user.is_authenticated:
        if request.method == 'POST':

            lon_nom =len(request.form.get('nombre'))
            lon_pass =len(request.form.get('clave')) 
            lon_email =len(request.form.get('email')) 
            if lon_nom != 0 and lon_email != 0 and lon_pass != 0:

                nombre_existente = usuarios.query.filter_by(nombre=request.form.get('nombre')).first()
                email_existente = usuarios.query.filter_by(email=request.form.get('email')).first()

                if nombre_existente:
                    flash('El nombre de usuario ya existe, intenta con otro', 'error')
                elif email_existente:
                    flash('El correo proporcionado ya existe, intenta con otro', 'error')
                elif request.form.get('clave') != request.form.get('confirClave'):
                    flash('La contraseña proporcionada no coincide','error')

                else:

                    codificar_clave = generate_password_hash(request.form.get('clave'), method = 'sha256')
                    nuevo_usuario = usuarios(nombre = request.form.get('nombre'), contraseña = codificar_clave, email= request.form.get('email')) 
                    db.session.add(nuevo_usuario)
                    db.session.commit()
                    # msg = Message('Gracias por registrarte!', sender= app.config['MAIL_USERNAME'], recipients=[request.form.get('email')])
                    # msg.html = render_template('email.html', user = request.form.get('nombre'))
                    # mail.send(msg)

                    flash(' Te has registrado exitosamente.','exito')

                    return redirect(url_for('iniciarsesion'))
            else:
                flash('No dejes espacios en blanco, todos los campos son abligatorios','error')
        
        return render_template('registro.html')
    return redirect(url_for('perfil'))


@app.route('/iniciarsesion',methods=['GET','POST'])
def iniciarsesion():
    if not current_user.is_authenticated:
        if request.method == 'POST':

            usuario = usuarios.query.filter_by(nombre = request.form.get('nombre')).first()

            if usuario and check_password_hash(usuario.contraseña, request.form.get('clave')):

                login_user(usuario, remember=request.form.get('recordar'))
            
                return redirect('/perfil')
            
            flash('La contraseña o el usuario no coinciden','error')

        return render_template('login.html')
    return redirect('/perfil')

@app.route('/perfil', methods=['GET','POST'])
@login_required
def perfil():
    user = current_user
    return render_template('perfil.html', user=user)

@app.route('/updateProfile', methods=['GET'])
@login_required
def updateProfile():
    user = current_user
   
    return render_template('updateProfile.html', user=user)

@app.route('/updateProfile', methods=['POST'])
@login_required
def changeProfile():
   
    usuario = usuarios.query.filter_by(id = request.form.get('id')).first()
    usuario.nombre = request.form.get('nombre')
    usuario.email = request.form.get('clave')
    db.session.commit()
    flash('Se han guardado los cambios con exito','exito')
    return redirect('/updateProfile')

@app.route('/salir')
@login_required
def salir():
    logout_user()
    return redirect('/')

@app.route('/acomulados',methods=['GET', 'POST'])
@login_required
def acomulados():

    wSensor = Sensors.query.order_by(Sensors.date.asc()).all()
    size = len(wSensor)
    if size >= 20:
        wSensor20 = wSensor[size-20:size]
    else:
        wSensor20 = wSensor
    name = 'Sensor de agua'
    color = 'rgb(57, 106, 177)'
    label = 'nivel de agua vs tiempo'

    if request.method == 'POST':
        stsend = request.form.get('sensorType')
        dateSend = request.form.get('date')
        timeSend = request.form.get('time')
        if stsend == '1':
            query = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            allsensor1 = sensor1.query.filter(sensor1.fecha.like(query)).all()
            wSensor20 = allsensor1
            name = 'Sensor de Agua'
            color = 'rgb(57, 106, 177)'
            label = 'Nivel de agua vs tiempo'
        elif stsend == '2':
            query = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            allsensor2 = sensor2.query.filter(sensor2.fecha.like(query)).all()
            wSensor20 = allsensor2
            name = 'Sensor de Temperatura'
            color = 'rgb(218, 124, 48)'
            label = 'Temperatura vs Tiempo'
        elif stsend == '3':
            query = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            allsensor3 = sensor3.query.filter(sensor3.fecha.like(query)).all()
            wSensor20 = allsensor3
            name = 'Sensor de Humedad'
            color = 'rgb(62, 150, 81)'
            label = 'Humedad vs Tiempo'
        elif stsend == '4':
            query = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            allsensor4 = sensor4.query.filter(sensor4.fecha.like(query)).all()
            wSensor20 = allsensor4
            name = 'Sensor Barometrico'
            color = 'rgb(204, 37, 41)'
            label = 'Presion atmosferica vs Tiempo'


    return render_template('acomulados.html',wSensor20 = wSensor20, name= name, color=color, label=label )

@app.route('/downloadData',methods=['GET', 'POST'])
@login_required
def downloadData():      
    return render_template('downloadData.html')



@app.route('/download',methods=['GET', 'POST'])
def download():
    data = []
    date = []
    if request.method == 'POST':
        dateSend = request.form.get('date')
        timeSend = request.form.get('time')
        stSend = request.form.get('sensorType')
        if stSend == '1':
            format = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            sensorQuery1 = sensor1.query.filter(sensor1.fecha.like(format)).all()
            if sensorQuery1 != []:
                for i in sensorQuery1:
                    data.append(i.dato)
                    date.append(i.fecha.strftime('%m/%d/%Y--%H:%M:%S'))
                dict = {'Nivel de Agua': data, 'fecha': date} 
                df = pd.DataFrame(dict) 
                filepath = Path('app/download/csv/datos.csv')  
                filepath.parent.mkdir(parents=True, exist_ok=True)  
                df.to_csv(filepath) 
                p = 'download/csv/datos.csv' 
                return send_file(p,as_attachment=True)
            else:
                flash('No hay datos para la fecha ingresada','error')
                return redirect('/downloadData')
        elif stSend == '2':
            format = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            sensorQuery2 = sensor2.query.filter(sensor2.fecha.like(format)).all()
            if sensorQuery2 != []:
                for i in sensorQuery2:
                    data.append(i.dato)
                    date.append(i.fecha.strftime('%m/%d/%Y--%H:%M:%S'))
                dict = {'Temperatura': data, 'fecha': date} 
                df = pd.DataFrame(dict)
                df.to_csv('datos.csv') 
                p = 'datos.csv' 
                return send_file(p,as_attachment=True)
            else:
                flash('No hay datos para la fecha ingresada','error')
                return redirect('/downloadData')
        elif stSend == '3':
            format = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            sensorQuery3 = sensor3.query.filter(sensor3.fecha.like(format)).all()
            if sensorQuery3 != []:
                for i in sensorQuery3:
                    data.append(i.dato)
                    date.append(i.fecha.strftime('%m/%d/%Y--%H:%M:%S'))
                dict = {'Humedad': data, 'fecha': date} 
                df = pd.DataFrame(dict) 
                df.to_csv('datos.csv') 
                p = 'datos.csv' 
                return send_file(p,as_attachment=True)
            else:
                flash('No hay datos para la fecha ingresada','error')
                return redirect('/downloadData')
        elif stSend == '4':
            format = "%{dateSend} {timeSend}%".format(dateSend = dateSend,timeSend = timeSend)
            sensorQuery4 = sensor4.query.filter(sensor4.fecha.like(format)).all()
            if sensorQuery4 != []:
                for i in sensorQuery4:
                    data.append(i.dato)
                    date.append(i.fecha.strftime('%m/%d/%Y--%H:%M:%S'))
                dict = {'Humedad': data, 'fecha': date} 
                df = pd.DataFrame(dict) 
                df.to_csv('datos.csv') 
                p = 'datos.csv' 
                return send_file(p,as_attachment=True)
            else:
                flash('No hay datos para la fecha ingresada','error')
                return redirect('/downloadData')

        else:
            flash('No se pueden descargar datos porque los campos estan vacios o el sensor no existe','error')
            return redirect('/downloadData')

@app.route('/changepassword',methods=['GET', 'POST'])
def changepassword():
    global gtoken
    if request.method == 'POST':
        email_existente = usuarios.query.filter_by(email=request.form.get('emailRec')).first()
        if email_existente != None:
            token= s.dumps(email_existente.email, salt='email-rec').decode('utf-8')
            msg = Message('Recuperar contraseña!', sender= app.config['MAIL_USERNAME'], recipients=[email_existente.email])
            format = "hola para recuperar la contraseña ingresa al siguiente enlace: http://127.0.0.1:5000/recoverpassword/{token}".format(token=token)
            msg.body = format
            mail.send(msg)
            flash('Se ha enviado un email de recuperacion al correo proporcionado','exito')
        else:
            flash('El correo proporcionado no se encuentra registrado','error')
    return render_template('changepassword.html')

@app.route('/recoverpassword/<token>')
def recoverpassword(token):
    try:
        email = s.loads(token, salt='email-rec')
        userQuery = usuarios.query.filter_by(email = email).first()
    
    except SignatureExpired:
        return render_template('expired.html')
    return render_template('resetpassword.html',userQuery=userQuery ,token = token)


@app.route('/newpassword',methods=['GET', 'POST'])
def newpassword():

    if request.method == 'POST':
        valueToken = request.form.get('valueToken')
        password=request.form.get('clave')
        passwordConf = request.form.get('confirClave')
        userId = request.form.get('user')
        if password == passwordConf:
            userQuery = usuarios.query.filter_by(id = userId).first()
            oldUser = userQuery
            db.session.delete(userQuery)
            db.session.commit()
            codificar_clave = generate_password_hash(password, method = 'sha256')
            newUser = usuarios(nombre = oldUser.nombre, contraseña = codificar_clave , email = oldUser.email )
            db.session.add(newUser)
            db.session.commit()
            flash('La contraseña se ha cambiado con exito','exito')
            return redirect('iniciarsesion')
        else:
            flash('La contraseña no coincide','error')
    rformat = 'recoverpassword/{token}'.format(token= valueToken)  
    print(rformat)
    return redirect(rformat)

def _dato():
    dato = Sensors.query.order_by(Sensors.date.desc()).first()
    # dict1 = {'dato':dato.dato,'dato2':dato2.dato, 'dato3':dato3.dato,'dato4':dato4.dato,'fecha':dato.fecha.strftime('%H:%M:%S')}
    if dato != None:
        dict = {'dato':dato.voltage,'fecha':dato.date.strftime('%H:%M:%S')}
    else: 
        dict = {'dato':'','fecha':''}
    
    # dict1 = {'dato':'32','fecha':'25/05/2022'}
    json_data = json.dumps(dict)
    yield f"data:{json_data}\n\n"

@app.route('/datos_monitoreo')
def datos_monitoreo():
    enviar = _dato()
    return Response(stream_with_context(enviar), mimetype='text/event-stream')


@app.route('/dispositivos',methods=['GET', 'POST'])
@login_required
def device():  

    deviceQuery = dispositivos.query.all()  

    return render_template('dispositivos.html',deviceQuery=deviceQuery)

@app.route('/agregardispositivo',methods=['GET'])
@login_required
def agregardispositivo():
   return render_template('agregardispositivo.html')

@app.route('/agregardispositivo',methods=['POST'])
def guardardispositivo():
    if request.method == 'POST':
        dispositivo = request.form.get('dispositivo')
        status = request.form.get('status')
        newDivice = dispositivos(nombre = dispositivo, status = status)
        db.session.add(newDivice)
        db.session.commit()
        flash('Ha agregado un nuevo dispositivo!','exito')

    return redirect('dispositivos')

@app.route('/devicestatus',methods=['POST'])
def devicestatus():
    if request.method == 'POST':
        id= request.form.get('id')
        query = dispositivos.query.filter_by(id = id).first() 
        if query.status:
            query.status = 0
            db.session.commit()
        else:
            query.status = 1
            db.session.commit()

        data = { 
                "deviceName":query.nombre,
                "id":query.id,
                "status":query.status
                }
        jsonFormat = json.dumps(data)
        mqtt.publish('notification',jsonFormat)
 
    mensaje = {'exito':'mensaje recibido'}
    return redirect('dispositivos')