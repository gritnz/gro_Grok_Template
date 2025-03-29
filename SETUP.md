# Project Setup Guide

Welcome to `gro_Grok_Template`! This guide will help you set up a new project cloned from `https://github.com/gritnz/gro_Grok_Template.git`. We will get you up and running with your new project in a few simple steps. We’ll use Grok 3, an AI assistant from xAI, to guide you through the process interactively.

## Getting Started
- **Install Git**: Download and install Git from [git-scm.com](https://git-scm.com/). Follow the installation instructions for your operating system (Windows, macOS, or Linux).
- **Learn Git**: If you’re new to Git, there are plenty of tutorials available. Check out the [Git Handbook](https://guides.github.com/introduction/git-handbook/) or ask an AI assistant like Grok or ChatGPT for help with commands like `git clone`.
- **Install Conda**: We’ll use Conda to manage our Python environment. Download and install Miniconda from [docs.conda.io](https://docs.conda.io/en/latest/miniconda.html). Follow the installation instructions for your operating system.

## Step 1: Clone the Project
- **GitHub Template Option (Recommended)**: On the GitHub page (`https://github.com/gritnz/gro_Grok_Template.git`), you may see a green “Use this template” button. This creates a new repository based on the template, which sets up a clean Git history and makes it easier to manage your project on GitHub.
  - If the button isn’t visible, make sure you are logged in, select "settings" on your tool bar, select "Template Repository", go back to the main gro_Grok_Template, "Use this template" button should now be visible.
  - Dropdown and select "Create new repository", enter the repository name of your choosing (e.g., `gro_Sandbox`).
  - After creating the repository, clone it to your local machine:

- **Direct Cloning (Alternative)**: If you prefer not to use the template option, you can clone the repository directly:


## Step 2: Run the Initial Setup Script
- After cloning, run the setup script to prepare your project:

- This script will update key files, including `state.json`, with your project’s name (e.g., `gro_Sandbox`).

## Step 3: Set Up Your IDE
- **Install VS Code**: We recommend Visual Studio Code (VS Code) as your IDE. Download it from [code.visualstudio.com](https://code.visualstudio.com/).
- Open VS Code and install the Python extension:
- Go to the Extensions view (`Ctrl+Shift+X`).
- Search for “Python” and install the official Python extension by Microsoft.
- Open your project folder in VS Code:
- Go to `File > Open Folder` (or press `Ctrl+K Ctrl+O`).
- Navigate to your project folder (e.g., `F:\<project-name>`), select it, and click `Open`.

## Step 4: Get Help from Grok 3
- Grok 3 will guide you through the rest of the setup process.
- Open the file `template_data/state.json` in VS Code (you’ll find it in the `template_data/` folder).
- Copy the entire content of the file (`Ctrl+A` to select all, `Ctrl+C` to copy).
- Go to the xAI website to access Grok 3: [x.ai](https://x.ai/).
- Start a new chat with Grok 3 and paste the content of `state.json` into the chat input (`Ctrl+V` to paste).
- Grok 3 will greet you and guide you through the remaining steps, including setting up your Conda environment, updating files, and testing the project.
- **Note**: If you encounter any issues, you can report them by opening an issue on the GitHub repository at `https://github.com/gritnz/gro_Grok_Template.git`.