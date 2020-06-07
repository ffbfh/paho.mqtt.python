#!/usr/bin/env python3
"""Crypto Helper class

Author:
    Fabian Fischer <fabian.fischer.1@students.bfh.ch>
"""

import nacl.encoding
import nacl.signing
import base64


class CryptoHelper():
    """Empty CryptoHelper as a container."""
    def __init__(self):
        """Initialize all properties to None."""
        self._private_key = None
        self._public_key = None

    @property
    def private_key(self):
        """private key, also known as signing key"""
        return self._private_key

    @property
    def public_key(self):
        """public key, also known as verify key"""
        return self._public_key

    def generate_keypair(self):
        """Helper function for generating EdDSA key pair."""
        self._private_key = nacl.signing.SigningKey.generate()
        self._public_key = self._private_key.verify_key

    def get_public_key(self):
        return self._public_key.encode(encoder=nacl.encoding.RawEncoder)

    def get_public_key_encoded(self, padding=True):
        if padding:
            encoded = str(base64.b32encode(self._public_key.encode(
                encoder=nacl.encoding.RawEncoder)), 'utf-8')
        else:
            encoded = str(base64.b32encode(self._public_key.encode(
                encoder=nacl.encoding.RawEncoder)).rstrip(b'='), 'utf-8')

        return encoded

    def sign_message(self, message):
        return self._private_key.sign(message)
