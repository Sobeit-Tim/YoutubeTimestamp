from flask import Flask, render_template, request
import Clustering


app = Flask(__name__)

# @app.route("/", methods = ["GET", "POST"])
# def timestamp():
#     if request.method == "POST":
#         url = request.form["url"]
#         result = Clustering.main(url)
       
#         return render_template("Result.html", result = result)
#     else:
#         return render_template("Index.html")

@app.route("/")
def index():
    return render_template("Index.html")

@app.route("/timestamp", methods = ["GET", "POST"])
def timestamp():
    if request.method == "POST":
        url = request.form["url"]
        # print(url)

        result = Clustering.main(url)
        # print(result)
        
        # return render_template("TimeStamp.html", result = result)
        return render_template("Result.html", result = result)
    
    else:
        return render_template("Index.html")
    
# @app.route("/test")
# def test():
#     return render_template("VariableSendTest.html", test = "Test")

if __name__ == "__main__":
    app.run()