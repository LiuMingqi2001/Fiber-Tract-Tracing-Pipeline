import os
import subprocess

"""
This script processes anatomical masks for T1-weighted images, including generating
masks for striatum, cortex, and white matter, followed by resampling them to 3mm resolution.

Label values used for segmentation are based on:
https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/AnatomicalROI/FreeSurferColorLUT

Prerequisites:
- Each subject must have a folder named after their ID containing a "T1" subfolder.
- The "T1" subfolder must contain:
    - wmparc.nii.gz (segmentation file).

Outputs:
- Segmented masks (striatum, cortex, white matter) for left, right, and full regions.
- 3mm resampled versions of these masks.
"""

# Define the root directory for HCP data
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
        print(f"Error occurred while running command: {command}\n{e}")


def generate_mask(input_seg, output_mask, lower_thr, upper_thr):
    """
    Generates a binary mask using fslmaths.
    Args:
        input_seg (str): Path to the segmentation file.
        output_mask (str): Path to save the binary mask.
        lower_thr (int): Lower threshold for segmentation.
        upper_thr (int): Upper threshold for segmentation.
    """
    command = f"fslmaths {input_seg} -thr {lower_thr} -uthr {upper_thr} -bin {output_mask}"
    run_command(command)
    print(f"Generated mask: {output_mask}")


def add_masks(mask1, mask2, output_mask):
    """
    Combines two binary masks into one using fslmaths.
    Args:
        mask1 (str): Path to the first mask.
        mask2 (str): Path to the second mask.
        output_mask (str): Path to save the combined mask.
    """
    command = f"fslmaths {mask1} -add {mask2} {output_mask}"
    run_command(command)
    print(f"Combined masks into: {output_mask}")


def resample_to_3mm(input_mask, output_mask):
    """
    Resamples a mask to 3mm resolution using flirt.
    Args:
        input_mask (str): Path to the input mask.
        output_mask (str): Path to save the resampled mask.
    """
    command = f"flirt -ref {input_mask} -in {input_mask} -o {output_mask} -applyisoxfm 3 -interp nearestneighbour"
    run_command(command)
    print(f"Resampled mask to 3mm: {output_mask}")


def process_subject(subject_path):
    """
    Processes a single subject: generates anatomical masks and resamples them.
    Args:
        subject_path (str): Path to the subject's folder.
    """
    t1_dir = os.path.join(subject_path, "T1")
    t1_seg = os.path.join(t1_dir, "wmparc.nii.gz")

    if not os.path.exists(t1_seg):
        print(f"Segmentation file missing for {subject_path}. Skipping.")
        return

    print(f"Processing subject: {os.path.basename(subject_path)}")

    # Striatum masks
    left_striatum = os.path.join(t1_dir, "left_striatum_mask.nii.gz")
    right_striatum = os.path.join(t1_dir, "right_striatum_mask.nii.gz")
    full_striatum = os.path.join(t1_dir, "full_striatum_mask.nii.gz")

    generate_mask(t1_seg, left_striatum, 11, 12)
    generate_mask(t1_seg, right_striatum, 50, 51)
    add_masks(left_striatum, right_striatum, full_striatum)

    # Cortex masks
    left_cortex = os.path.join(t1_dir, "left_cortex_mask.nii.gz")
    right_cortex = os.path.join(t1_dir, "right_cortex_mask.nii.gz")
    full_cortex = os.path.join(t1_dir, "full_cortex_mask.nii.gz")

    generate_mask(t1_seg, left_cortex, 1000, 1035)
    generate_mask(t1_seg, right_cortex, 2000, 2035)
    add_masks(left_cortex, right_cortex, full_cortex)

    # White matter masks
    left_white_known = os.path.join(t1_dir, "left_white_mask_known.nii.gz")
    left_white_unknown = os.path.join(t1_dir, "left_white_mask_unknown.nii.gz")
    left_white = os.path.join(t1_dir, "left_white_mask.nii.gz")
    right_white_known = os.path.join(t1_dir, "right_white_mask_known.nii.gz")
    right_white_unknown = os.path.join(t1_dir, "right_white_mask_unknown.nii.gz")
    right_white = os.path.join(t1_dir, "right_white_mask.nii.gz")
    full_white = os.path.join(t1_dir, "full_white_mask.nii.gz")

    generate_mask(t1_seg, left_white_known, 3001, 3035)
    generate_mask(t1_seg, left_white_unknown, 5001, 5001)
    add_masks(left_white_known, left_white_unknown, left_white)
    generate_mask(t1_seg, right_white_known, 4001, 4035)
    generate_mask(t1_seg, right_white_unknown, 5002, 5002)
    add_masks(right_white_known, right_white_unknown, right_white)
    add_masks(left_white, right_white, full_white)

    # Resample masks to 3mm
    masks_to_resample = [
        (left_striatum, os.path.join(t1_dir, "left_striatum_mask_3mm.nii.gz")),
        (right_striatum, os.path.join(t1_dir, "right_striatum_mask_3mm.nii.gz")),
        (left_cortex, os.path.join(t1_dir, "left_cortex_mask_3mm.nii.gz")),
        (right_cortex, os.path.join(t1_dir, "right_cortex_mask_3mm.nii.gz")),
        (left_white, os.path.join(t1_dir, "left_white_mask_3mm.nii.gz")),
        (right_white, os.path.join(t1_dir, "right_white_mask_3mm.nii.gz"))
    ]

    for input_mask, output_mask in masks_to_resample:
        resample_to_3mm(input_mask, output_mask)


def main():
    """
    Main function to iterate through all subjects in the data directory.
    """
    for subject_dir in os.listdir(DATA_DIRECTORY):
        subject_path = os.path.join(DATA_DIRECTORY, subject_dir)
        if os.path.isdir(subject_path):
            process_subject(subject_path)


if __name__ == "__main__":
    main()
