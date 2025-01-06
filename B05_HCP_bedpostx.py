import os

data_directory = "/home/test/lmq/data/HCP"

def run_bedpostx(subject_dir, data_directory, preprocess_dir):
    """Run bedpostX for each subject."""
    subject_path = os.path.join(data_directory, subject_dir)
    bedpost_dir = os.path.join(subject_path, "DTI.bedpostX/")
    os.makedirs(bedpost_dir, exist_ok=True)

    # Copy required files
    os.system(f"cp {subject_path}/DTI/bvals {bedpost_dir}")
    os.system(f"cp {subject_path}/DTI/bvecs {bedpost_dir}")

    # Check if processing is already done
    target = os.path.join(bedpost_dir, "dyads3.nii.gz")
    if os.path.exists(target):
        print(f"BedpostX already processed for subject: {subject_dir}")
        return

    print(f"Running bedpostX for subject: {subject_dir}")
    os.system(f"export CUDA_VISIBLE_DEVICES=0; bash {preprocess_dir}/bedpostx_gpu_local.sh {subject_path}/DTI")

def main():
    """Main function to process all subjects."""
    preprocess_dir = "/home/test/lmq/Striatal_Subdivision/pipeline"

    for subject_dir in os.listdir(data_directory):
        run_bedpostx(subject_dir, data_directory, preprocess_dir)

if __name__ == "__main__":
    main()
