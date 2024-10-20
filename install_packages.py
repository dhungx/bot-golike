import subprocess


def install_packages():
    packages = ["playwright", "recognizer", "asyncio"]
    try:
        subprocess.run(["pip3", "install", "--upgrade", "pip3"], check=True)
        print("Successfully upgraded pip")
    except subprocess.CalledProcessError as e:
        print(f"Failed to upgrade pip. Error: {e}")
    for package in packages:
        try:
            subprocess.run(["pip3", "install", package], check=True)
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Error: {e}")


if __name__ == "__main__":
    install_packages()
