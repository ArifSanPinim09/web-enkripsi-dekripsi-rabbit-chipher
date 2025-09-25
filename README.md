# PDFCrypto - Secure PDF Encryption with Rabbit Cipher

PDFCrypto is a web-based application that demonstrates the practical implementation of the Rabbit Cipher algorithm for securing PDF documents. Built as an educational project, it showcases modern cryptographic principles while providing a user-friendly interface for file encryption and decryption.

## 🔐 Features

- **Military-Grade Security**: Uses Rabbit Cipher, a high-speed stream cipher designed for maximum security
- **Password-Based Encryption**: SHA-256 key derivation from user passwords
- **Magic Header Validation**: Ensures successful decryption and password correctness
- **No Server Storage**: All processing happens temporarily, files are immediately deleted
- **Modern UI/UX**: Responsive design with dark/light mode support
- **Drag & Drop Interface**: Easy file upload with visual feedback
- **Password Generator**: Built-in strong password generation
- **Real-time Password Strength**: Visual feedback on password security

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd PDFCrypto
```

2. **Create a virtual environment**:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
python app.py
```

5. **Open your browser** and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
PDFCrypto/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── crypto/                # Cryptographic modules
│   ├── __init__.py
│   ├── rabbit_cipher.py   # Rabbit Cipher implementation
│   └── crypto_utils.py    # Encryption utilities
├── utils.py               # Helper functions
├── templates/             # Jinja2 templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── encrypt.html      # Encryption page
│   ├── decrypt.html      # Decryption page
│   └── about.html        # About page
└── static/               # Static assets
    ├── js/
    │   └── ui.js         # UI interactions
    └── css/              # Custom styles (if any)
```

## 🔧 Technical Details

### Rabbit Cipher Implementation

The Rabbit Cipher is a high-speed stream cipher with the following characteristics:

- **Key Size**: 128 bits
- **Algorithm Type**: Stream cipher
- **Performance**: Optimized for both software and hardware
- **Security**: Extensively analyzed by the cryptographic community

### Key Features:

1. **Password Hashing**: User passwords are hashed using SHA-256 to create consistent 128-bit keys
2. **Magic Header**: Each encrypted file contains a validation header (`MAGIC123`)
3. **Stream Processing**: Files are encrypted/decrypted in 16-byte blocks
4. **Error Handling**: Comprehensive validation for file integrity and password correctness

### Security Considerations

- Passwords are never stored on the server
- All processing happens server-side temporarily
- Files are immediately deleted after processing
- Magic header validation prevents brute force attacks
- SHA-256 provides cryptographically secure key derivation

## 🎯 Usage

### Encrypting a PDF

1. Navigate to the **Encrypt** page
2. Upload your PDF file (drag & drop or click to browse)
3. Enter a strong password or use the password generator
4. Click **Encrypt PDF**
5. Download the encrypted `.enc` file

### Decrypting a PDF

1. Navigate to the **Decrypt** page
2. Upload your encrypted `.enc` file
3. Enter the exact password used for encryption
4. Click **Decrypt PDF**
5. Download the restored PDF file

### Password Recommendations

- Minimum 8 characters (12+ recommended)
- Include uppercase and lowercase letters
- Include numbers and special characters
- Avoid common words or patterns
- Use the built-in password generator for maximum security

## 🔍 API Endpoints

- `GET /` - Homepage
- `GET /encrypt` - Encryption page
- `GET /decrypt` - Decryption page
- `GET /about` - About page
- `POST /api/encrypt` - Encrypt PDF file
- `POST /api/decrypt` - Decrypt encrypted file
- `GET /api/generate-password` - Generate strong password

## 🧪 Testing

To test the application:

1. **Prepare test files**: Use sample PDF files for testing
2. **Test encryption**: Encrypt a PDF with a known password
3. **Test decryption**: Decrypt the `.enc` file using the same password
4. **Verify integrity**: Ensure the decrypted PDF opens correctly
5. **Test error cases**: Try wrong passwords, corrupted files, etc.

## 🔒 Security Notes

### For Educational Use

This implementation is designed for educational purposes and demonstration of cryptographic concepts. For production use, consider:

- Additional security layers (HTTPS, CSRF protection)
- Rate limiting and DDoS protection
- Enhanced error handling and logging
- Professional security audit

### Password Security

- Never share your encryption passwords
- Store passwords securely (use a password manager)
- If you lose the password, the file cannot be recovered
- The application cannot recover or reset passwords

## 🤝 Contributing

This is an educational project. Contributions that improve the learning experience are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📚 Educational Resources

### Cryptography Concepts Demonstrated

- **Stream Ciphers**: Understanding how Rabbit Cipher works
- **Key Derivation**: SHA-256 hashing for password-based encryption
- **File Processing**: Binary data handling and manipulation
- **Security Validation**: Magic headers and integrity checking

### Learning Objectives

- Understand practical cryptographic implementation
- Learn about secure password handling
- Explore file encryption/decryption processes
- Study web application security principles

## ⚠️ Limitations

- Maximum file size: 50MB
- Single file processing only
- No batch operations
- Temporary server-side processing
- Educational implementation (not for commercial use)

## 📖 References

- [Rabbit Cipher Specification](https://tools.ietf.org/rfc/rfc4503.txt)
- [eSTREAM Project](https://www.ecrypt.eu.org/stream/)
- [SHA-256 Specification](https://tools.ietf.org/html/rfc6234)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Tailwind CSS](https://tailwindcss.com/)

## 📄 License

This project is created for educational purposes. Please check the repository for license details.

## 🙋‍♂️ Support

For questions, issues, or educational discussions:

1. Check existing issues in the repository
2. Create a new issue with detailed description
3. Include steps to reproduce any problems
4. Specify your environment (OS, Python version, etc.)

---

**Disclaimer**: This is an educational project demonstrating cryptographic concepts. While functional, it should not be used for production security without proper security review and hardening.