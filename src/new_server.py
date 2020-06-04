from flask import Flask, render_template, request
from Clustering import main
from db_query import DBQuery


app = Flask(__name__)

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

        result = main(url, lang, num)
        # print(result)
        result = result.replace('\n', '<br>') 
        # return render_template("TimeStamp.html", result = result)
        return render_template("Result.html", result = result)
    
    else:
        return render_template("Index.html")
    
@app.route("/test")
def db_query_test():
    database = DBQuery()

    score = 5.0
    text = "Final test"

    database.insert_comment(score, text)
    score_rows = database.select_score()
    comment_rows = database.select_comment()

    database.close_db()

    print(f"\nscore_rows:\n{score_rows}\n")
    print(f"comment_rows:\n{comment_rows}\n")

    return render_template("DBQueryTest.html", score = score_rows, text = comment_rows)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
