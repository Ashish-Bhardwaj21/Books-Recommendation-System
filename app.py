from flask import Flask,render_template,request
import pickle
import numpy as np
from fuzzywuzzy import fuzz,process


popular_dataf=pickle.load(open('populardata.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similar_scores = pickle.load(open('similar_scores.pkl','rb'))
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_dataf['Book-Title'].values),
                           author=list(popular_dataf['Book-Author'].values),
                           image=list(popular_dataf['Image-URL-M'].values),
                           votes=list(popular_dataf['num_ratings'].values),
                           rating=list(popular_dataf['avg_ratings'].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')

    query = user_input
    choices = []
    for i in range(0, len(pt)):
        choices.append(pt.index[i])

    book_name =process.extractOne(query, choices)[0]

    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similar_scores[index])), key=lambda xx: xx[1], reverse=True)[0:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item[2] = item[2][:4] + "s" + item[2][4:]
        data.append(item)
    print(data)

    return render_template('recommend.html', data=data)


if __name__=='__main__':
    app.run(debug=True)