from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cle_secrete_definitive'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wifi_support.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='ouvert')
    priority = db.Column(db.String(10), default='moyenne')
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    client = db.relationship('User', foreign_keys=[client_id], backref='client_tickets')
    agent = db.relationship('User', foreign_keys=[agent_id], backref='agent_tickets')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender_type = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', foreign_keys=[sender_id])
    ticket = db.relationship('Ticket', backref='messages')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    user_type = SelectField('Type d\'utilisateur', choices=[('client', 'Client'), ('agent', 'Agent')], validators=[DataRequired()])
    submit = SubmitField('S\'inscrire')

class TicketForm(FlaskForm):
    title = StringField('Titre du problème', validators=[DataRequired()])
    description = TextAreaField('Description détaillée', validators=[DataRequired()])
    priority = SelectField('Priorité', choices=[('basse', 'Basse'), ('moyenne', 'Moyenne'), ('haute', 'Haute')], validators=[DataRequired()])
    submit = SubmitField('Signaler la panne')

class MessageForm(FlaskForm):
    content = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Envoyer')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Nom d\'utilisateur ou mot de passe incorrect')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Ce nom d\'utilisateur existe déjà')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Cet email est déjà utilisé')
            return render_template('register.html', form=form)
        
        user = User(username=form.username.data, email=form.email.data, user_type=form.user_type.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Inscription réussie! Vous pouvez maintenant vous connecter.')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        if current_user.user_type == 'client':
            tickets = Ticket.query.filter_by(client_id=current_user.id).order_by(Ticket.created_at.desc()).all()
            return render_template('client_dashboard.html', tickets=tickets)
        else:
            tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
            return render_template('agent_dashboard.html', tickets=tickets)
    except Exception as e:
        flash(f'Erreur lors du chargement du tableau de bord: {str(e)}')
        return redirect(url_for('index'))

@app.route('/create_ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if current_user.user_type != 'client':
        flash('Seuls les clients peuvent créer des tickets')
        return redirect(url_for('dashboard'))
    
    form = TicketForm()
    if form.validate_on_submit():
        try:
            ticket = Ticket(
                title=form.title.data,
                description=form.description.data,
                priority=form.priority.data,
                client_id=current_user.id
            )
            db.session.add(ticket)
            db.session.commit()
            
            flash('Ticket créé avec succès!')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Erreur lors de la création du ticket: {str(e)}')
            db.session.rollback()
    
    return render_template('create_ticket.html', form=form)

@app.route('/ticket/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        
        if current_user.user_type == 'client' and ticket.client_id != current_user.id:
            flash('Accès non autorisé')
            return redirect(url_for('dashboard'))
        
        messages = Message.query.filter_by(ticket_id=ticket_id).order_by(Message.created_at.asc()).all()
        form = MessageForm()
        
        return render_template('view_ticket.html', ticket=ticket, messages=messages, form=form)
    except Exception as e:
        flash(f'Erreur lors du chargement du ticket: {str(e)}')
        return redirect(url_for('dashboard'))

@app.route('/ticket/<int:ticket_id>/add_message', methods=['POST'])
@login_required
def add_message(ticket_id):
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        
        if current_user.user_type == 'client' and ticket.client_id != current_user.id:
            flash('Accès non autorisé')
            return redirect(url_for('view_ticket', ticket_id=ticket_id))
        
        form = MessageForm()
        if form.validate_on_submit():
            message = Message(
                content=form.content.data,
                ticket_id=ticket_id,
                sender_id=current_user.id,
                sender_type=current_user.user_type
            )
            db.session.add(message)
            
            if ticket.status == 'ouvert' and current_user.user_type == 'agent':
                ticket.status = 'en_cours'
                ticket.agent_id = current_user.id
            
            ticket.updated_at = datetime.utcnow()
            db.session.commit()
            
            flash('Message envoyé!')
        
        return redirect(url_for('view_ticket', ticket_id=ticket_id))
    except Exception as e:
        flash(f'Erreur lors de l\'envoi du message: {str(e)}')
        db.session.rollback()
        return redirect(url_for('view_ticket', ticket_id=ticket_id))

@app.route('/ticket/<int:ticket_id>/update_status', methods=['POST'])
@login_required
def update_ticket_status(ticket_id):
    try:
        if current_user.user_type != 'agent':
            flash('Accès non autorisé')
            return redirect(url_for('view_ticket', ticket_id=ticket_id))
        
        ticket = Ticket.query.get_or_404(ticket_id)
        new_status = request.form.get('status')
        
        if new_status in ['ouvert', 'en_cours', 'resolu', 'ferme']:
            ticket.status = new_status
            if new_status == 'en_cours' and not ticket.agent_id:
                ticket.agent_id = current_user.id
            ticket.updated_at = datetime.utcnow()
            db.session.commit()
            
            flash('Statut mis à jour!')
        
        return redirect(url_for('view_ticket', ticket_id=ticket_id))
    except Exception as e:
        flash(f'Erreur lors de la mise à jour du statut: {str(e)}')
        db.session.rollback()
        return redirect(url_for('view_ticket', ticket_id=ticket_id))

@app.errorhandler(404)
def not_found_error(error):
    flash('Page non trouvée')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    flash('Une erreur interne est survenue')
    return redirect(url_for('index'))

@app.errorhandler(Exception)
def handle_exception(e):
    db.session.rollback()
    flash(f'Une erreur est survenue: {str(e)}')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=False)
