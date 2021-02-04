from flask import render_template, request
from app import app
import app.upc_lookup as ul
from app.sql_manager import sqlManager

DB_NAME = "test1"

cart = []
'''
    {'name': 'Thing 1', 'price': 2.50, 'pricestr': '2.50', 'qty': 2, 'upc': 000, 'EAN': 000},
    {'name': 'Thing 3', 'price': 0.10, 'pricestr': '0.10', 'qty': 15, 'upc': 000, 'EAN': 000},
    {'name': 'Thing 4', 'price': 15.66, 'pricestr': '15.66', 'qty': 10, 'upc': 000, 'EAN': 000},
    {'name': 'Thing 5', 'price': 12.11, 'pricestr': '12.11', 'qty': 9, 'upc': 000, 'EAN': 000},
    {'name': 'Thing 6', 'price': 0.85, 'pricestr': '0.85', 'qty': 1, 'upc': 000, 'EAN': 000},
    {'name': 'Thing 7', 'price': 2.66, 'pricestr': '2.66', 'qty': 2, 'upc': 000, 'EAN': 000},
    {'name': 'Thing 8', 'price': 18.98, 'pricestr': '18.98', 'qty': 1, 'upc': 000, 'EAN': 000},
    {'name': 'Trident Vibes Gum Tropical 1X40 Pc', 'price': 2.49, 'pricestr': '2.49', 'qty': 1, 'upc': 000, 'EAN': 000},
    {'name': 'Old Spice Hardest Working Collection Antiperspirant & Deodorant For Men Pure Sport Plus - 2.6Oz', 'price': 3.50, 'pricestr': '3.50', 'qty': 1, 'upc': 000, 'EAN': 000},
    {'name': 'Steelseries - Arctis 5 Wired Dts Headphone Gaming Headset For Pc And Playstation 4 - Black', 'price': 18.99, 'pricestr': '18.99', 'qty': 1, 'upc': 000, 'EAN': 000}]
'''

@app.route('/')
def index():
    ns = not ul.isScanner()
    return render_template("index.html", notScanner=ns)

@app.route('/tracker')
def about():
    ns = not ul.isScanner()
    return render_template("tracker.html", cart=cart, notScanner=ns)


@app.route('/response', methods=['POST'])
def lookup_code():
    upc = request.form.get("bcval")
    pd = ul.get_and_parse(upc)
    if pd.status == ul.Status.HTTP_ERROR:
        return render_template("index.html", error="API call error")
    elif pd.status == ul.Status.BC_NOT_FOUND:
        return render_template("index.html", error="Barcode not found in lookup")
    elif pd.status == ul.Status.OK:
        return render_template("index.html", upc=pd.upc, ean=pd.ean, name=pd.name,
                desc=pd.desc, lprice=pd.lprice,
                lpricestr="{price:.02f}".format(price=pd.lprice))
    else:
        return render_template("index.html", error="Unknown error")

@app.route('/additem', methods=['POST'])
def add_item_to_cart():
    # This needs to be fixed... static db object would be ideal
    db = sqlManager(DB_NAME)

    # Get upc, search database
    upc = request.form.get("bcval")
    db_entry_upc = db.select_product_by_upc(upc)  #This is terrible. Fix please!
    db_entry_ean = db.select_product_by_ean(upc)

    # Get data
    if (len(db_entry_upc) > 0):
        pd = ul.construct_pd(db_entry_upc[0])
    elif (len(db_entry_upc) > 0):
        pd = ul.construct_pd(db_entry_ean[0])
    else:
        pd = ul.get_and_parse(upc)

    # Process data
    if pd.status == ul.Status.HTTP_ERROR:
        # Calculate cart total price
        for item in cart:
            cart_total += item["price"] * item["qty"]
        return render_template("tracker.html", error="API call error", cart=cart, cart_total=cart_total)
    elif pd.status == ul.Status.BC_NOT_FOUND:
        # Calculate cart total price
        for item in cart:
            cart_total += item["price"] * item["qty"]
        return render_template("tracker.html", error="Barcode not found in lookup", cart=cart, cart_total=cart_total)
    elif pd.status == ul.Status.OK:
        db.create_product((pd.upc, pd.ean, pd.name, pd.desc, pd.lprice))
        # Check if item is in cart
        item_index = 0
        item_exists = False
        for item in cart:
            if item["upc"] == pd.upc:
                item_index = cart.index(item)
                item_exists = True
        if item_exists:
            # Increment qty by 1 if item is in cart
            cart[item_index]["qty"] += 1
        else:
            # Add entry to cart list (Use SQLite for this in the future??)
            cart.append({'name': pd.name, 'price': pd.lprice,
            'pricestr': "{price:.02f}".format(price=pd.lprice), 'qty': 1, 'desc': pd.desc, 'upc': pd.upc, 'ean': pd.ean})
        # Calculate total
        cart_total = 0
        for item in cart:
            cart_total += item["price"] * item["qty"]

        #print(db.select_all_products())
        return render_template("tracker.html", cart=cart, cart_total=cart_total)
    else:
        return render_template("trtacker.html", error="Unknown error")
