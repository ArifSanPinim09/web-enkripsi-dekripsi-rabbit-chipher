"""
Utility functions for password generation and other helpers
"""

import secrets
import string

class PasswordGenerator:
    """Password generation utilities"""
    
    @staticmethod
    def generate_strong_password(length=16):
        """Generate a strong password with mixed characters"""
        if length < 8:
            length = 8  # Minimum length for security
        
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase  
        digits = string.digits
        special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        # Ensure at least one character from each set
        password = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(special_chars)
        ]
        
        # Fill remaining length with random characters from all sets
        all_chars = lowercase + uppercase + digits + special_chars
        for _ in range(length - 4):
            password.append(secrets.choice(all_chars))
        
        # Shuffle the password list
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    @staticmethod
    def generate_passphrase(word_count=4):
        """Generate a passphrase with random words"""
        # Simple word list - in production, use a larger dictionary
        words = [
            'apple', 'banana', 'cherry', 'dragon', 'elephant', 'forest',
            'guitar', 'horizon', 'island', 'jungle', 'kitchen', 'lemon',
            'mountain', 'nebula', 'ocean', 'penguin', 'quantum', 'rainbow',
            'sunset', 'thunder', 'umbrella', 'volcano', 'waterfall', 'xenon',
            'yellow', 'zebra', 'adventure', 'butterfly', 'cascade', 'diamond'
        ]
        
        selected_words = []
        for _ in range(word_count):
            word = secrets.choice(words)
            # Capitalize first letter randomly
            if secrets.randbelow(2):
                word = word.capitalize()
            selected_words.append(word)
        
        # Join with random separators
        separators = ['-', '_', '.', '']
        separator = secrets.choice(separators)
        
        # Add random numbers at the end
        numbers = str(secrets.randbelow(1000)).zfill(2)
        
        return separator.join(selected_words) + numbers

class FileUtils:
    """File handling utilities"""
    
    @staticmethod
    def format_file_size(size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    @staticmethod
    def validate_pdf_header(file_data):
        """Validate PDF file header"""
        if not file_data:
            return False
        
        # PDF files start with %PDF
        return file_data.startswith(b'%PDF')
    
    @staticmethod
    def get_file_extension(filename):
        """Get file extension safely"""
        if '.' not in filename:
            return ''
        return filename.rsplit('.', 1)[1].lower()

class ValidationUtils:
    """Input validation utilities"""
    
    @staticmethod
    def is_safe_filename(filename):
        """Check if filename is safe for download"""
        if not filename:
            return False
        
        # Remove dangerous characters
        dangerous_chars = ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*']
        
        for char in dangerous_chars:
            if char in filename:
                return False
        
        return True
    
    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filename for safe download"""
        if not filename:
            return 'download'
        
        # Replace dangerous characters with underscore
        dangerous_chars = ['/', '\\', '<', '>', ':', '"', '|', '?', '*']
        
        for char in dangerous_chars:
            filename = filename.replace(char, '_')
        
        # Remove .. sequences
        filename = filename.replace('..', '_')
        
        # Limit length
        if len(filename) > 100:
            name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
            filename = name[:95] + ('.' + ext if ext else '')
        
        return filename