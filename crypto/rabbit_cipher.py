"""
Rabbit Cipher Implementation
A high-speed stream cipher algorithm
"""

import struct

class RabbitCipher:
    def __init__(self, key):
        """Initialize Rabbit cipher with 128-bit key"""
        if isinstance(key, str):
            key = key.encode('utf-8')
        
        if len(key) < 16:
            # Pad key to 16 bytes if shorter
            key = key + b'\x00' * (16 - len(key))
        elif len(key) > 16:
            # Truncate key to 16 bytes if longer
            key = key[:16]
        
        self.key = key
        self.x = [0] * 8  # Internal state
        self.c = [0] * 8  # Counter system
        self.carry = 0
        
        self._key_setup()
    
    def _key_setup(self):
        """Initialize the cipher state with the key"""
        # Convert key to 32-bit words
        key_words = list(struct.unpack('<4I', self.key))
        
        # Expand key words
        subkeys = []
        for i in range(8):
            if i % 2 == 0:
                subkeys.append(key_words[i // 2])
            else:
                subkeys.append(key_words[(i // 2 + 1) % 4])
        
        # Initialize state and counters
        for i in range(8):
            if i % 2 == 0:
                self.x[i] = subkeys[i]
                self.c[i] = subkeys[(i + 1) % 8]
            else:
                self.x[i] = subkeys[i]
                self.c[i] = subkeys[(i + 1) % 8]
        
        # Initial iteration to mix the state
        for _ in range(4):
            self._next_state()
    
    def _rotl32(self, n, b):
        """32-bit left rotation"""
        n &= 0xFFFFFFFF
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF
    
    def _g_func(self, x):
        """G function for Rabbit cipher"""
        x &= 0xFFFFFFFF
        x = (x * x) & 0xFFFFFFFFFFFFFFFF
        return (x ^ (x >> 32)) & 0xFFFFFFFF
    
    def _next_state(self):
        """Generate next internal state"""
        # Counter system
        c_old = self.c[:]
        
        for i in range(8):
            temp = (c_old[i] + 0x4D34D34D + self.carry) & 0xFFFFFFFFFFFFFFFF
            self.carry = temp >> 32
            self.c[i] = temp & 0xFFFFFFFF
        
        # Next-state function
        g = [0] * 8
        for i in range(8):
            g[i] = self._g_func((self.x[i] + self.c[i]) & 0xFFFFFFFF)
        
        self.x[0] = (g[0] + self._rotl32(g[7], 16) + self._rotl32(g[6], 16)) & 0xFFFFFFFF
        self.x[1] = (g[1] + self._rotl32(g[0], 8) + g[7]) & 0xFFFFFFFF
        self.x[2] = (g[2] + self._rotl32(g[1], 16) + self._rotl32(g[0], 16)) & 0xFFFFFFFF
        self.x[3] = (g[3] + self._rotl32(g[2], 8) + g[1]) & 0xFFFFFFFF
        self.x[4] = (g[4] + self._rotl32(g[3], 16) + self._rotl32(g[2], 16)) & 0xFFFFFFFF
        self.x[5] = (g[5] + self._rotl32(g[4], 8) + g[3]) & 0xFFFFFFFF
        self.x[6] = (g[6] + self._rotl32(g[5], 16) + self._rotl32(g[4], 16)) & 0xFFFFFFFF
        self.x[7] = (g[7] + self._rotl32(g[6], 8) + g[5]) & 0xFFFFFFFF
    
    def _extract(self):
        """Extract 128-bit keystream block"""
        s = [0] * 4
        
        s[0] = (self.x[0] ^ (self.x[5] >> 16) ^ (self.x[3] << 16)) & 0xFFFFFFFF
        s[1] = (self.x[2] ^ (self.x[7] >> 16) ^ (self.x[5] << 16)) & 0xFFFFFFFF
        s[2] = (self.x[4] ^ (self.x[1] >> 16) ^ (self.x[7] << 16)) & 0xFFFFFFFF
        s[3] = (self.x[6] ^ (self.x[3] >> 16) ^ (self.x[1] << 16)) & 0xFFFFFFFF
        
        return struct.pack('<4I', *s)
    
    def encrypt(self, data):
        """Encrypt data using Rabbit cipher"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        result = bytearray()
        data_len = len(data)
        
        for i in range(0, data_len, 16):
            # Generate keystream block
            self._next_state()
            keystream = self._extract()
            
            # XOR with data block
            block = data[i:i+16]
            for j in range(len(block)):
                result.append(block[j] ^ keystream[j])
        
        return bytes(result)
    
    def decrypt(self, data):
        """Decrypt data using Rabbit cipher (same as encrypt due to XOR)"""
        return self.encrypt(data)
    
    def reset(self):
        """Reset cipher to initial state"""
        self.x = [0] * 8
        self.c = [0] * 8
        self.carry = 0
        self._key_setup()