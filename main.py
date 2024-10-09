from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import numpy as np
import webcolors
from collections import Counter
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB upload limit

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)



def get_color_name(rgb_color):
    """
    Get the color name and HEX code for a given RGB color.
    """
    try:
        name = webcolors.rgb_to_name(rgb_color, spec='css3')
    except ValueError:
        name = "Unknown Color"
    hex_code = webcolors.rgb_to_hex(rgb_color)
    return name.title(), hex_code.upper()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)


            image = Image.open(filepath)
            image = image.convert('RGB')
            img_array = np.array(image)
            pixels = img_array.reshape(-1, 3)


            counts = Counter(map(tuple, pixels))
            top_colors = counts.most_common(10)


            color_info = []
            for color, count in top_colors:
                name, hex_code = get_color_name(color)
                color_info.append({
                    'name': name,
                    'hex': hex_code,
                    'count': count
                })

            return render_template('index.html', color_info=color_info, image_url=filepath)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5002)
