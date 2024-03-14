from flask import render_template, redirect, url_for, flash, request
from market.model import Items, User
from market.form import RegisterForm, LoginForm, purchaseForm, sellForm
from market import db, app
from flask_login import login_user, login_manager, logout_user, login_required, current_user
import requests

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/market",methods=['GET', 'POST'])
@login_required
def market_page():
	purchase_form = purchaseForm()
	sell_form = sellForm()
	if request.method == "POST":
		purchased_item = request.form.get('purchase_item')
		p_item_obj = Items.query.filter_by(name= purchased_item).first()
		if p_item_obj:
			if current_user.can_buy(p_item_obj):
				p_item_obj.buy(current_user)
				flash(f"You have successfully purchased {p_item_obj.name} for {p_item_obj.price}", category='success')
				return redirect(url_for('market_page'))
			else:
				flash(f"Sorry You have insufficient fund to buy")
			sell_item = request.form.get('sell_item')
			s_item_obj= Items.query.filter_by(name= sell_item).first()
			if s_item_obj:
				if current_user.can_sell(current_user):
					s_item_obj.sell(current_user)
		return redirect(url_for('market_page'))

	if request.method == "GET":
		item_name= Items.query.filter_by()
		owned_items= Items.query.filter_by(owner= current_user.id)
		return render_template("market.html", item_name=item_name, purchase_form=purchase_form, owned_items=owned_items, sell_form=sell_form)

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash('Account created successfully! You can now log in.', category='success')
        return redirect(url_for('login_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error while creating the account: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
	form = LoginForm()
	if form.validate_on_submit():
		attempted_user= User.query.filter_by(username=form.username.data).first()
		if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
			login_user(attempted_user)
			flash(f"Welcome {attempted_user.username}. You have successfully logged in...", category="success"),403
			return redirect(url_for('market_page'))
		else:
			flash("Invalid User Credentials", category="danger")
	return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
	logout_user()
	flash("Now You have successfully Logged Out", category="info")
	return redirect(url_for('home_page'))
 







































