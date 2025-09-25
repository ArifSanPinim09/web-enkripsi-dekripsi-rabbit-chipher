"""
Cryptographic utilities for password handling and file encryption/decryption
"""

import hashlib
import secrets
import struct

class CryptoUtils:
    MAGIC_HEADER = b'MAGIC123'  # Header for validation
    HEADER_SIZE = 8  # Size of magic header
    
    @staticmethod
    def generate_key_from_password(password):
        """Generate encryption key from password using SHA-256"""
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        # Hash password with SHA-256 to create consistent key
        hash_obj = hashlib.sha256()
        hash_obj.update(password)
        key = hash_obj.digest()[:16]  # Use first 16 bytes for Rabbit cipher
        
        return key
    
    @staticmethod
    def encrypt_file_with_header(file_data, rabbit_cipher):
        """Encrypt file data with magic header for validation"""
        # Add magic header at the beginning
        data_with_header = CryptoUtils.MAGIC_HEADER + file_data
        
        # Encrypt the data with header
        encrypted_data = rabbit_cipher.encrypt(data_with_header)
        
        return encrypted_data
    
    @staticmethod
    def decrypt_file_with_header(encrypted_data, rabbit_cipher):
        """Decrypt file data and validate magic header"""
        # Decrypt the data
        decrypted_data = rabbit_cipher.decrypt(encrypted_data)
        
        # Check if magic header is present
        if not decrypted_data.startswith(CryptoUtils.MAGIC_HEADER):
            raise ValueError("Invalid password or corrupted file - magic header not found")
        
        # Remove magic header and return original file data
        original_data = decrypted_data[CryptoUtils.HEADER_SIZE:]
        
        return original_data
    
    @staticmethod
    def validate_password_strength(password):
        """Validate password strength and return score"""
        if not password:
            return {'score': 0, 'feedback': 'Password is required'}
        
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append('Use at least 8 characters')
        
        # Character variety checks
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        
        if has_lower:
            score += 1
        else:
            feedback.append('Include lowercase letters')
        
        if has_upper:
            score += 1
        else:
            feedback.append('Include uppercase letters')
        
        if has_digit:
            score += 1
        else:
            feedback.append('Include numbers')
        
        if has_special:
            score += 1
        else:
            feedback.append('Include special characters')
        
        # Determine strength level
        if score >= 6:
            strength = 'Very Strong'
        elif score >= 4:
            strength = 'Strong'
        elif score >= 2:
            strength = 'Medium'
        else:
            strength = 'Weak'
        
        return {
            'score': score,
            'strength': strength,
            'feedback': feedback if feedback else ['Password looks good!']
        }
    
    @staticmethod
    def generate_salt():
        """Generate random salt for key derivation"""
        return secrets.token_bytes(16)
    
    @staticmethod
    def secure_compare(a, b):
        """Constant-time string comparison to prevent timing attacks"""
        if len(a) != len(b):
            return False
        
        result = 0
        for x, y in zip(a, b):
            result |= x ^ y
        
        return result == 0