import unittest
import tempfile
import os

from file_encryptor import convergence

class TestConvergence(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.mkdtemp()

        self.sample1 = os.path.join(self.directory, "super1.txt")
        self.sample2 = os.path.join(self.directory, "super2.txt")
        self.sample3 = os.path.join(self.directory, "frowny.txt")

        with open(self.sample1, "wb") as f:
            f.write("Superstar!\n".encode())

        with open(self.sample2, "wb") as f:
            f.write("Superstar!\n".encode())

        with open(self.sample3, "wb") as f:
            f.write("Frowny face :(\n".encode())

    def contents(self, name):
        with open(name, "rb") as f:
            return f.read()

    def tearDown(self):
        os.remove(self.sample1)
        os.remove(self.sample2)
        os.remove(self.sample3)
        os.rmdir(self.directory)

    def test_inline_encryption(self):
        convergence.encrypt_file_inline(self.sample1, None)

        self.assertNotEqual(
            self.contents(self.sample1),
            "Superstar!\n".encode())

    def test_inline_encryption_with_passphrase(self):
        convergence.encrypt_file_inline(self.sample1, "potato")

    def test_deterministic_inline_encryption(self):
        convergence.encrypt_file_inline(self.sample1, None)
        convergence.encrypt_file_inline(self.sample2, None)

        self.assertEqual(
            self.contents(self.sample1),
            self.contents(self.sample2))

    def test_passphrase_does_something(self):
        convergence.encrypt_file_inline(self.sample1, "first")
        convergence.encrypt_file_inline(self.sample2, "second")

        self.assertNotEqual(
            self.contents(self.sample1),
            self.contents(self.sample2))

    def test_inline_decryption(self):
        plaintext = self.contents(self.sample1)

        key = convergence.encrypt_file_inline(self.sample1, None)

        convergence.decrypt_file_inline(self.sample1, key)

        self.assertEqual(plaintext, self.contents(self.sample1))

    def test_inline_decryption_with_passphrase(self):
        plaintext = self.contents(self.sample1)

        key = convergence.encrypt_file_inline(self.sample1, "super secret")

        convergence.decrypt_file_inline(self.sample1, key)

        self.assertEqual(plaintext, self.contents(self.sample1))

    def test_streaming_decryption(self):
        plaintext = self.contents(self.sample1)

        key = convergence.encrypt_file_inline(self.sample1, "super secret")

        decrypted = "".encode()
        for chunk in convergence.decrypt_generator(self.sample1, key):
            decrypted += chunk

        self.assertEqual(plaintext, decrypted)
