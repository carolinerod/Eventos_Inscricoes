import certifi
import os
import shutil

def install_certifi():
    dst = os.path.join(os.environ["SSL_CERT_FILE"] if "SSL_CERT_FILE" in os.environ else "", "cacert.pem")
    shutil.copy(certifi.where(), dst)
    print("Certificados copiados para:", dst)

if __name__ == "__main__":
    install_certifi()
