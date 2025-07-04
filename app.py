from os import environ
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
from rembg import remove
from requests import get

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            mine_type = file.content_type

            data = file.stream.read()
            result = remove(data=data)
            return Response(response=result, mimetype=mine_type, headers={
                'Content-Disposition': f'inline; filename=removedbg_{filename}'
            })

    url = request.args.get('url') or request.form.get('url')
    if url:
        downloadImageFromUrl = get(url)
        mine_type = downloadImageFromUrl.headers['Content-Type']
        data = downloadImageFromUrl.content
        result = remove(data=data)
        return Response(response=result, mimetype=mine_type, headers={
            'Content-Disposition': f'inline; filename=removedbg_{url.split("/")[-1]}'
        })

    return Response(response='No file or url provided', status=400)


if __name__ == '__main__':
    app.run(
        host=environ.get('HOST', '0.0.0.0'),
        port=int(environ.get('PORT', 10000)),  # 👈 fix importante
        debug=False
    )
