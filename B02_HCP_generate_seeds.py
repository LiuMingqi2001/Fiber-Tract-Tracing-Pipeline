import os

data_directory = "/home/test/lmq/data/HCP"

for subject_dir in os.listdir(data_directory):
    # Prepare working directory
    subject_path = os.path.join(data_directory, subject_dir)
    T1_dir = os.path.join(subject_path, "T1")
    # T1_target = os.path.join(T1_dir, "full_cortex_mask.nii.gz")
    T1_target = os.path.join(T1_dir, "left_cortex_mask_3mm.nii.gz")
    # T1_Seg = os.path.join(T1_dir, "aparc.a2009s+aseg.nii.gz")
    T1_Seg = os.path.join(T1_dir, "wmparc.nii.gz")

    if os.path.exists(T1_Seg):
        if not os.path.exists(T1_target):
            print("----------Running Generate Seeds for {}----------".format(subject_dir))
            # Generate striatum masks (left, right, full)
            os.system(f"fslmaths {T1_Seg} -thr 11 -uthr 12 -bin {T1_dir}/left_striatum_mask.nii.gz")
            os.system(f"fslmaths {T1_Seg} -thr 50 -uthr 51 -bin {T1_dir}/right_striatum_mask.nii.gz")
            os.system(f"fslmaths {T1_dir}/left_striatum_mask.nii.gz -add {T1_dir}/right_striatum_mask.nii.gz {T1_dir}/full_striatum_mask.nii.gz")
            
            # Generate cortex masks (left, right, full)
            os.system(f"fslmaths {T1_Seg} -thr 1000 -uthr 1035 -bin {T1_dir}/left_cortex_mask.nii.gz")
            os.system(f"fslmaths {T1_Seg} -thr 2000 -uthr 2035 -bin {T1_dir}/right_cortex_mask.nii.gz")
            os.system(f"fslmaths {T1_dir}/left_cortex_mask.nii.gz -add {T1_dir}/right_cortex_mask.nii.gz {T1_dir}/full_cortex_mask.nii.gz")
            
            # Generate white matter masks (left, right, full)
            os.system(f"fslmaths {T1_Seg} -thr 3001 -uthr 3035 -bin {T1_dir}/left_white_mask_known.nii.gz")
            os.system(f"fslmaths {T1_Seg} -thr 5001 -uthr 5001 -bin {T1_dir}/left_white_mask_unknown.nii.gz")
            os.system(f"fslmaths {T1_dir}/left_white_mask_known.nii.gz -add {T1_dir}/left_white_mask_unknown.nii.gz {T1_dir}/left_white_mask.nii.gz")
            os.system(f"fslmaths {T1_Seg} -thr 4001 -uthr 4035 -bin {T1_dir}/right_white_mask_known.nii.gz")
            os.system(f"fslmaths {T1_Seg} -thr 5002 -uthr 5002 -bin {T1_dir}/right_white_mask_unknown.nii.gz")
            os.system(f"fslmaths {T1_dir}/right_white_mask_known.nii.gz -add {T1_dir}/right_white_mask_unknown.nii.gz {T1_dir}/right_white_mask.nii.gz")
            os.system(f"fslmaths {T1_dir}/left_white_mask.nii.gz -add {T1_dir}/right_white_mask.nii.gz {T1_dir}/full_white_mask.nii.gz")
            
            # Resample masks to 3mm resolution
            os.system('flirt -ref {}/left_striatum_mask.nii.gz -in {}/left_striatum_mask.nii.gz \
                            -o {}/left_striatum_mask_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour'.format(T1_dir, T1_dir, T1_dir))
            os.system('flirt -ref {}/right_striatum_mask.nii.gz -in {}/right_striatum_mask.nii.gz \
                            -o {}/right_striatum_mask_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour'.format(T1_dir, T1_dir, T1_dir))
            os.system('flirt -ref {}/left_cortex_mask.nii.gz -in {}/left_cortex_mask.nii.gz \
                            -o {}/left_cortex_mask_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour'.format(T1_dir, T1_dir, T1_dir))
            os.system('flirt -ref {}/right_cortex_mask.nii.gz -in {}/right_cortex_mask.nii.gz \
                            -o {}/right_cortex_mask_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour'.format(T1_dir, T1_dir, T1_dir))
            os.system('flirt -ref {}/left_white_mask.nii.gz -in {}/left_white_mask.nii.gz \
                            -o {}/left_white_mask_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour'.format(T1_dir, T1_dir, T1_dir))
            os.system('flirt -ref {}/right_white_mask.nii.gz -in {}/right_white_mask.nii.gz \
                            -o {}/right_white_mask_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour'.format(T1_dir, T1_dir, T1_dir))
