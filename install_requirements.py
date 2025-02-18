import subprocess
import sys

# List of required packages
required_packages = [
    "Pillow",           # Image processing
    "Aes-Everywhere",    # AES encryption
    "roboflow",         # AI model handling
    "opencv-python",    # OpenCV for image processing
    "numpy",             # Numerical operations
    "adafruit-circuitpython-irremote"
]

def install_package(package):
    """Installs a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
        print(f"Successfully installed: {package}")
    except subprocess.CalledProcessError:
        print(f"Failed to install: {package}")

def main():
    print("Installing required Python packages...")

    # Ensure pip is up-to-date
    install_package("pip")

    # Install each required package
    for package in required_packages:
        install_package(package)

    print("Installation complete!")

if __name__ == "__main__":
    main()
