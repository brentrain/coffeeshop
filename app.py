from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer, default=0)
    orders = db.relationship('Order', backref='user', lazy=True)

# Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items = db.Column(db.String(500), nullable=False)
    total = db.Column(db.Float, nullable=False)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Drink {self.name}>'

# Sample drinks data
drinks = [
    # Hot Coffee
    {'id': 1, 'name': 'Espresso', 'category': 'hot_coffee', 'base_price': 2.99, 'description': 'A rich, bold espresso shot'},
    {'id': 2, 'name': 'Americano', 'category': 'hot_coffee', 'base_price': 3.49, 'description': 'Espresso with hot water'},
    {'id': 3, 'name': 'Cappuccino', 'category': 'hot_coffee', 'base_price': 3.99, 'description': 'Espresso with steamed milk and foam'},
    {'id': 4, 'name': 'Latte', 'category': 'hot_coffee', 'base_price': 4.49, 'description': 'Espresso with steamed milk'},
    
    # Cold Coffee
    {'id': 5, 'name': 'Iced Coffee', 'category': 'cold_coffee', 'base_price': 3.99, 'description': 'Chilled coffee served over ice'},
    {'id': 6, 'name': 'Cold Brew', 'category': 'cold_coffee', 'base_price': 4.49, 'description': 'Slow-steeped cold coffee'},
    {'id': 7, 'name': 'Iced Latte', 'category': 'cold_coffee', 'base_price': 4.99, 'description': 'Espresso with cold milk over ice'},
    {'id': 8, 'name': 'Frappuccino', 'category': 'cold_coffee', 'base_price': 5.49, 'description': 'Blended coffee drink with ice'},
    
    # Black Tea
    {'id': 9, 'name': 'English Breakfast', 'category': 'black_tea', 'base_price': 2.99, 'description': 'Classic black tea blend'},
    {'id': 10, 'name': 'Earl Grey', 'category': 'black_tea', 'base_price': 2.99, 'description': 'Black tea with bergamot'},
    {'id': 11, 'name': 'Darjeeling', 'category': 'black_tea', 'base_price': 3.49, 'description': 'Premium Indian black tea'},
    {'id': 12, 'name': 'Sweetened Iced Tea', 'category': 'black_tea', 'base_price': 3.49, 'description': 'Refreshing iced tea with sugar'},
    {'id': 13, 'name': 'Unsweetened Iced Tea', 'category': 'black_tea', 'base_price': 2.99, 'description': 'Refreshing iced tea without sugar'},
    
    # Green Tea
    {'id': 14, 'name': 'Sencha', 'category': 'green_tea', 'base_price': 3.49, 'description': 'Japanese green tea'},
    {'id': 15, 'name': 'Jasmine', 'category': 'green_tea', 'base_price': 3.49, 'description': 'Green tea with jasmine flowers'},
    {'id': 16, 'name': 'Matcha Latte', 'category': 'green_tea', 'base_price': 4.99, 'description': 'Green tea powder with milk'},
    
    # White Tea
    {'id': 17, 'name': 'Silver Needle', 'category': 'white_tea', 'base_price': 3.99, 'description': 'Premium white tea'},
    {'id': 18, 'name': 'White Peony', 'category': 'white_tea', 'base_price': 3.49, 'description': 'Classic white tea'},
    
    # Matcha
    {'id': 19, 'name': 'Traditional Matcha', 'category': 'matcha', 'base_price': 4.49, 'description': 'Pure matcha green tea'},
    {'id': 20, 'name': 'Matcha Latte', 'category': 'matcha', 'base_price': 4.99, 'description': 'Matcha with steamed milk'},
    {'id': 21, 'name': 'Iced Matcha', 'category': 'matcha', 'base_price': 4.99, 'description': 'Matcha with cold milk over ice'}
]

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_test_user():
    with app.app_context():
        # Check if test user already exists
        test_user = User.query.filter_by(email='coffee@coffee.com').first()
        if not test_user:
            # Create test user
            test_user = User(
                username='coffee_lover',
                email='coffee@coffee.com',
                password=generate_password_hash('hotcoffee'),
                points=100
            )
            db.session.add(test_user)
            db.session.commit()
            print("Test user created successfully!")
        return test_user

