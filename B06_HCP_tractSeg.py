import os

data_directory = "/home/test/lmq/data/HCP"

def run_tractseg(subject_dir, data_directory, preprocess_dir, software_dir):
    """Run TractSeg for each subject."""
    subject_path = os.path.join(data_directory, subject_dir)
    DTI_dir = os.path.join(subject_path, "DTI")
    DTI_data = os.path.join(DTI_dir, "data.nii.gz")
    bval = os.path.join(DTI_dir, "bvals")
    bvec = os.path.join(DTI_dir, "bvecs")
    Mask = os.path.join(DTI_dir, "nodif_brain_mask.nii.gz")
    tractseg_dir = os.path.join(subject_path, "tractseg_output")
    os.makedirs(tractseg_dir, exist_ok=True)
    in_file = os.path.join(tractseg_dir, "bundle_segmentations.nii.gz")

    if not os.path.exists(in_file):
        print(f"Running TractSeg for subject: {subject_dir}")
        os.system(f"export CUDA_VISIBLE_DEVICES=0; TractSeg -i {DTI_data} -o {tractseg_dir} --bvals {bval} --bvecs {bvec} --brain_mask {Mask} \
                    --raw_diffusion_input --single_output_file")

        # Resample fiber bundle segmentations
        os.system(f"flirt -ref {DTI_dir}/LowResMask.nii.gz -in {tractseg_dir}/bundle_segmentations.nii.gz \
                    -o {DTI_dir}/LowRes_Fibers.nii.gz -applyisoxfm 3 -interp nearestneighbour")

def main():
    """Main function to process all subjects with TractSeg."""
    preprocess_dir = "/home/test/lmq/Striatal_Subdivision/pipeline"
    software_dir = "/home/test/lmq/Striatal_Subdivision/pipeline/soft_path.sh"

    for subject_dir in os.listdir(data_directory):
        run_tractseg(subject_dir, data_directory, preprocess_dir, software_dir)

if __name__ == "__main__":
    main()
