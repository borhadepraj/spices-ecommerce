from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages and session management

# Custom filter to calculate total amount
@app.template_filter('sum_total')
def sum_total(cart):
    return sum(item['total'] for item in cart)

# Make cart accessible to all templates
@app.context_processor
def inject_cart():
    return dict(cart=session.get('cart', []))

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Products route
@app.route('/products')
def products():
    return render_template('products.html')

# About route
@app.route('/about')
def about():
    return render_template('about.html')

# Contact route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        with open('messages.txt', 'a') as file:
            file.write(f"Name: {name}\nEmail: {email}\nMessage: {message}\n---\n")
        
        flash("Your message has been sent successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')

# Add to cart route - prevents duplicate entries
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product = request.form.get('product')
    price = float(request.form.get('price'))
    quantity = int(request.form.get('quantity'))

    cart = session.get('cart', [])
    
    # Check if product already exists in cart
    for item in cart:
        if item['product'] == product:
            item['quantity'] += quantity
            item['total'] = item['quantity'] * item['price']
            break
    else:
        cart.append({
            'product': product,
            'price': price,
            'quantity': quantity,
            'total': price * quantity
        })

    session['cart'] = cart
    flash(f"{product} added to cart!", "success")
    return redirect(url_for('products'))

# Cart page
@app.route('/cart')
def cart():
    return render_template('cart.html')

# Clear cart route (POST method)
@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    flash("Cart has been cleared!", "success")
    return redirect(url_for('cart'))

# Billing page
@app.route('/billing')
def billing():
    return render_template('billing.html')


if __name__ == '__main__':
    app.run(debug=True)
