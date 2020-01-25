from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from bs4 import BeautifulSoup
import requests

# Creating flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a4jFh9qWatzZp7HcIh8HndR3K3XmXQYg'

headers = {
    'User-Agent': 'com.ss.android.ugc.trill/584 (Linux; U; Android 5.1.1; en_US; LG-H961N;',
}


# Creating the form
class RequestForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                           description="Enter the username in TikTok to see account's data",
                           render_kw={'class': 'form-control',
                                      'id': 'username',
                                      'placeholder': 'Enter username'}
                           )


# Create the view
@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = RequestForm()
    if form.validate_on_submit():
        username = form.username.data
        url = 'https://www.tiktok.com/@{}'.format(username)
        # Hit the TikTok server
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            # Parsing and getting the data from the page
            soup = BeautifulSoup(request.text, 'html.parser')
            avatar = soup.find(attrs={'class': 'profile-avatar'}).next_element
            following = soup.find(attrs={'title': 'Following'})
            followers = soup.find(attrs={'title': 'Followers'})
            likes = soup.find(attrs={'title': 'Likes'})
            username = username
            # Rendering the results page
            return render_template('results.html',
                                   avatar=avatar.attrs.get('src'),
                                   following=following.get_text(),
                                   followers=followers.get_text(),
                                   likes=likes.get_text(),
                                   username=username,
                                   )
    # Rendering the homepage
    return render_template('home.html', form=form)


# Entry point
if __name__ == '__main__':
    app.run()
