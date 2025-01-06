import os

def generate_seeds(subject_dir, data_directory):
    """Generate seeds for tractography for each subject."""
    subject_path = os.path.join(data_directory, subject_dir)
    T1_dir = os.path.join(subject_path, "T1")
    T1_target = os.path.join(T1_dir, "left_cortex_mask_3mm.nii.gz")
    T1_Seg = os.path.join(T1_dir, "wmparc.nii.gz")

    if os.path.exists(T1_Seg) and not os.path.exists(T1_target):
        print(f"Running seed generation for subject: {subject_dir}")

        # Example of striatum mask generation and resampling
        os.system(f"flirt -ref {T1_dir}/left_striatum_mask.nii.gz -in {T1_dir}/left_striatum_mask.nii.gz \
                        -o {T1_dir}/left_striatum_mask_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour")
        os.system(f"flirt -ref {T1_dir}/right_striatum_mask.nii.gz -in {T1_dir}/right_striatum_mask.nii.gz \
                        -o {T1_dir}/right_striatum_mask_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour")

        # Example of cortex mask generation and resampling
        os.system(f"flirt -ref {T1_dir}/left_cortex_mask.nii.gz -in {T1_dir}/left_cortex_mask.nii.gz \
                        -o {T1_dir}/left_cortex_mask_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour")
        os.system(f"flirt -ref {T1_dir}/right_cortex_mask.nii.gz -in {T1_dir}/right_cortex_mask.nii.gz \
                        -o {T1_dir}/right_cortex_mask_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour")

        # Example of white matter mask generation and resampling
        os.system(f"flirt -ref {T1_dir}/left_white_mask.nii.gz -in {T1_dir}/left_white_mask.nii.gz \
                        -o {T1_dir}/left_white_mask_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour")
        os.system(f"flirt -ref {T1_dir}/right_white_mask.nii.gz -in {T1_dir}/right_white_mask.nii.gz \
                        -o {T1_dir}/right_white_mask_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour")

def main():
    """Main function to iterate through all subjects and generate seeds."""
    data_directory = "/home/test/lmq/data/HCP"

    for subject_dir in os.listdir(data_directory):
        generate_seeds(subject_dir, data_directory)

if __name__ == "__main__":
    main()
