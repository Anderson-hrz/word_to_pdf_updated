from os import remove, path
from random import randint
from subprocess import check_output, CalledProcessError
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # Importando o CORS

app = Flask(__name__)

# Habilitar CORS para todas as rotas e origens
CORS(app)

# Função para gerar um nome único para os arquivos temporários
def generate_temp_filename(extension):
    return f'{randint(0, 1000)}.{extension}'

@app.route('/doc_to_pdf', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
            <input type="file" name="file" accept=".docx">
            <input type="submit" value="Upload">
        </form>
        '''
    
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400

    if file and file.filename.endswith('.docx'):
        try:
            # Gera um nome temporário para o arquivo DOCX e PDF
            docx_filename = generate_temp_filename('docx')
            pdf_filename = generate_temp_filename('pdf')

            # Salva o arquivo DOCX
            file.save(docx_filename)

            # Converte o arquivo DOCX para PDF
            try:
                check_output(['libreoffice', '--headless', '--convert-to', 'pdf', docx_filename])
            except CalledProcessError as e:
                return jsonify({'message': 'Error during file conversion', 'error': str(e)}), 500

            # Verifica se o arquivo PDF foi gerado
            if not path.exists(pdf_filename):
                return jsonify({'message': 'PDF conversion failed'}), 500

            # Envia o arquivo PDF para o cliente
            return send_file(pdf_filename, download_name=pdf_filename, as_attachment=True)

        except Exception as e:
            return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500
        
        finally:
            # Remove os arquivos temporários
            try:
                if path.exists(docx_filename):
                    remove(docx_filename)
                if path.exists(pdf_filename):
                    remove(pdf_filename)
            except Exception as e:
                # Log ou tratamento adicional pode ser feito aqui
                print(f'Error removing temporary files: {e}')

    else:
        return jsonify({'message': 'Invalid file format. Only DOCX files are accepted.'}), 400

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5006)
