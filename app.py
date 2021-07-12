from flask import Flask, render_template, redirect, url_for
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import amazon
import summary

subscription_key = "4e6fc5014582468ea54de7d20dae4ad6"
endpoint = "https://trace-textanalysis.cognitiveservices.azure.com/"

def authenticate_client():
    ta_credential = AzureKeyCredential(subscription_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

def sentiment_analysis_example(client):
    r2.sentimental_analysis = ""
    p=0
    n=0
    review_list = form.all_reviews
    for x in review_list:
        documents = [x]
        response = client.analyze_sentiment(documents=documents)[0]
        pos = response.confidence_scores.positive
        neg = response.confidence_scores.negative
        if(pos>neg):
            p=p+1
        elif(neg>pos):
            n=n+1
    if(p>n):
        r2.sentimental_analysis = "positive"
    elif(p==0 and n==0):
        r2.sentimental_analysis = "neutral" 
    else:
        r2.sentimental_analysis = "negative"
    print("Document Sentiment: {}".format(r2.sentimental_analysis))


app = Flask(__name__)

app.config['SECRET_KEY'] = '7b040a256ba53639fe34e81ccba6bb41'

@app.route("/", methods = ['GET','POST'])
def home_page():
    global form
    form=ReviewForm()
    r2.review_string = ""
    if form.validate_on_submit():
        l=len(form.review.data)
        ending=form.review.data[l-11:]
        if ending !='all_reviews':
            return redirect(url_for('error_page'))
        else:
            form.all_reviews = amazon.get_review(form.review.data)
            for i in form.all_reviews:
                r2.review_string=r2.review_string+i+" "
            sentiment_analysis_example(client)
            r2.summary_text = summary.create_summary(r2.review_string)
            r2.user_review = form.all_reviews
            print(r2.summary_text)
            return redirect(url_for('result_page'))
    return render_template('home.html', form=form)

@app.route("/results")
def result_page():
    return render_template('results.html', d1 = r2.review_string, d2 = r2.sentimental_analysis, d3 = r2.summary_text)

@app.route("/error")
def error_page():
    return render_template('error.html')

class ReviewForm(FlaskForm):
    review = StringField(label='Enter an Amazon product link: ')
    submit = SubmitField(label='Check Sentiment')
    all_reviews = []   


class Results():
    review_string = ""
    sentimental_analysis = "" 
    key_phrases = []
    summary_text = ""
    
r2 = Results()


if __name__ == '__main__':
    app.debug = True
    app.run()