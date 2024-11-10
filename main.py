from flask import Flask, redirect, request, render_template, url_for

app = Flask(__name__)

max_temp = 90
min_temp = 50
min_boundary = 0
max_boundary = 120
password = ""

water_pipe_engaged = False
emergency_pipe = False

password='albayan'
print(password)

@app.route("/")
def index():
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
            if temp_input < min_boundary or temp_input > max_boundary:
                return render_template('shut-and-call-manager.html')
            if temp_input > max_temp:
                if water_pipe_engaged:
                    if emergency_pipe:
                        return render_template('emergency.html')
                    emergency_pipe = True
                    return render_template('emergency-pipe.html')
                water_pipe_engaged = True
                return render_template('temp-high.html')
            elif temp_input == max_temp:
                if water_pipe_engaged:
                    return render_template('max-temp-after-high.html')
            if min_temp <= temp_input <= max_temp:
                emergency_pipe = False
                water_pipe_engaged = False
                return render_template('temp-right.html')
            else:
                return render_template('temp-low.html')

    if request.method == "POST":
        print("yel!")
        print(request.form.to_dict())
        if request.form.get('passwordtxt') == password:
            return render_template("control.html")
    elif request.method == "GET":
        print("yar!")
    return render_template("home.html")


if __name__ == "__main__":
    app.run()
