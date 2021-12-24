<div align="center">

# Encryptor

<img src="icon.png" width=100>

### Simple CLI for Two-Factor Encryption

___

</div>

## Install

```shell
user: ~$ pip install -e .
```

## Usage

The encryption is done in two step.

1. Encryption by AES
2. Encarypt the key with provided password

Thus you need the generated key file and the matching keyword

### Encryption

```console
user: ~$ tfc encrypt [path/to/target/file] -t password -o output_dir
```

1. `-t` is optional. Unless provided, use default password.
2. `-o` is set to the same path to the target file by default.

### Decryption

```console
user: ~$ tfc decrypt [path/to/target/file] -t password -o output_dir -k path/to/key
```

1. `-k` is necessary.
2. `-t` must match with the password used at encryption
