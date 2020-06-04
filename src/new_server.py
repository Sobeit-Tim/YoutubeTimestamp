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
    return render_template("index.html")

@app.route("/timestamp", methods = ["GET", "POST"])
def timestamp():
    if request.method == "POST":
        url = request.form["url"]
        num = request.form["cluster_num"] # number of cluster
        lang = request.form["language"] # en or ko
        num = int(num)        # number of cluster

        result = Clustering.main(url, lang, num)
        # print(result)
        result = result.replace('\n', '<br>') 
        # return render_template("TimeStamp.html", result = result)
        return render_template("Result.html", result = result)
    
    else:
        return render_template("Index.html")
    
# @app.route("/test")
# def test():
#     return render_template("VariableSendTest.html", test = "Test")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
