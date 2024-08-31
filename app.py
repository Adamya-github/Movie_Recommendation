from flask import Flask, request, render_template
import joblib

app = Flask(__name__)

# Load data and model
df = joblib.load('/model/movies_df.pkl')
cosine_sim = joblib.load('/model/cosine_sim.pkl')

def get_recommendations(title):
    movie_index = df[df['title'] == title].index[0]
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:6]
    return [df.iloc[i[0]]['title'] for i in sorted_similar_movies]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['movie_title']
    recommendations = get_recommendations(movie_title)
    return render_template('index.html', recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
