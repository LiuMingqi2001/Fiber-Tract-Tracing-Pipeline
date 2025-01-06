import os
import subprocess

"""
This script performs the following operations:
1. Downsamples T1-weighted raw data from 0.7mm to 3mm resolution.
2. Generates a 3mm low-resolution mask for DTI.

Preconditions:
- Each subject must have a dedicated folder named after their ID.
- Inside each subject folder, there should be two subfolders: "DTI" and "T1".

The "DTI" folder must contain:
    - bvals
    - bvecs
    - data.nii.gz
    - nodif_brain_mask.nii.gz

The "T1" folder must contain:
    - brainmask_fs.nii.gz
    - T1w_acpc_dc_restore_brain.nii.gz
    - wmparc.nii.gz
"""

# Define the root directory for HCP data
DATA_DIRECTORY = "/home/test/lmq/data/HCP"

def run_flirt(input_path, ref_path, output_path, resolution):
    """
    Wrapper function for the FSL flirt command to perform image resampling.
    Args:
        input_path (str): Path to the input NIfTI file.
        ref_path (str): Path to the reference NIfTI file.
        output_path (str): Path to save the output NIfTI file.
        resolution (float): Isotropic resolution for the output.
    """
    try:
        command = [
            "flirt", 
            "-ref", ref_path,
            "-in", input_path,
            "-o", output_path,
            "-applyisoxfm", str(resolution),
            "-interp", "nearestneighbour"
        ]
        subprocess.run(command, check=True)
        print(f"Generated {output_path} at {resolution}mm resolution.")
    except subprocess.CalledProcessError as e:
        print(f"Error running flirt for {output_path}: {e}")

def process_subject(subject_path):
    """
    Process a single subject's data for T1 downsampling and DTI mask generation.
    Args:
        subject_path (str): Path to the subject's folder.
    """
    dti_dir = os.path.join(subject_path, "DTI")
    t1_dir = os.path.join(subject_path, "T1")

    # Check if processing is needed
    if not os.path.exists(os.path.join(dti_dir, "nodif_brain.nii.gz")):
        print(f"Processing subject: {os.path.basename(subject_path)}")
        
        # Define paths for T1 files
        t1_input = os.path.join(t1_dir, "T1w_acpc_dc_restore_brain.nii.gz")
        t1_1mm_output = os.path.join(t1_dir, "T1_1mm.nii.gz")
        t1_3mm_output = os.path.join(t1_dir, "T1_3mm.nii.gz")
        low_res_mask_output = os.path.join(dti_dir, "LowResMask.nii.gz")
        
        # Generate T1 downsampled images
        run_flirt(t1_input, t1_input, t1_1mm_output, 1)
        run_flirt(t1_input, t1_input, t1_3mm_output, 3)
        
        # Generate low-resolution mask
        run_flirt(t1_input, t1_input, low_res_mask_output, 3)
    else:
        print(f"Subject {os.path.basename(subject_path)} already processed. Skipping.")

def main():
    """
    Main function to iterate through all subjects in the data directory.
    """
    for subject_dir in os.listdir(DATA_DIRECTORY):
        subject_path = os.path.join(DATA_DIRECTORY, subject_dir)
        
        # Ensure it is a directory
        if os.path.isdir(subject_path):
            process_subject(subject_path)

if __name__ == "__main__":
    main()
