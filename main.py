from flask import Flask, redirect, request, render_template, url_for
import database

app = Flask(__name__)

# define variables
max_temp = 90
min_temp = 50
min_boundary = 0
max_boundary = 120
water_pipe_engaged = False
emergency_pipe = False
password='albayan'

# website goes to this by default
@app.route("/")
def index():
    # goes to
    return redirect(url_for("home"))

@app.route("/main/", methods=['GET','POST'])
def home():
    global water_pipe_engaged, emergency_pipe
    if request.method == 'POST':
        if request.form.keys().__contains__('gotomainpage'):
            return render_template("control.html")
        if request.form.get('send') == 'Submit' and request.form.get('temptxt') != None:
            try:
                temp_input = int(request.form.get('temptxt'))
            except ValueError as e:
                return render_template("wrong-input.html")
            database.save_input(temp_input)
            return judge_temp(temp_input)

    if request.method == "POST":
        print(request.form.to_dict())
        if request.form.get('passwordtxt') == password:
            return render_template("control.html")
    return render_template("home.html")

def judge_temp(temp_input):
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
        database.save_result("Temperature is too low.")
        return render_template('temp-low.html')

if __name__ == "__main__":
    app.run()
