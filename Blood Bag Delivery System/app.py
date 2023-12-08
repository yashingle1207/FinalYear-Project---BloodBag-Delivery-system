from datetime import datetime
from bson import ObjectId
import os
from flask import Flask, render_template, request, jsonify, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = os.urandom(24)


# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')  # Update the MongoDB connection string
db = client['BloodBag']  # Update with your database name
HospUser = db['HospitalUsers']  # Collection for storing user data
BBUser = db['BloodBankUsers']  # Collection for storing user data
BloodStockAdd = db['BloodStock']
Searchbb = db['BloodStock']
Order = db['Orders']


def update_delivery_status(order_id):
    # Update the status to 'delivered'
    current_datetime = datetime.now()
    Order.update_one(
        {'_id': ObjectId(order_id)},
        {'$set': {'status': 'delivered', 'timestamp': current_datetime}}
    )


@app.route('/initiate_delivery', methods=['POST'])
def initiate_delivery():
    if request.method == 'POST':
        order_id = request.form.get('order_id')

        # Assuming you have a function to update the status in your MongoDB collection
        update_delivery_status(order_id)

        return render_template('dispatched.html')


@app.route('/ViewStock')
def viewstock():

        # Query MongoDB to fetch all blood bags
        blood_bags = Searchbb.find()

        # Prepare the results to be displayed or processed further
        results = []
        for bag in blood_bags:
            results.append({
                'blood_group': bag.get('blood_group'),  # Fix: use get method to access dictionary values
                'blood_component': bag.get('blood_component'),
                'quantity': bag.get('quantity'),
            })

        print(results)
        # Render the template with the results
        return render_template('ViewStock.html', results=results)

####################################

@app.route('/delorder', methods=['GET'])
def completed_orders():
    # Query MongoDB to get all orders
    orders = Order.find({'status': 'delivered'})

    # Prepare the results to be displayed
    order_list = []
    for order in orders:
        order_list.append({

            '_id': order.get('_id'),
            'Hospital_ID': order.get('Hospital_ID'),
            'BloodBank_Id': 'MH/105118',
            'BloodGrp': order.get('BloodGrp'),
            'BloodComp': order.get('BloodComp'),
            'BloodQuantity': order.get('BloodQuantity'),


            'req_type': order.get('req_type'),
            'fname': order.get('fname'),
            'mname': order.get('mname'),
            'lname': order.get('lname'),
            'age': order.get('age'),
            'regno': order.get('regno'),
            'ward': order.get('ward'),
            'bedno': order.get('bedno'),
            'gender': order.get('gender'),
            'diagnosis': order.get('diagnosis'),
            'reason_for_transfusion': order.get('reason_for_transfusion'),
            'officer_name': order.get('officer_name'),
            'officer_qualification': order.get('officer_qualification'),
            'doctor_reg_no': order.get('doctor_reg_no'),
            'doctor_mobile_no': order.get('doctor_mobile_no'),
            'timestamp': order.get('timestamp')
        })

    return render_template('DeliveredBags.html', orders=order_list)


@app.route('/delorder1', methods=['GET'])
def received_orders():
    # Query MongoDB to get all orders
    orders = Order.find({'status': 'delivered'})

    # Prepare the results to be displayed
    order_list = []
    for order in orders:
        order_list.append({

            '_id': order.get('_id'),
            'Hospital_ID': order.get('Hospital_ID'),
            'BloodBank_Id': 'MH/105118',
            'BloodGrp': order.get('BloodGrp'),
            'BloodComp': order.get('BloodComp'),
            'BloodQuantity': order.get('BloodQuantity'),


            'req_type': order.get('req_type'),
            'fname': order.get('fname'),
            'mname': order.get('mname'),
            'lname': order.get('lname'),
            'age': order.get('age'),
            'regno': order.get('regno'),
            'ward': order.get('ward'),
            'bedno': order.get('bedno'),
            'gender': order.get('gender'),
            'diagnosis': order.get('diagnosis'),
            'reason_for_transfusion': order.get('reason_for_transfusion'),
            'officer_name': order.get('officer_name'),
            'officer_qualification': order.get('officer_qualification'),
            'doctor_reg_no': order.get('doctor_reg_no'),
            'doctor_mobile_no': order.get('doctor_mobile_no'),
            'timestamp': order.get('timestamp')
        })

    return render_template('ReceivedBags.html', orders=order_list)

