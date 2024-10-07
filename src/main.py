from crypto import fetch_crypto_data
from options import fetch_options_data


def main():
    print("\n")
    print("CRYPTO DATA")
    crypto_data = fetch_crypto_data()
    print(crypto_data)
    print("\n")

    print("\n")
    print("OPTIONS DATA")
    options_data = fetch_options_data()
    print(options_data)
    print("\n")


if __name__ == "__main__":
    main()
