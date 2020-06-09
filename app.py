import os
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy.orm.session import sessionmaker
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy import and_
from sqlalchemy.orm import scoped_session, sessionmaker
from dominate.tags import option
from werkzeug.exceptions import BadRequest
import requests
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import *
from datetime import datetime, date, time, timezone
from flask_mail import Mail, Message



app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tfodhbftaktvtw:bd653d6a2a4a61edd889e915a99f19a3a1e8f4bc3105ceede15fe7a19dec9856@ec2-3-222-150-253.compute-1.amazonaws.com:5432/dkeq04ivd5eie'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#-------mail configuration----------------#
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
#app.config['MAIL_DEBUG'] = 
app.config['MAIL_USERNAME'] = 'rb@cbngroup.com.ar'
app.config['MAIL_PASSWORD'] = 'fplloqvxloaskgdd'
app.config['MAIL_DEFAULT_SENDER'] = 'rb@cbngroup.com.ar'
app.config['MAIL_MAX_EMAILS'] = None
#app.config['MAIL_SUPPRESS_SEND '] = 
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/')
def index():
    return render_template('index.html')


#--------------------------------LOG IN USUARIO--------------------------------------#

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Member.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

#------------------------GENERAR USUARIO------------------------------------#

@app.route('/ONcugKNIWAWfdXpGvMBfNQIGOVV829WWKgj1vVrnDlpQ9MdDXdcgliYjP13NlpGy', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Member(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)


#------------------------PANEL GENERAL / DASHBOARD ---------------------------#

@app.route('/dashboard')
@login_required
def dashboard():
    
    responsible=Member.query.filter_by(username=current_user.username).first()
    petitioner=Member.query.filter_by(username=current_user.username).first()
    totTicketsCount=Tickets.query.count()
    totTicketsCountOpen=Tickets.query.filter(Tickets.status=="abierta").count()
    totTicketsCountClosed=Tickets.query.filter(Tickets.status=="cerrada").count()
    totTicketsCountCourse=Tickets.query.filter(Tickets.status=="en curso").count()
    totTicketsCountPausada=Tickets.query.filter(Tickets.status=="pausada").count()
    totTicketsCountmedia=Tickets.query.filter(Tickets.priority=="media").count()
    totTicketsCountbaja=Tickets.query.filter(Tickets.priority=="baja").count()
    totTicketsCountalta=Tickets.query.filter(Tickets.priority=="alta").count()
    
    
    
    return render_template('dashboard.html',totTicketsCountmedia=totTicketsCountmedia, totTicketsCountbaja=totTicketsCountbaja, totTicketsCountalta=totTicketsCountalta, name=current_user.username, totTicketsCount=totTicketsCount, totTicketsCountOpen=totTicketsCountOpen, totTicketsCountClosed=totTicketsCountClosed, totTicketsCountCourse=totTicketsCountCourse, totTicketsCountPausada=totTicketsCountPausada )



#------------------------------LOG OUT--------------------------------------------#
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#-----------------------------------BUSCADOR OS------------------------------------#
@app.route('/buscar_os')
@login_required
def ticket_search():
    ticket = db.session.query(Tickets.id, Tickets.date_start, Tickets.description, Tickets.priority, Tickets.status, Sites.name.label('siteName')).filter(Tickets.site_id==Sites.id).order_by(Tickets.date_start.desc()).all()
    ticketCount = db.session.query(Tickets.id, Tickets.date_start, Tickets.description, Tickets.priority, Tickets.status, Sites.name.label('siteName')).filter(Tickets.site_id==Sites.id).count()

    return render_template('ticket_search.html',name=current_user.username, ticket=ticket, ticketCount=ticketCount)

#-----------------------------------EQUIPOS-----------------------------------------#
@app.route('/equipos')
@login_required
def assets():
    assets = db.session.query(Assets.id, Assets.name, Sites.name.label('siteName')).filter(Assets.site_id==Sites.id).order_by(Sites.name.label('siteName').desc()).all()
    assetsCount = db.session.query(Assets.id, Assets.name, Sites.name.label('siteName')).filter(Assets.site_id==Sites.id).count()


    return render_template('equipos.html', name=current_user.username, assets=assets, assetsCount=assetsCount)

#-----------------------------------Detalle Equipos-----------------------------------------#
@app.route('/equipos/<equipo_id>', methods=['GET'])
@login_required
def asset_detail(equipo_id):
    equipo=Assets.query.filter_by(id=equipo_id).first()
    ticketAsset = db.session.query(Tickets.id, Tickets.date_start, Tickets.description, Tickets.priority, Tickets.status, Sites.name.label('siteName')).filter(and_(Tickets.site_id==Sites.id, Tickets.asset_id==equipo_id)).order_by(Tickets.date_start.desc()).all()
    ticketAssetCount = db.session.query(Tickets.id, Tickets.date_start, Tickets.description, Tickets.priority, Tickets.status, Sites.name.label('siteName')).filter(Tickets.asset_id==equipo_id).count()


    return render_template('detalle_equipos.html',name=current_user.username, equipo=equipo, equipo_id=equipo_id, ticketAsset=ticketAsset, ticketAssetCount=ticketAssetCount)


#----------------------------------GENERADOR DE OS----------------------------------#

@app.route('/generar_os', methods=["GET","POST"])
@login_required
def generar_os():
    sites=Sites.query.all()
    area=Area.query.all()
    asset=Assets.query.all()
    failure=Failure.query.all()
    member=Member.query.all()
    vendor=Vendors.query.all()

    if request.method == 'POST':

        description = request.form.get("description")
        petitioner = Member.query.filter_by(username=current_user.username).first()
        responsible = Member.query.filter_by(username=request.form.get("responsible")).first()
        site = Sites.query.filter_by(name=request.form.get("site")).first()
        area = Area.query.filter_by(name=request.form.get("area")).first()
        asset = Assets.query.filter_by(name=request.form.get("asset")).first()
        date_start = request.form.get('fechaInicio')
        priority = request.form.get("priority")
        failure = Failure.query.filter_by(name=request.form.get("failure")).first()
        vendor = Vendors.query.filter_by(name=request.form.get("vendor")).first()
        
        petitioner_id = int(petitioner.id)
        responsible_id = int(responsible.id)
        site_id = int(site.id) 
        area_id = int(area.id)
        asset_id = int(asset.id)
        failure_id = int(failure.id)
        vendor_id = int(vendor.id)
        email=responsible.email
        

        ticket = Tickets(description=description, petitioner_id=petitioner_id, responsible_id=responsible_id, site_id=site_id, area_id=area_id, asset_id=asset_id, date_start=date_start, priority=priority, failure_id=failure_id, status="abierta", vendor_id=vendor_id)
        db.session.add(ticket)
        db.session.commit()

        #------email sending-----------#

        msg = Message("Orden de servicio asignada", sender='rb@cbngroup.com.ar', recipients=[email])

        msg.html = '<p>Se le ha asignado una nueva orden de servicio. Para verla ingresa a la aplicacion.</p>'
        mail.send(msg)
        
        return redirect(url_for('os_generada', ticket_id=ticket.id))    
    return render_template('ticket_generator.html', name=current_user.username, sites=sites, area=area, asset=asset, failure=failure, member=member, vendor=vendor)

#---------------------OS GENERADAS----------------------------------------#

@app.route('/os_generada/<ticket_id>', methods=['GET'])
@login_required
def os_generada(ticket_id):
    ticketId=int(ticket_id)
    ticket = Tickets.query.filter_by(id=ticketId).first()
    return render_template('os_created.html', ticket=ticket, name=current_user.username)

#------------------OS ASIGNADAS-------------------------------------#

@app.route('/os_asignada/<ticket_id>', methods=['GET','POST'])
@login_required
def os_asignada(ticket_id):
    ticketId=ticket_id
    ticket = Tickets.query.filter_by(id=ticketId).first()
    currentUser = Member.query.filter_by(username=current_user.username).first()
    if ticket.responsible_id==currentUser.id:
     petitioner = Member.query.filter_by(id=ticket.petitioner_id).first()
     responsible = Member.query.filter_by(id=ticket.responsible_id).first()
     sites = Sites.query.filter_by(id=ticket.site_id).first()
     area = Area.query.filter_by(id=ticket.area_id).first()
     asset = Assets.query.filter_by(id=ticket.asset_id).first()
     date_start = ticket.date_start
     priority =ticket.priority
     failure = Failure.query.filter_by(id=ticket.failure_id).first()
     vendor = Vendors.query.filter_by(id=ticket.vendor_id).first()
    else:
        return "no puede editar esta OS"
    
    ticketNotes=db.session.query(Tickets_notes).filter_by(ticket_id=ticket_id).first()
    ticketNotesCount=db.session.query(Tickets_notes).filter_by(ticket_id=ticket_id).count()


    if request.method == 'POST':
        ticket=db.session.query(Tickets).filter_by(id=ticket_id).first()        
        if request.form.get("fechaFin") !="":
            ticket.date_end = request.form.get("fechaFin")
            db.session.commit()

        if request.form.get("status") !=None:
            ticket.status = request.form.get("status")
            db.session.commit()
            
        if request.form.get("ticketNote")!="":
            ticketNotes = Tickets_notes(description=request.form.get("ticketNote"), ticket_id=ticket_id, user_id=currentUser.id, date=date.today())
            db.session.add(ticketNotes)
            db.session.commit()

 
        return render_template('message.html', message="OS modificada")


    ticket_notes = db.session.query(Tickets_notes.description, Tickets_notes.date, Member.username).filter(and_(Tickets_notes.user_id==Member.id, Tickets_notes.ticket_id==ticket_id)).order_by(Tickets_notes.date.desc()).all()





    return render_template('os_asignada.html',ticket_notes=ticket_notes, ticket=ticket, name=current_user.username, petitioner=petitioner, responsible=responsible, sites=sites, area=area, asset=asset, failure=failure, vendor=vendor, date_start=date_start, priority=priority)



#------------------OS REQUERIDAS-------------------------------------#

@app.route('/os_requerida/<ticket_id>', methods=['GET' ,'POST'])
@login_required
def os_requerida(ticket_id):
    currentUser = Member.query.filter_by(username=current_user.username).first()
    sitesAll=Sites.query.all()
    areaAll=Area.query.all()
    assetAll=Assets.query.all()
    failureAll=Failure.query.all()
    memberAll=Member.query.all()
    vendorAll=Vendors.query.all()  
    ticketId=ticket_id
    ticket = Tickets.query.filter_by(id=ticketId).first()
    ticketCount=Tickets.query.filter_by(id=ticketId).count()
    if ticketCount==0:
        return "No existe una OS con ese número"
    else:
     currentUser = Member.query.filter_by(username=current_user.username).first()
     if ticket.petitioner_id==currentUser.id:
      petitioner = Member.query.filter_by(id=ticket.petitioner_id).first()
      responsible = Member.query.filter_by(id=ticket.responsible_id).first()
      sites = Sites.query.filter_by(id=ticket.site_id).first()
      area = Area.query.filter_by(id=ticket.area_id).first()
      asset = Assets.query.filter_by(id=ticket.asset_id).first()
      date_start = ticket.date_start
      priority =ticket.priority
      failure = Failure.query.filter_by(id=ticket.failure_id).first()
      vendor = Vendors.query.filter_by(id=ticket.vendor_id).first()
     else:
         return "no puede editar esta OS"
    

    if request.method == 'POST':
        descriptionReq = request.form.get("description")
        responsibleReq = Member.query.filter_by(username=request.form.get("responsible")).first()
        siteReq = Sites.query.filter_by(name=request.form.get("site")).first()
        areaReq = Area.query.filter_by(name=request.form.get("area")).first()
        assetReq = Assets.query.filter_by(name=request.form.get("asset")).first()
        date_startReq = request.form.get('dateStart')
        priorityReq = request.form.get("priority")
        failureReq = Failure.query.filter_by(name=request.form.get("failure")).first()
        vendorReq = Vendors.query.filter_by(name=request.form.get("vendor")).first()
        statusReq = request.form.get("status")
        date_endReq = request.form.get("dateEnd")
        ticket=db.session.query(Tickets).filter_by(id=ticket_id).first()

        if descriptionReq != "":
            ticket.description = request.form.get("description")
            db.session.commit()
        if responsibleReq != None:
            responsible_id = int(responsibleReq.id)
            ticket.responsible_id = responsible_id
            db.session.commit()
        if siteReq != None:
            site_id = int(siteReq.id) 
            ticket.site_id = site_id
            db.session.commit()
        if areaReq != None:
            area_id = int(areaReq.id) 
            ticket.area_id = area_id
            db.session.commit()
        if assetReq != None:
            asset_id = int(areaReq.id)
            ticket.asset_id = asset_id
            db.session.commit()
        if date_startReq != "":
            ticket.date_start = date_startReq
            db.session.commit()
        if priorityReq != None:
            ticket.priority = priorityReq
            db.session.commit()
        if failureReq != None:
            failure_id = int(failureReq.id)
            ticket.failure_id = failure_id
            db.session.commit()
        if vendorReq != None:
            vendor_id = int(vendorReq.id)
            ticket.vendor_id = vendor_id
            db.session.commit()
        if statusReq != None:
            ticket.status = statusReq
            db.session.commit()
        if date_endReq != "":
            ticket.date_end = date_endReq
            db.session.commit()
        if request.form.get('ticketNoteReq') != "":
            ticketNotes = Tickets_notes(description=request.form.get("ticketNoteReq"), ticket_id=ticket_id, user_id=currentUser.id, date=date.today())
            db.session.add(ticketNotes)
            db.session.commit()
        return render_template('message.html', message="OS modificada")



    ticket_notes = db.session.query(Tickets_notes.description, Tickets_notes.date, Member.username).filter(and_(Tickets_notes.user_id==Member.id, Tickets_notes.ticket_id==ticket_id)).order_by(Tickets_notes.date.desc()).all()


    return render_template('os_requerida.html', ticket_notes=ticket_notes, ticket=ticket, name=current_user.username, petitioner=petitioner, responsible=responsible, sites=sites, area=area, asset=asset, failure=failure, vendor=vendor, date_start=date_start, priority=priority, memberAll=memberAll, sitesAll=sitesAll, assetAll=assetAll, areaAll=areaAll, failureAll=failureAll, vendorAll=vendorAll)


#------------------OS DETALLE-------------------------------------#

@app.route('/os_detalle/<ticket_id>', methods=['GET'])
@login_required
def os_detalle(ticket_id):
    ticketId=ticket_id
    ticket = Tickets.query.filter_by(id=ticketId).first()
    ticketCount=Tickets.query.filter_by(id=ticketId).count()
    currentUser = Member.query.filter_by(username=current_user.username).first()
    if ticketCount==0:
        return "No existe una OS con ese número"
    petitioner = Member.query.filter_by(id=ticket.petitioner_id).first()
    responsible = Member.query.filter_by(id=ticket.responsible_id).first()
    sites = Sites.query.filter_by(id=ticket.site_id).first()
    area = Area.query.filter_by(id=ticket.area_id).first()
    asset = Assets.query.filter_by(id=ticket.asset_id).first()
    date_start = ticket.date_start
    priority =ticket.priority
    failure = Failure.query.filter_by(id=ticket.failure_id).first()
    vendor = Vendors.query.filter_by(id=ticket.vendor_id).first()
 
   
    if ticket.date_end==None:
        ticket.date_end=None
    else:
        ticket.date_end=ticket.date_end.strftime('%d-%m-%Y')
    


    ticket_notes = db.session.query(Tickets_notes.description, Tickets_notes.date, Member.username).filter(and_(Tickets_notes.user_id==Member.id, Tickets_notes.ticket_id==ticket_id)).order_by(Tickets_notes.date.desc()).all()


    return render_template('os_detalle.html', ticket_notes=ticket_notes, ticket=ticket, name=current_user.username, petitioner=petitioner, responsible=responsible, sites=sites, area=area, asset=asset, failure=failure, vendor=vendor, date_start=date_start, priority=priority)


#------------------------LISTA DE ORDENES ASIGNADAS-REQUERIDAS ---------------------------#

@app.route('/orders_list')
@login_required
def orders_list():
    responsible=Member.query.filter_by(username=current_user.username).first()
    petitioner=Member.query.filter_by(username=current_user.username).first()
    totTicketsCount=Tickets.query.filter(and_(Tickets.responsible_id==responsible.id, Tickets.status!="cerrada")).count()
    totTicketsCount2=Tickets.query.filter(and_(Tickets.petitioner_id==petitioner.id, Tickets.status!="cerrada")).count()

    if totTicketsCount==0:
        totTicketsCount="0"
    
    if totTicketsCount2==0:
        totTicketsCount2="0"
    
    ticket= db.session.query(Tickets.id, Tickets.date_start, Tickets.description, Member.username, Tickets.priority, Tickets.status, Sites.name.label('siteName')).filter(and_(Tickets.responsible_id==Member.id, Tickets.responsible_id==responsible.id, Tickets.site_id==Sites.id, Tickets.status!="cerrada")).order_by(Tickets.date_start.desc()).all()
    ticketreq = db.session.query(Tickets.id, Tickets.date_start, Tickets.description, Member.username, Tickets.priority, Tickets.status, Sites.name.label('siteName')).filter(and_(Tickets.responsible_id==Member.id, Tickets.petitioner_id==petitioner.id, Tickets.site_id==Sites.id)).order_by(Tickets.date_start.desc()).all()
    
    return render_template('orders_List.html', name=current_user.username, ticket=ticket, totTicketsCount2=totTicketsCount2, totTicketsCount=totTicketsCount, ticketreq=ticketreq)













if __name__ == '__main__':
    TEMPLATES_AUTO_RELOAD = True
    app.run(debug=True)