################################################################

@app.route('/BBNewReq', methods=['GET'])
def display_orders():
    # Query MongoDB to get all orders
    orders = Order.find({'status': 'undelivered'})

    # Prepare the results to be displayed
    order_list = []
    for order in orders:
        order_list.append({

            '_id': order.get('_id'),
            'Hospital_ID': order.get('Hospital_ID'),
            'BloodBank_Id': 'MH/105118',
            'BloodGrp': order.get('BloodGrp'),
            'BloodComp': order.get('BloodComp'),
            'BloodQuantity': order.get('BloodQuantity'),


            'req_type': order.get('req_type'),
            'fname': order.get('fname'),
            'mname': order.get('mname'),
            'lname': order.get('lname'),
            'age': order.get('age'),
            'regno': order.get('regno'),
            'ward': order.get('ward'),
            'bedno': order.get('bedno'),
            'gender': order.get('gender'),
            'diagnosis': order.get('diagnosis'),
            'reason_for_transfusion': order.get('reason_for_transfusion'),
            'officer_name': order.get('officer_name'),
            'officer_qualification': order.get('officer_qualification'),
            'doctor_reg_no': order.get('doctor_reg_no'),
            'doctor_mobile_no': order.get('doctor_mobile_no'),
            'timestamp': order.get('timestamp')
        })

    return render_template('BBNewReq.html', orders=order_list)

##############################################

@app.route('/submit_request', methods=['POST'])
def submit_request():
    if request.method == 'POST':
        # Get user input from the form
        req_type = request.form.get('reqtype')
        fname = request.form.get('fname')
        mname = request.form.get('mname')
        lname = request.form.get('lname')
        age = int(request.form.get('age'))

        regno = request.form.get('regno')
        ward = request.form.get('ward')
        bedno = request.form.get('bedno')
        gender = request.form.get('gender')

        diagnosis = request.form.get('diagnosis')
        reason_for_transfusion = request.form.get('reasonfortransfusion')

        officer_name = request.form.get('officername')
        officer_qualification = request.form.get('officerqualification')
        doctor_reg_no = request.form.get('regno')
        doctor_mobile_no = request.form.get('mobileno')

        # Decrease the quantity of blood bags in MongoDB
        blood_group = session.get('blood_group')
        blood_component = session.get('blood_component')
        requested_quantity = int(session.get('quantity'))

        # Create a dictionary with the form data
        form_data = {
            'Hospital_ID': session.get('hosp_reg_no'),
            'BloodBank_Id': 'MH/105118',
            'BloodGrp': blood_group,
            'BloodComp':blood_component,
            'BloodQuantity': requested_quantity,
            'req_type': req_type,
            'fname': fname,
            'mname': mname,
            'lname': lname,
            'age': age,
            'regno': regno,
            'ward': ward,
            'bedno': bedno,
            'gender': gender,
            'diagnosis': diagnosis,
            'reason_for_transfusion': reason_for_transfusion,
            'officer_name': officer_name,
            'officer_qualification': officer_qualification,
            'doctor_reg_no': doctor_reg_no,
            'doctor_mobile_no': doctor_mobile_no,
            'timestamp': datetime.now(),
            'status': 'undelivered'
        }

        # Insert the form data into the Order collection in MongoDB
        Order.insert_one(form_data)



        # Find the relevant blood bags in the database
        blood_bags = BloodStockAdd.find({'blood_group': blood_group, 'blood_component': blood_component})

        # Update the quantity of each blood bag
        for blood_bag in blood_bags:
            available_quantity = blood_bag.get('quantity', 0)
            if available_quantity >= requested_quantity:
                new_quantity = available_quantity - requested_quantity
                # Update the quantity in the database
                BloodStockAdd.update_one(
                    {'_id': blood_bag['_id']},
                    {'$set': {'quantity': new_quantity}}
                )
            else:
                # Handle insufficient quantity error
                return render_template('error.html', message='Insufficient quantity of blood bags.')

    return render_template('map.html')
