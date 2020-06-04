from flask import Flask, render_template, request
from Clustering import main
from db_query import DBQuery
import numpy as np

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
        if not num or not url: # empty url or empty num
            return render_template("index.html")

        num = int(num)        # number of cluster
        err = 0
        try:
            video_name_list = url.split('youtu.be/')
            if len(video_name_list) == 1:
                video_name = url.replace('v=', ' ').replace('&', ' ').split(' ')[1]
            else:
                video_name = video_name_list[1]
        except:
            err = 1
        
        if err == 1: # not available url, no id
            #return err, "Not available youtube URL", "None"
            return render_template("index.html")
        err, result, subtitle = main(url, lang, num, video_name)
        # err - 1 : not available url
        #       2 : not supported youtube url
        #       3 : no language subtitle
        result = result.replace('\n', '<br>')
        subtitle = subtitle.replace('\n', '<br>')
        link = "https://www.youtube.com/embed/" + video_name
        link = "\"{}\"".format(link)
        print(link)
        
        database = DBQuery()
        #score = 5.0
        #text = "Final test"
        #database.insert_comment(score, text) # comment input  -> insert
        score_rows = database.select_score()
        comment_rows = database.select_comment()
        database.close_db()
        print(f"\nscore_rows:\n{score_rows}\n")
        print(f"comment_rows:\n{comment_rows}\n")
        average_score = int(round(np.average(np.array(score_rows))))
        print("average", average_score)

        #score_rows =  ((63, 5, 'I love this so much!'), (64, 3, 'Not bad'), (65, 4, 'Pretty good'))
        #average_score = 4
        #return render_template("TimeStamp.html")
        return render_template("TimeStamp.html", video = link, result = result, subtitle = subtitle, average = average_score, score = comment_rows)
        #return render_template("Result.html", result = result)
    
    else:
        return render_template("index.html")
    
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
    average_score = int(round(np.average(np.array(score_rows))))
    print(average_score)
    return render_template("DBQueryTest.html", score = score_rows, text = comment_rows)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
