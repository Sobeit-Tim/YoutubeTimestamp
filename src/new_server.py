from flask import Flask, render_template, request, flash, redirect, url_for, session
from Clustering import main
from db_query import DBQuery
import numpy as np

app = Flask(__name__)
app.secret_key = '1234321' #random number for client-side session, prevent temparing
# https://stackoverflow.com/questions/30223379/trying-to-flash-a-message-raises-an-exception'

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
            flash("URL is empty or Number of cluster is empty ")
            #return redirect(request.url)
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
            flash('Not available youtube URL')
            # return redirect(request.url)
            return render_template("index.html")
        err, result, subtitle = main(url, lang, num, video_name)
        # err - 1 : not available url
        #       2 : not supported youtube url
        #       3 : no language subtitle
        if err == 2: # not available url, no id
            #return err, "Not available youtube URL", "None"
            flash('Not available youtube URL')
            # return redirect(request.url)
            return render_template("index.html")
        if err == 3:
            flash('There is no subtitle for this languague in this video')
            return render_template("index.html")
        if err == 4:
            flash('Number of cluster might be too large to make a timestamp')
            return render_template("index.html")
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
        session['url'] = url
        session['lang'] = lang
        session['num'] = num
        session['video'] = video_name
        #score_rows =  ((63, 5, 'I love this so much!'), (64, 3, 'Not bad'), (65, 4, 'Pretty good'))
        #average_score = 4
        #return render_template("TimeStamp.html")
        return render_template("TimeStamp.html", video = link, result = result, subtitle = subtitle, average = average_score, score = comment_rows)
        #return render_template("Result.html", result = result)
    
    else:
        return render_template("index.html")
@app.route("/comment", methods = ["POST"])
def comment():
    if request.method == "POST":
        score = request.form["number"]
        text = request.form["review"] # number of cluster
        if not text:
            text = ' '
        database = DBQuery()
        database.insert_comment(score, text) # comment input  -> insert
        database.close_db()
        
        if "url" not in session:
            flash('wrong access')
            return redirect(url_for(index))
        url = session['url']
        lang = session['lang']
        num = session['num']
        video_name = session['video']
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
        session['url'] = url
        session['lang'] = lang
        session['num'] = num
        #score_rows =  ((63, 5, 'I love this so much!'), (64, 3, 'Not bad'), (65, 4, 'Pretty good'))
        #average_score = 4
        return render_template("TimeStamp.html", video = link, result = result, subtitle = subtitle, average = average_score, score = comment_rows)
        
    else:
        flash('wrong access')
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
