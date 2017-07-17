#coding:utf-8

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64



random_generator =Random.new().read

rsa = RSA.generate(1024, random_generator)
# private_pem =rsa.exportKey()
public_pem = rsa.publickey().exportKey()

# pubkey ='&#43;Bedvcv05Xpsy3CQZQbsnj1iI6xsvUzt02GxKCKainm2/Z5xzT&#43;VT3wD7&#43;'
pubKey2 ='''
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCr57Wb3aXQ6Yj0czKSnKnwXKwf
zrzgVuPJ+KlS1iJU0Yuf0l01/wxnbw5CUUabaNl450o8QwQWQRylk1CBMrOETIvA
93jcW87EhXSygFt8rG7sq2+2ga6UEatd8zUGjEkb3RhFdWFPWi7j8b0m0tle+pfT
6Lz9FPiXK8539MecRwIDAQAB
-----END PUBLIC KEY-----
'''
# print private_pem
print public_pem
# print type(public_pem)

message = 'wuhan123'
rsakey = RSA.importKey(public_pem)
cipher = Cipher_pkcs1_v1_5.new(rsakey)
cipher_text = base64.b64encode(cipher.encrypt(message))
print cipher_text
