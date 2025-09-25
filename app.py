from flask import Flask, render_template, request, send_file, jsonify, flash
import os
import tempfile
import hashlib
import secrets
from werkzeug.utils import secure_filename
from crypto.rabbit_cipher import RabbitCipher
from crypto.crypto_utils import CryptoUtils
from utils import PasswordGenerator
import io

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Allowed extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@app.route('/encrypt')
def encrypt_page():
    """Encryption page"""
    return render_template('encrypt.html')

@app.route('/decrypt')
def decrypt_page():
    """Decryption page"""
    return render_template('decrypt.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/api/generate-password')
def generate_password():
    """Generate strong password recommendation"""
    try:
        length = int(request.args.get('length', 16))
        password = PasswordGenerator.generate_strong_password(length)
        return jsonify({'success': True, 'password': password})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/encrypt', methods=['POST'])
def encrypt_file():
    """Encrypt PDF file"""
    try:
        # Validate file upload
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file selected'})
        
        file = request.files['file']
        password = request.form.get('password', '').strip()
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if not password:
            return jsonify({'success': False, 'error': 'Password is required'})
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Only PDF files are allowed'})
        
        # Read file data
        file_data = file.read()
        
        # Validate PDF header
        if not file_data.startswith(b'%PDF'):
            return jsonify({'success': False, 'error': 'Invalid PDF file format'})
        
        # Generate encryption key from password
        encryption_key = CryptoUtils.generate_key_from_password(password)
        
        # Encrypt file
        rabbit_cipher = RabbitCipher(encryption_key)
        encrypted_data = CryptoUtils.encrypt_file_with_header(file_data, rabbit_cipher)
        
        # Create temp file for download
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.enc')
        temp_file.write(encrypted_data)
        temp_file.close()
        
        # Generate secure filename
        original_name = secure_filename(file.filename)
        encrypted_filename = f"{original_name.rsplit('.', 1)[0]}.enc"
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=encrypted_filename,
            mimetype='application/octet-stream'
        )
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Encryption failed: {str(e)}'})
    finally:
        # Clean up temp file
        try:
            if 'temp_file' in locals():
                os.unlink(temp_file.name)
        except:
            pass

@app.route('/api/decrypt', methods=['POST'])
def decrypt_file():
    """Decrypt encrypted file"""
    try:
        # Validate file upload
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file selected'})
        
        file = request.files['file']
        password = request.form.get('password', '').strip()
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if not password:
            return jsonify({'success': False, 'error': 'Password is required'})
        
        if not file.filename.lower().endswith('.enc'):
            return jsonify({'success': False, 'error': 'Only .enc files are allowed for decryption'})
        
        # Read encrypted data
        encrypted_data = file.read()
        
        # Generate decryption key from password
        decryption_key = CryptoUtils.generate_key_from_password(password)
        
        # Decrypt file
        rabbit_cipher = RabbitCipher(decryption_key)
        
        try:
            decrypted_data = CryptoUtils.decrypt_file_with_header(encrypted_data, rabbit_cipher)
        except ValueError as e:
            return jsonify({'success': False, 'error': 'Invalid password or corrupted file'})
        
        # Validate decrypted PDF
        if not decrypted_data.startswith(b'%PDF'):
            return jsonify({'success': False, 'error': 'Invalid password - decrypted data is not a valid PDF'})
        
        # Create temp file for download
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.write(decrypted_data)
        temp_file.close()
        
        # Generate filename
        original_name = secure_filename(file.filename)
        pdf_filename = f"{original_name.rsplit('.', 1)[0]}.pdf"
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=pdf_filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Decryption failed: {str(e)}'})
    finally:
        # Clean up temp file
        try:
            if 'temp_file' in locals():
                os.unlink(temp_file.name)
        except:
            pass

@app.errorhandler(413)
def too_large(e):
    return jsonify({'success': False, 'error': 'File too large. Maximum size is 50MB.'}), 413

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)