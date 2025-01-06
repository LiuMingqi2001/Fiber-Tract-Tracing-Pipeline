import os

data_directory = "/home/test/lmq/data/HCP"

def run_probtrack(subject_dir, data_directory, preprocess_dir, hemisphere):
    """Run ProbtrackX2 for each subject with specified hemisphere."""
    subject_path = os.path.join(data_directory, subject_dir)
    output_dir = os.path.join(subject_path, f"probtrackx_{hemisphere[0].upper()}_omatrix2")
    output_file = os.path.join(output_dir, "fdt_matrix2.dot")

    if not os.path.exists(output_file):
        print(f"Running ProbtrackX2 for subject: {subject_dir}, hemisphere: {hemisphere}")
        os.system(f"export CUDA_VISIBLE_DEVICES=0; probtrackx2_gpu --samples={subject_path}/DTI.bedpostX/merged \
                --mask={subject_path}/DTI.bedpostX/nodif_brain_mask \
                --seedref={subject_path}/T1/T1w_acpc_dc_restore_brain.nii.gz \
                -P 5000 --loopcheck --forcedir -c 0.2 --sampvox=2 --randfib=1 \
                --stop={subject_path}/T1/{hemisphere}_cortex_mask_3mm.nii.gz --forcefirststep \
                -x {subject_path}/T1/{hemisphere}_striatum_mask_3mm.nii.gz \
                --omatrix2 --target2={subject_path}/DTI/LowResMask.nii.gz \
                --wtstop={subject_path}/T1/{hemisphere}_white_mask_3mm.nii.gz \
                --dir={output_dir} --opd -o {hemisphere[0].upper()}")
    else:
        print(f"ProbtrackX2 already processed for subject: {subject_dir}, hemisphere: {hemisphere}")

def main():
    """Main function to process all subjects with ProbtrackX2."""
    preprocess_dir = "/home/test/lmq/Striatal_Subdivision/pipeline"

    for subject_dir in os.listdir(data_directory):
        for hemisphere in ["left", "right"]:
            run_probtrack(subject_dir, data_directory, preprocess_dir, hemisphere)

if __name__ == "__main__":
    main()
