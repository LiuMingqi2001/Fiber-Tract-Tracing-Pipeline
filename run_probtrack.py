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


def run_probtrack(subject_dir, data_directory, hemisphere):
    """
    Runs ProbtrackX2 for a given subject and specified hemisphere.
    
    Args:
        subject_dir (str): The subject's directory name.
        data_directory (str): The root directory containing all subject data.
        hemisphere (str): Hemisphere to process ('left' or 'right').
    """
    subject_path = os.path.join(data_directory, subject_dir)
    output_dir = os.path.join(subject_path, f"probtrackx_{hemisphere[0].upper()}_omatrix2")
    output_file = os.path.join(output_dir, "fdt_matrix2.dot")

    # Check if processing is already done
    if os.path.exists(output_file):
        print(f"ProbtrackX2 already processed for subject: {subject_dir}, hemisphere: {hemisphere}")
        return

    print(f"Running ProbtrackX2 for subject: {subject_dir}, hemisphere: {hemisphere}")

    # Construct paths for required files
    samples_path = os.path.join(subject_path, "DTI.bedpostX", "merged")
    mask_path = os.path.join(subject_path, "DTI.bedpostX", "nodif_brain_mask")
    seedref_path = os.path.join(subject_path, "T1", "T1w_acpc_dc_restore_brain.nii.gz")
    stop_mask = os.path.join(subject_path, "T1", f"{hemisphere}_cortex_mask_3mm.nii.gz")
    seed_mask = os.path.join(subject_path, "T1", f"{hemisphere}_striatum_mask_3mm.nii.gz")
    target_mask = os.path.join(subject_path, "DTI", "LowResMask.nii.gz")
    white_mask = os.path.join(subject_path, "T1", f"{hemisphere}_white_mask_3mm.nii.gz")

    # Check if all required input files exist
    required_files = [samples_path, mask_path, seedref_path, stop_mask, seed_mask, target_mask, white_mask]
    for file in required_files:
        if not os.path.exists(file):
            print(f"Missing required file for subject {subject_dir}, hemisphere {hemisphere}: {file}")
            return

    # Build and run the ProbtrackX2 command
    command = (
        f"export CUDA_VISIBLE_DEVICES=0; probtrackx2_gpu "
        f"--samples={samples_path} "
        f"--mask={mask_path} "
        f"--seedref={seedref_path} "
        f"-P 5000 --loopcheck --forcedir -c 0.2 --sampvox=2 --randfib=1 "
        f"--stop={stop_mask} --forcefirststep "
        f"-x {seed_mask} "
        f"--omatrix2 --target2={target_mask} "
        f"--wtstop={white_mask} "
        f"--dir={output_dir} --opd -o {hemisphere[0].upper()}"
    )
    run_command(command)


def main():
    """
    Main function to process all subjects with ProbtrackX2.
    """
    for subject_dir in os.listdir(DATA_DIRECTORY):
        subject_path = os.path.join(DATA_DIRECTORY, subject_dir)
        if os.path.isdir(subject_path):
            for hemisphere in ["left", "right"]:
                run_probtrack(subject_dir, DATA_DIRECTORY, hemisphere)


if __name__ == "__main__":
    main()
