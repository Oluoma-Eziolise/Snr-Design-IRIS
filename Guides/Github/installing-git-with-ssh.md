# Setting Up Git Locally with SSH

This guide will walk you through the steps to install Git and configure it to use SSH for secure communication with GitHub. 
You will need to have ssh agent installed to complete this tutorial. If you do not have it installed, follow the instructions 
in [install-ssh](https://github.com/Oluoma-Eziolise/Snr-Design-IRIS/main/Guides/Github/install-ssh.md).

---

## Prerequisites
- A computer with a supported operating system (Windows, macOS, or Linux).
- Access to a terminal (Command Prompt, Git Bash, or Terminal).
- A GitHub account ([Sign up here](https://github.com) if you don't have one).
- SSH agent

---

## Step 1: Install Git
### **On Windows**
1. Download the Git installer from [git-scm.com](https://git-scm.com).
2. Run the installer and follow the prompts:
   - Use the default settings unless you have specific preferences.
   - Ensure "Git Bash Here" is selected to allow easy access to Git Bash.

### **On macOS**
1. Open Terminal.
2. Install Git using Homebrew (if Homebrew is not installed, follow the [Homebrew installation guide](https://brew.sh/)):
   ```bash
   brew install git
   ```

### **On Linux**
1. Open Terminal.
2. Use your package manager to install Git:
   ```bash
   sudo apt update
   sudo apt install git
   ```
   Replace `apt` with your package manager if you're not using Debian/Ubuntu.

---

## Step 2: Generate an SSH Key
SSH keys allow secure access to GitHub without entering your password every time.

1. Open a terminal.
2. Generate a new SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   Replace `your_email@example.com` with the email associated with your GitHub account.
3. When prompted:
   - Press **Enter** to accept the default file location.
   - Optionally, set a passphrase for added security or press **Enter** to skip.

4. Start the SSH agent:
   ```bash
   eval $(ssh-agent -s)
   ```

5. Add your SSH key to the agent:
   ```bash
   ssh-add ~/.ssh/id_ed25519
   ```

---

## Step 3: Add the SSH Key to GitHub
1. Copy your SSH key to the clipboard:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
2. Go to your GitHub account:
   - Navigate to **Settings** > **SSH and GPG keys** > **New SSH key**.
   - Paste the key and give it a title (e.g., "My Laptop").
   - Click **Add SSH Key**.

---

## Step 4: Test the Connection
1. In your terminal, test the SSH connection:
   ```bash
   ssh -T git@github.com
   ```
2. If successful, you will see a message like:
   ```
   Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.
   ```

---

## Step 5: Configure Git Locally
1. Set your global username and email:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your_email@example.com"
   ```

2. Verify your configuration:
   ```bash
   git config --list
   ```

---

## You're All Set!
You have successfully installed Git, configured SSH, and connected it to GitHub. You can now clone repositories, push changes, and collaborate securely using SSH!
