from os import remove
from random import randint
from subprocess import check_output
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # Importando o CORS

app = Flask(__name__)

# Habilitar CORS para todas as rotas e origens
CORS(app)

@app.route('/doc_to_pdf', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
        '''
    
    filename = randint(0, 1000)
    filename = {
        'docx': f'{filename}.docx',
        'pdf': f'{filename}.pdf'
    }

    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp

    if file and request.method == 'POST':
        try:
            # Salva o arquivo DOCX
            file.save(filename["docx"])
            # Converte o DOCX para PDF
            check_output(['libreoffice', '--headless', '--convert-to', 'pdf', filename["docx"]])
            # Envia o arquivo PDF para o cliente
            return send_file(filename["pdf"], download_name=filename["pdf"], as_attachment=True)
        except Exception as e:
            return str(e)
        finally:
            try:
                # Remove os arquivos temporários
                for key in filename:
                    remove(filename[key])
            except:
                pass

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5006, debug=True)