@app.route('/')
def index():
    # Automatically log in the test user
    test_user = create_test_user()
    login_user(test_user)
    return render_template('index.html', user=test_user, current_date=datetime.now().strftime('%B %d, %Y'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect to index page
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Redirect to index page
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/customize_drink/<int:drink_id>')
@login_required
def customize_drink(drink_id):
    # Find the drink in our drinks data
    drink = next((d for d in drinks if d['id'] == drink_id), None)
    if not drink:
        flash('Drink not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('customize_drink.html', drink=drink)

@app.route('/add_to_cart/<int:drink_id>', methods=['POST'])
@login_required
def add_to_cart(drink_id):
    # Get the drink
    drink = next((d for d in drinks if d['id'] == drink_id), None)
    if not drink:
        flash('Drink not found', 'error')
        return redirect(url_for('index'))
    
    # Get customization options from form
    size = request.form.get('size')
    milk = request.form.get('milk')
    sugar = request.form.get('sugar', 0)
    extras = {
        'whipped_cream': request.form.get('whipped_cream') == 'on',
        'caramel_drizzle': request.form.get('caramel_drizzle') == 'on',
        'chocolate_syrup': request.form.get('chocolate_syrup') == 'on'
    }
    tea_strength = request.form.get('tea_strength')
    sweetener = request.form.get('sweetener')
    matcha_grade = request.form.get('matcha_grade')
    sweetness = request.form.get('sweetness')
    instructions = request.form.get('instructions')
    lemon = request.form.get('lemon') == 'on'
    flavor = request.form.get('flavor', 'none')
    
    # Calculate total price
    total_price = drink['base_price']
    
    # Add size upcharge
    if size == 'medium':
        total_price += 0.5
    elif size == 'large':
        total_price += 1.0
    
    # Add milk upcharge
    if milk in ['almond', 'soy', 'oat']:
        total_price += 0.5
    
    # Add extras upcharge
    if extras['whipped_cream'] or extras['caramel_drizzle'] or extras['chocolate_syrup']:
        total_price += 0.5
    
    # Add honey upcharge
    if sweetener == 'honey':
        total_price += 0.5
    
    # Add premium matcha upcharge
    if matcha_grade == 'premium':
        total_price += 1.0
    
    # Add flavor upcharge
    if flavor != 'none':
        total_price += 0.5
    
    # Create order item
    order_item = {
        'drink_id': drink_id,
        'name': drink['name'],
        'size': size,
        'milk': milk,
        'sugar': sugar,
        'extras': extras,
        'tea_strength': tea_strength,
        'sweetener': sweetener,
        'matcha_grade': matcha_grade,
        'sweetness': sweetness,
        'lemon': lemon,
        'flavor': flavor,
        'instructions': instructions,
        'price': total_price
    }
    
    # Add to session cart
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(order_item)
    session.modified = True
    
    flash(f'{drink["name"]} added to cart!', 'success')
    return redirect(url_for('index'))

@app.route('/cart')
@login_required
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/remove_from_cart/<int:index>', methods=['POST'])
@login_required
def remove_from_cart(index):
    cart = session.get('cart', [])
    if 0 <= index < len(cart):
        removed_item = cart.pop(index)
        session['cart'] = cart
        session.modified = True
        flash(f'{removed_item["name"]} removed from cart', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout')
@login_required
def checkout():
    cart_items = session.get('cart', [])
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('cart'))
    
    total = sum(item['price'] for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/process_checkout', methods=['POST'])
@login_required
def process_checkout():
    cart_items = session.get('cart', [])
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('cart'))
    
    total = sum(item['price'] for item in cart_items)
    
    # Create a new order
    order = Order(
        user_id=current_user.id,
        items=str(cart_items),
        total=total
    )
    db.session.add(order)
    db.session.commit()
    
    # Clear the cart
    session['cart'] = []
    session.modified = True
    
    # Update user points (1 point per dollar spent)
    current_user.points += int(total)
    db.session.commit()
    
    flash(f'Order placed successfully! You earned {int(total)} points!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_test_user()
    app.run(debug=True) 