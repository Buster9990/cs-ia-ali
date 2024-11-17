# Library for web development
from flask import Flask, redirect, request, render_template, url_for
# Imports database class
import database
# Imports datetime library for recording time of inputs in database.
import datetime
# Create a new web application
app = Flask(__name__)

# define variables
# Maximum temperature allowed without water pipes
max_temp = 90
# Minimum temperature in safe range
min_temp = 50
# Shut down if reaches or goes lower
min_boundary = 20
# Shut down if reaches or exceeds
max_boundary = 120
water_pipe_engaged = False
emergency_pipe = False
# System password
password='albayan'

# website goes to this by default
@app.route("/")
def index():
    # instantly sends to the function below.
    return redirect(url_for("home"))

@app.route("/main/", methods=['GET','POST'])
def home():
    # Allows use for these two global variables inside the function.
    global water_pipe_engaged, emergency_pipe
    # POST method is when input is received from the user
    if request.method == 'POST':
        # Button to go to main page is clicked.
        if request.form.keys().__contains__('gotomainpage'):
            # Goes to control page
            return render_template("control.html")
        # Button to view history is clicked
        elif request.form.keys().__contains__('viewhistory'):
            # Go to view history web page. data=database.read_all() is specifying a variable in the web-page for the information to show
            return render_template("view_history.html", data=database.read_all())
        # Right after login, the user hits the water pipe engaged button
        elif request.form.keys().__contains__('pipe_engaged'):
            # Save it
            water_pipe_engaged = True
            # Go to main page
            return render_template("control.html")
        # Right after login, the user hits the no pipe engaged button
        elif request.form.keys().__contains__('pipe_not_engaged'):
            # Set it to off
            water_pipe_engaged = False
            # go to main page
            return render_template("control.html")
        # Right after login, the user hits emergency pipe engaged button.
        elif request.form.keys().__contains__('emergency_pipe_engaged'):
            # Sets both pipe variables to true
            water_pipe_engaged = True
            emergency_pipe = True
            # go to main page
            return render_template("control.html")
        # Input is sent through the main page after the user hits the send button
        if request.form.get('send') == 'Submit' and request.form.get('temptxt') != None:
            # tries to convert the inputted string into an integer
            try:
                temp_input = int(request.form.get('temptxt'))
            except ValueError as e:
                # The user inputted a letter and not just a number, show they inputted the wrong thing.
                return render_template("wrong-input.html")
            # Saves the input, current pipe status, and the time with Bahrain's timezone.
            database.save_input(temp_input, water_pipe_engaged, emergency_pipe, datetime.datetime.utcnow() + datetime.timedelta(hours=3))
            # Method inside this script to judge what the response is according to the temperature inputted.
            return judge_temp(temp_input)
	# Checks for the input of the password
    if request.method == "POST":
        print(request.form.to_dict())
        if request.form.get('passwordtxt') == password:
            # password is correct, send the user to answer which pipes are engaged.
            return render_template("pipe-engaged.html")
    # If password is incorrect, asks for it again
    return render_template("home.html")

def judge_temp(temp_input):
    # Allows use for these global variables inside the functions.
    global water_pipe_engaged, emergency_pipe
    if temp_input < min_boundary or temp_input > max_boundary:
        database.save_result("Shut down and call manager")
        return render_template('shut-and-call-manager.html')
    if temp_input > max_temp:
        if water_pipe_engaged:
            if emergency_pipe:
                database.save_result("Call emergency, heat not going down even after using emergency pipe.")
                return render_template('emergency.html')
            emergency_pipe = True
            database.save_result("Engage emergency pipe.")
            return render_template('emergency-pipe.html')
        water_pipe_engaged = True
        database.save_result("Temperature is high, engage water pipe.")
        return render_template('temp-high.html')
    elif temp_input == max_temp:
        if water_pipe_engaged:
            database.save_result("Temperature not decreasing, engage emergency pipe.")
            emergency_pipe = True
            return render_template('max-temp-after-high.html')
    if min_temp <= temp_input <= max_temp:
        emergency_pipe = False
        water_pipe_engaged = False
        database.save_result("Temperature is within safe range")
        return render_template('temp-right.html')
    else:
        if water_pipe_engaged:
            database.save_result("Disengage pipe, temperature is low.")
            return render_template('temp-low.html', value="Disengage pipe, temperature is too low.")
        else:
            database.save_result("Temperature is too low, call manager.")
            return render_template('temp-low.html', value="Temperature is too low, call manager.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)