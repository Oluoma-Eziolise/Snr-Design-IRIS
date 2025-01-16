# How to Install SSH

This guide provides step-by-step instructions to install and set up SSH (Secure Shell) on your system, enabling secure communication with remote servers or services like GitHub.

---

## What is SSH?
SSH (Secure Shell) is a protocol used to securely access and manage remote machines or services over a network. It encrypts the data transfer to ensure secure communication.

---

## Step 1: Check if SSH is Already Installed

### **On Windows**
1. Open PowerShell or Command Prompt.
2. Type:
   ```bash
   ssh -V
   ```
3. If SSH is installed, you will see the version information. If not, proceed to the installation steps below.

### **On macOS**
1. Open Terminal.
2. Type:
   ```bash
   ssh -V
   ```
3. SSH is typically pre-installed on macOS. If it is missing, follow the installation instructions for macOS.

### **On Linux**
1. Open Terminal.
2. Type:
   ```bash
   ssh -V
   ```
3. Most Linux distributions come with SSH pre-installed. If not, proceed with the installation.

---

## Step 2: Install SSH

### **On Windows**
1. Open your settings
2. Navigate to "System > Optional Features"
3. Search for "OpenSSH Client"
4. Select "Install"
5. Verify the installation by running in your terminal:
   ```bash
   ssh -V
   ```

### **On macOS**
1. Open Terminal.
2. If SSH is not available, install it using Homebrew (install Homebrew first if not already installed):
   ```bash
   brew install openssh
   ```
3. Verify the installation:
   ```bash
   ssh -V
   ```

### **On Linux**
1. Open Terminal.
2. Use the package manager for your distribution to install SSH:
   - For Debian/Ubuntu:
     ```bash
     sudo apt update
     sudo apt install openssh-client
     ```
   - For Fedora:
     ```bash
     sudo dnf install openssh-clients
     ```
   - For Arch Linux:
     ```bash
     sudo pacman -S openssh
     ```
3. Verify the installation:
   ```bash
   ssh -V
   ```
   
---

## Additional Tips
- To learn more about using SSH, type:
  ```bash
  man ssh
  ```
- Now you are ready to generate SSH keys for passwordless authentication ([installing git with ssh](https://github.com/Oluoma-Eziolise/Snr-Design-IRIS/blob/main/Guides/Github/installing-git-with-ssh.md)).

