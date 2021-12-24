from core import TwoFactorCryptor
import argparse


def main():
    parser = argparse.ArgumentParser(description="Two Factor Cryptor")
    parser.add_argument("mode", choices=["encrypt", "decrypt"])
    parser.add_argument("file_path", type=str)
    parser.add_argument("-k", "--key", type=str, help="The key to decrypt the file.")
    parser.add_argument(
        "-t",
        "--two_factor_keyword",
        type=str,
        help="The keyword used to encrypt the key.",
        default="YourSecretKey",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="The output file path.", default="."
    )

    args = parser.parse_args()

    model = TwoFactorCryptor(args.two_factor_keyword)
    if args.output:
        model.output_path = args.output

    if args.mode == "encrypt":
        model(args.file_path, args.output, mode="encrypt")
    elif args.mode == "decrypt":
        model(args.file_path, args.key, mode="decrypt")


if __name__ == "__main__":
    main()
