from flask import Flask, render_template, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SoopaSafe'
app.config['UPLOAD_FOLDER'] = 'uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


class FeedingMachine(FlaskForm):
    file = FileField(validators=[
        FileAllowed(photos, 'Only Images are allowed!'),
        FileRequired('Choose a file to upload.')])
    submit = SubmitField('Upload File')

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = FeedingMachine()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file)    
        file_url = url_for('get_file', file=file) # this will display the uploaded image
    else:
        file_url = None
    return render_template('index.html', form=form, file_url=file_url)

if __name__ == '__main__':
    app.run(debug=True)



