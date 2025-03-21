import os
import subprocess
import shutil

def run_command(command, cwd=None):
    """Run a shell command and handle errors."""
    result = subprocess.run(command, shell=True, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def setup_project(project_name, env_name):
    """Automate the setup of a new project from gro_Grok_Template."""
    print(f"Setting up new project: {project_name}")

    # Step 1: Clone Repository
    print("Cloning repository...")
    clone_url = "https://github.com/gritnz/gro_Grok_Template.git"
    if os.path.exists(project_name):
        print(f"Directory {project_name} already exists, skipping clone.")
    else:
        if not run_command(f"git clone {clone_url} {project_name}"):
            return False

    project_dir = os.path.abspath(project_name)
    print(f"Project directory: {project_dir}")

    # Step 2: Set Up Conda Environment
    print("Setting up Conda environment...")
    if subprocess.run(f"conda env list", shell=True, text=True, capture_output=True).stdout.find(env_name) != -1:
        print(f"Conda environment '{env_name}' already exists, skipping creation.")
    else:
        if not run_command(f"conda create -n {env_name} python=3.11 -y"):
            return False

    # Step 3: Activate Conda Environment (Manual Step for Windows)
    print(f"Conda environment '{env_name}' created or already exists.")
    print("Please ensure the environment is activated:")
    print(f"    conda activate {env_name}")
    print(f"Then, run the remaining steps from the project directory:")
    print(f"    cd {project_dir}")
    print(f"    python -m setup_project  # (if setup_project.py is copied to the project)")
    print("For now, this script will attempt to continue, but ensure the environment is active.")

    # Step 4: Initialize Data
    print("Initializing data...")
    src_dir = os.path.join(project_dir, "template_data")
    dest_dir = os.path.join(project_dir, "data", "historical")
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
    print(f"Copied {src_dir} to {dest_dir}")

    # Step 5: Run Template
    print("Running the template...")
    if not run_command("python src/gro_instructor.py", cwd=project_dir):
        print("Failed to run gro_instructor.py. Ensure the Conda environment is activated.")
        return False

    print(f"Setup complete! Project ready at {project_dir}")
    return True

if __name__ == "__main__":
    project_name = input("Enter project name: ").strip()
    env_name = input("Enter Conda environment name: ").strip()
    setup_project(project_name, env_name)