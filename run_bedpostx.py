import os
import subprocess

# Define the root data directory
DATA_DIRECTORY = "/home/test/lmq/data/HCP"

def run_command(command):
    """
    Executes a shell command and handles errors.
    Args:
        command (str): The shell command to execute.
    """
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}\n{e}")


def run_bedpostx(subject_dir, data_directory, script_path):
    """
    Runs bedpostX for a given subject.

    Args:
        subject_dir (str): The subject's directory name.
        data_directory (str): The root directory containing all subject data.
        script_path (str): Path to the bedpostx_gpu_local.sh script.
    """
    subject_path = os.path.join(data_directory, subject_dir)
    bedpost_dir = os.path.join(subject_path, "DTI.bedpostX")
    os.makedirs(bedpost_dir, exist_ok=True)

    # Copy required files
    try:
        required_files = ["bvals", "bvecs"]
        for file in required_files:
            source_file = os.path.join(subject_path, "DTI", file)
            dest_file = os.path.join(bedpost_dir, file)
            if not os.path.exists(source_file):
                print(f"Required file missing: {source_file}. Skipping subject: {subject_dir}")
                return
            run_command(f"cp {source_file} {dest_file}")

        # Check if bedpostX processing is already completed
        target_file = os.path.join(bedpost_dir, "dyads3.nii.gz")
        if os.path.exists(target_file):
            print(f"BedpostX already processed for subject: {subject_dir}")
            return

        # Run bedpostX processing
        print(f"Running bedpostX for subject: {subject_dir}")
        run_command(f"export CUDA_VISIBLE_DEVICES=0; bash {script_path} {os.path.join(subject_path, 'DTI')}")

    except Exception as e:
        print(f"Error processing subject {subject_dir}: {e}")


def main():
    """
    Main function to iterate over all subjects and run bedpostX.
    """
    
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bedpostx_gpu_local.sh")

    if not os.path.exists(script_path):
        print(f"Script not found: {script_path}. Ensure bedpostx_gpu_local.sh is in the same directory.")
        return

    for subject_dir in os.listdir(DATA_DIRECTORY):
        subject_path = os.path.join(DATA_DIRECTORY, subject_dir)
        if os.path.isdir(subject_path):
            run_bedpostx(subject_dir, DATA_DIRECTORY, script_path)


if __name__ == "__main__":
    main()