#############################################


#################################################


@app.route('/searchbb', methods=['POST'])
def search_blood_bag():
    if request.method == 'POST':
        # Get user input from the form
        blood_group = request.form.get('bloodgrp')
        blood_component = request.form.get('comptype')
        quantity = int(request.form.get('quantity'))

        # Query MongoDB to find matching blood bags
        blood_bags = Searchbb.find({
            'blood_group': blood_group,
            'blood_component': blood_component,
            'quantity': {'$gte': quantity}  # Filter bags with quantity greater than or equal to user input
        })


        # Store the values in the user's session
        session['blood_group'] = blood_group
        session['blood_component'] = blood_component
        session['quantity'] = quantity


        # Prepare the results to be displayed or processed further
        results = []
        for bag in blood_bags:
            results.append({
                'blood_group': bag['blood_group'],
                'blood_component': bag['blood_component'],
                'quantity': bag['quantity'],

            })

        # Return the results, you can customize this part based on your needs
        return render_template('SearchResults.html', results=results)

    return render_template('SearchResults.html')



@app.route('/addbb', methods=['POST'])
def add_blood_bag():
    if request.method == 'POST':
        # Get user input from the form
        blood_group = request.form.get('bloodgrp')
        blood_component = request.form.get('comptype')
        quantity = int(request.form.get('quantity'))

        # Check if a record with the same blood group and blood component exists
        existing_record = BloodStockAdd.find_one({'blood_group': blood_group, 'blood_component': blood_component})

        if existing_record:
            # If the record exists, update the quantity
            new_quantity = existing_record['quantity'] + quantity
            # Update the existing record with the new quantity
            BloodStockAdd.update_one(
                {'blood_group': blood_group, 'blood_component': blood_component},
                {'$set': {'quantity': new_quantity, 'timestamp': datetime.now()}}
            )
        else:
            # If the record does not exist, create a new record
            blood_bag_info = {
                'blood_group': blood_group,
                'blood_component': blood_component,
                'quantity': quantity,
                'timestamp': datetime.now()
            }
            # Insert the blood bag information into MongoDB
            BloodStockAdd.insert_one(blood_bag_info)

    return render_template('StockAddSuccessful.html')





###########################################

@app.route('/HospSignUp', methods=['POST'])
def Hospsignup():
    if request.method == 'POST':
        # Get user input from the signup form
        facility_name = request.form.get('facilityName')
        facility_email = request.form.get('facilityEmailId')
        facility_password = request.form.get('facilityPassword')
        facility_contact_num = request.form.get('facilityContactNum')
        facility_address = request.form.get('facilityAddress')
        facility_reg_num = request.form.get('facilityRegNum')

        # Check if the email already exists
        existing_user = HospUser.find_one({'email': facility_email})
        if existing_user:
            return jsonify({'status': 'Email already exists'})

        # Create a new user document
        new_user = {
            'facility_name': facility_name,
            'email': facility_email,
            'password': facility_password,
            'contact_num': facility_contact_num,
            'address': facility_address,
            'reg_num': facility_reg_num
        }

        # Insert the new user into the MongoDB collection
        HospUser.insert_one(new_user)

    return render_template('HospitalDashboard.html')

