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


def run_tractseg(subject_dir, data_directory):
    """
    Runs TractSeg for a given subject.
    
    Args:
        subject_dir (str): The subject's directory name.
        data_directory (str): The root directory containing all subject data.
    """
    subject_path = os.path.join(data_directory, subject_dir)
    dti_dir = os.path.join(subject_path, "DTI")
    dti_data = os.path.join(dti_dir, "data.nii.gz")
    bval = os.path.join(dti_dir, "bvals")
    bvec = os.path.join(dti_dir, "bvecs")
    mask = os.path.join(dti_dir, "nodif_brain_mask.nii.gz")
    tractseg_dir = os.path.join(subject_path, "tractseg_output")
    os.makedirs(tractseg_dir, exist_ok=True)
    output_file = os.path.join(tractseg_dir, "bundle_segmentations.nii.gz")

    # Check if processing is already done
    if os.path.exists(output_file):
        print(f"TractSeg already processed for subject: {subject_dir}")
        return

    # Check if required input files exist
    required_files = [dti_data, bval, bvec, mask]
    for file in required_files:
        if not os.path.exists(file):
            print(f"Missing required file for subject {subject_dir}: {file}")
            return

    print(f"Running TractSeg for subject: {subject_dir}")

    # Run TractSeg
    tractseg_command = (
        f"export CUDA_VISIBLE_DEVICES=0; "
        f"TractSeg -i {dti_data} -o {tractseg_dir} --bvals {bval} --bvecs {bvec} "
        f"--brain_mask {mask} --raw_diffusion_input --single_output_file"
    )
    run_command(tractseg_command)

    # Resample fiber bundle segmentations
    low_res_mask = os.path.join(dti_dir, "LowResMask.nii.gz")
    low_res_output = os.path.join(dti_dir, "LowRes_Fibers.nii.gz")
    if os.path.exists(low_res_mask):
        resample_command = (
            f"flirt -ref {low_res_mask} -in {output_file} "
            f"-o {low_res_output} -applyisoxfm 3 -interp nearestneighbour"
        )
        run_command(resample_command)
    else:
        print(f"LowResMask.nii.gz not found for subject: {subject_dir}")


def main():
    """
    Main function to process all subjects with TractSeg.
    """
    for subject_dir in os.listdir(DATA_DIRECTORY):
        subject_path = os.path.join(DATA_DIRECTORY, subject_dir)
        if os.path.isdir(subject_path):
            run_tractseg(subject_dir, DATA_DIRECTORY)


if __name__ == "__main__":
    main()
