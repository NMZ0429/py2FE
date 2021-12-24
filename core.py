import os
import random
from pathlib import Path
from typing import List, Tuple, Optional

from cryptography.fernet import Fernet


class TwoFactorCryptor:
    def __init__(self, keyword: str = "YourSecretKey", output_path: str = "") -> None:
        self.keyword = keyword  # not really necessary for now.
        self.output_path = output_path  # not really necessary for now.

    def __call__(
        self,
        file_path: str,
        key_path: Optional[str] = None,
        mode: str = "encrypt",
        output_path: str = "",
    ) -> None:
        # apply encrypt or decrypt to the file and save it
        output_path = output_path or self.output_path
        if mode == "encrypt":
            with open(file_path, "rb") as f:
                raw_bytes = f.read()

            encrypted_bytes, altered_key = self.encrypt(raw_bytes)
            self.__write_enc(file_path, encrypted_bytes, altered_key, output_path)

        elif mode == "decrypt":
            if not key_path:
                raise ValueError("key_path is required for decrypt mode.")
            with open(file_path, "rb") as f:
                encrypted_bytes = f.read()
            with open(key_path, "rb") as f:
                altered_key = f.read()
            decrypted_bytes = self.decrypt(encrypted_bytes, altered_key)
            self.__write_dec(file_path, decrypted_bytes, output_path)

    def encrypt(
        self, raw_bytes: bytes, encrypt_keyword: Optional[str] = ""
    ) -> Tuple[bytes, bytes]:
        """Return the encrypted bytes object and required key. The key is secondly encrypted with encrypt_keyword.

        Args:
            raw_bytes (bytes): The raw bytes object.
            encrypt_keyword (str): The keyword used to encrypt the key. If not provided, the keyword used in __init__ will be used.

        Returns:
            tuple: (encrypted_bytes, key)
        """
        encrypt_keyword = encrypt_keyword or self.keyword

        key = Fernet.generate_key()

        encrypted_bytes = Fernet(key).encrypt(raw_bytes)
        altered_key = self._modify_key(key, encrypt_keyword, mode="encrypt")

        return encrypted_bytes, altered_key

    def decrypt(
        self,
        encrypted_bytes: bytes,
        altered_key: bytes,
        decrypt_keyword: Optional[str] = "",
    ) -> bytes:
        """Return the decrypted onnx binary.

        Args:
            encrypted_bytes (bytes): The encrypted byte object.
            altered_key (bytes): The key to be used for decryption.
            decrypt_keyword (str): The keyword used to decrypt the key. If not provided, the keyword used in __init__ will be used.

        Returns:
            bytes: The decrypted onnx binary.
        """
        decrypt_keyword = decrypt_keyword or self.keyword
        original_key = self._modify_key(altered_key, decrypt_keyword, mode="decrypt")

        decrypted_bytes = Fernet(original_key).decrypt(encrypted_bytes)

        return decrypted_bytes

    def _modify_key(
        self, key: bytes, keyword: Optional[str] = "", mode: str = "encrypt"
    ) -> bytes:
        """If mode is encrypt, the key is altered by the keyword. If mode is decrypt, return the original key if correct keyword is provided.

        Args:
            key (bytes): The key to be altered.
            keyword (str): The keyword to further enc/decrypt the key. If not provided, the keyword used in __init__ will be used.

        Returns:
            bytes: The altered key.
        """
        keyword = keyword or self.keyword

        random.seed(keyword)
        random_perms = self.__random_permutation(keyword, num_swaps=len(key))
        altered_key = bytearray(key)

        if mode == "encrypt":
            for i, j in random_perms:
                altered_key[i], altered_key[j] = altered_key[j], altered_key[i]
            return bytes(altered_key)
        elif mode == "decrypt":
            for i, j in reversed(random_perms):
                altered_key[j], altered_key[i] = altered_key[i], altered_key[j]
            return bytes(altered_key)
        else:
            raise ValueError(f"mode must be either encrypt or decrypt but got {mode}")

    def __random_permutation(
        self, keyword: str, num_swaps: int = 1000
    ) -> List[Tuple[int, ...]]:
        random.seed(keyword)
        return [
            tuple(random.randint(0, 43) for _ in range(2)) for _ in range(num_swaps)
        ]

    def __write_enc(
        self, file_path: str, content: bytes, key: bytes, output_path: str = ""
    ) -> None:
        base_name = os.path.basename(file_path)
        key_name = base_name + ".key"
        file_name = base_name + ".encrypted"

        if output_path:  # make output_path if not exist
            Path(output_path).mkdir(parents=True, exist_ok=True)
        else:
            output_path = os.path.dirname(file_path)

        with open(os.path.join(output_path, file_name), "wb") as f:
            f.write(content)

        with open(os.path.join(output_path, key_name), "wb") as f:
            f.write(key)

        # print destination
        print(f"Writing encrypted file and key to {output_path}")

    def __write_dec(
        self, file_path: str, decrypted_bytes, output_path: str = ""
    ) -> None:
        output = os.path.splitext(os.path.basename(file_path))[0]

        if output_path != ".":  # make output_path if not exist
            Path(output_path).mkdir(parents=True, exist_ok=True)
        else:
            output_path = os.path.dirname(file_path)

        dest = os.path.join(output_path, output)
        with open(dest, "wb") as f:
            f.write(decrypted_bytes)

        # print destination
        print(f"Writing decrypted file to {os.path.dirname(dest)}")