@app.route('/HospSignIn', methods=['POST'])
def HospsignIn():
    if request.method == 'POST':
        # Get user input from the login form
        hosp_email = request.form.get('hospEmailId')
        hosp_password = request.form.get('hospPassword')

        # Check if the user exists in the database
        existing_user = HospUser.find_one({'email': hosp_email, 'password': hosp_password})
        if existing_user:
            # Fetch the registration number from the user data
            hosp_reg_no = existing_user.get('reg_num')

            # Set the registration number in the session
            session['hosp_reg_no'] = hosp_reg_no

            # You can redirect to the hospital dashboard or render a template
            return render_template('HospitalDashboard.html', hosp_email=hosp_email, hosp_reg_no=hosp_reg_no)
        else:
            return render_template('LoginUnsuccessful.html')

    return render_template('HospitalSignIn.html')



@app.route('/BBSignUp', methods=['POST'])
def BBsignup():
    if request.method == 'POST':
        # Get user input from the signup form
        bb_name = request.form.get('BBName')
        bb_email = request.form.get('BBEmail')
        bb_password = request.form.get('BBPass')
        contact_num = request.form.get('ContactNum')
        address = request.form.get('Address')
        reg_num = request.form.get('RegNum')

        # Check if the email already exists
        existing_user = BBUser.find_one({'email': bb_email})
        if existing_user:
            return jsonify({'status': 'Email already exists'})

        # Create a new user document
        new_user = {
            'bb_name': bb_name,
            'email': bb_email,
            'password': bb_password,
            'contact_num': contact_num,
            'address': address,
            'reg_num': reg_num
        }

        # Insert the new user into the MongoDB collection
        BBUser.insert_one(new_user)

    return render_template('BloodBankDashboard.html')


@app.route('/BBSignIn', methods=['POST'])
def BBsignIn():
    if request.method == 'POST':
        # Get user input from the login form
        bb_email = request.form.get('BBemail1')
        bb_password = request.form.get('BBpass1')

        # Check if the user exists in the database
        existing_user = BBUser.find_one({'email': bb_email, 'password': bb_password})
        if existing_user:
            # You can redirect to the blood bank dashboard or render a template
            return render_template('BloodBankDashboard.html', bb_email=bb_email)
        else:
            return render_template('LoginUnsuccessful.html')

    return render_template('BloodBankDashboard.html')  # Update with the correct template name





##################################

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/HospDashboard')
def hospdash():
    return render_template('HospitalDashboard.html')

@app.route('/BBDashboard')
def bbdash():
    return render_template('BloodBankDashboard.html')

@app.route('/AddBB')
def addbb():
    return render_template('AddBloodBags.html')

@app.route('/Stockadded')
def stockadd():
    return render_template('StockAddSuccessful.html')


@app.route('/SearchResults')
def searchres():
    return render_template('SearchResults.html')


@app.route('/BBNewReq')
def bbnewreq():
    return render_template('BBNewReq.html')

@app.route('/SearchBlood')
def searchblood():
    return render_template('SearchBloodBag.html')

@app.route('/Blood order')
def reqform():
    return render_template('BloodBagRequestForm.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contact')
def contactus():
    return render_template('contactus.html')


@app.route('/map')
def map():
    return render_template('map.html')

# @app.route('/dispatch')
# def dispatch():
#     return render_template('dispatched.html')


@app.route('/HospSign')
def Hospsign():
    return render_template('HospSignup.html')

@app.route('/BBSign')
def BBsign():
    return render_template('BBSignup.html')

@app.route('/LoginUnsuccessful')
def faillogin():
    return render_template('LoginUnsuccessful.html')

# Decorator to handle CORS headers
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

app.after_request(add_cors_headers)

@app.route('/update_location', methods=['GET'])
def update_location():
    data = request.json  # Assuming the data is sent as JSON
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Store or process the location data as needed

    return jsonify({'status': 'Location updated successfully'})

@app.route('/submit_order', methods=['POST'])
def submit_order():
    blood_type = request.form['blood_type']
    quantity = request.form['quantity']
    # Here, you can process the order, save it to a database, etc.
    return f"Order placed: Blood Type - {blood_type}, Quantity - {quantity}"


if __name__ == '__main__':
    app.run(debug=True)
