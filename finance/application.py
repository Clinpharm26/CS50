import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # look up the current user
    users = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])
    quotes = {}

    for stock in stocks:
        quotes[stock["symbol"]] = lookup(stock["symbol"])


    cash_remaining = users[0]["cash"]
    total = cash_remaining

    return render_template("portfolio.html", quotes=quotes, stocks=stocks, total=total, cash_remaining=cash_remaining)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        # Check if the symbol exists
        if quote == None:
             return apology("invalid symbol", 400)

        # Check if shares was a positive integer
        try:
          shares = int(request.form.get("shares"))
        except:
          return apology("shares cannot be negative", 400)

        # Check if # of shares requested was 0
        if shares <= 0:
            return apology("cannot buy 0 or less than 0 shares", 400)

        # Query database for username
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # How much $$$ the user still has in her account
        cash_remaining = rows[0]["cash"]
        price_per_share = quote["price"]

        # Calculate the price of requested shares
        price = price_per_share * shares

        if price > cash_remaining:
             return apology("not enough funds")

        # Book keeping (TODO: should be wrapped with a transaction)
        db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id", price=price, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, time) VALUES(:user_id, :symbol, :shares, :price, datetime('now', 'utc'))",
                   user_id=session["user_id"],
                   symbol=request.form.get("symbol"),
                   shares=shares,
                   price=price)

        flash("Bought!")

        return redirect("/")

    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT symbol, shares, price, time FROM transactions WHERE user_id = :user_id ORDER BY time ASC", user_id=session["user_id"])

    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", quote=quote)

    # User reached route via GET (as by clicking a link or via redi)
    else:
      return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username!", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Ensure passwords are matching
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("Sorry, passwords did not match. Try Again!", 400)

        # Hash password / Store password hash_password =
        hashed_password = generate_password_hash(request.form.get("password"))

        # Check if user exists
        row = db.execute("SELECT username FROM users WHERE username = :username",
                         username=request.form.get("username"))
        if len(row) != 0:
            return apology("The username is already taken!", 400)

        # Add user to database
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"),
                             hash=hashed_password)


        # Remember which user has logged in
        session["user_id"] = result

        # Display a flash message
        flash("Registered!")

        # Redirect user to home page
        return redirect("/")

     # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        # Check if the symbol exists
        if quote == None:
            return apology("invalid symbol", 400)

        # Check if shares was a positive integer
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 400)

        # Check if # of shares requested was 0
        if shares <= 0:
            return apology("cannot sell less than or 0 shares", 400)

        # Check if we have enough shares
        stock = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id AND symbol = :symbol GROUP BY symbol",
                           user_id=session["user_id"], symbol=request.form.get("symbol"))

        if len(stock) != 1 or stock[0]["total_shares"] <= 0 or stock[0]["total_shares"] < shares:
            return apology("Cannot sell less than 0 shares or more shares than you own", 400)

        # Query database for username
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # How much $$$ the user still has in her account
        cash_remaining = rows[0]["cash"]
        price_per_share = quote["price"]

        # Calculate the price of requested shares
        price = price_per_share * shares

        # Book keeping (TODO: should be wrapped with a transaction)
        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", price=price, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, time) VALUES(:user_id, :symbol, :shares, :price, datetime('now', 'utc'))",
                   user_id=session["user_id"],
                   symbol=request.form.get("symbol"),
                   shares=-shares,
                   price=price)

        flash("Sold!")

        return redirect("/")

    else:
        stocks = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])

    return render_template("sell.html", stocks=stocks)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
