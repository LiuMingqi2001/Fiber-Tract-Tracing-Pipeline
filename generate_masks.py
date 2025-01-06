import os

"""
在这个文件中，我们会执行以下操作：
1、将T1原始数据从0.7mm降采样到3mm
2、为DTI生成3mm低分辨率掩膜

运行这段代码需要为每个被试单独准备一个以其名字命名的文件夹。
文件夹内设置两个文件夹"DTI"和"T1"
"DTI"文件夹需要有bvals, bvecs, data.nii.gz, nodif_brain_mask.nii.gz
"T1"文件夹需要有brainmask_fs.nii.gz, T1w_acpc_dc_restore_brain.nii.gz, wmparc.nii.gz
"""


data_directory="/home/test/lmq/data/HCP"

for subject_dir in os.listdir(data_directory):
    subject_path = os.path.join(data_directory, subject_dir)
    DTI_dir = os.path.join(subject_path, "DTI")
    T1_dir = os.path.join(subject_path, "T1")
    if not os.path.exists(os.path.join(DTI_dir, "nodif_brain.nii.gz")):
        print(f'Running T1 and DTI miniprocess for subject: {subject_dir}')
        # 生成T1_1mm数据
        os.system('flirt -ref {}/T1w_acpc_dc_restore_brain.nii.gz -in {}/T1w_acpc_dc_restore_brain.nii.gz \
                    -o {}/T1_1mm.nii.gz -applyisoxfm 1 -interp nearestneighbour'.format(T1_dir, T1_dir, T1_dir))
        # 生成T1_3mm数据
        os.system('flirt -ref {}/T1w_acpc_dc_restore_brain.nii.gz -in {}/T1w_acpc_dc_restore_brain.nii.gz \
                            -o {}/T1_3mm.nii.gz -applyisoxfm 3 -interp nearestneighbour'.format(T1_dir, T1_dir, T1_dir))
        # 生成低分辨率掩膜
        target_format = os.path.join(DTI_dir, "LowResMask.nii.gz")
        os.system('flirt -ref {}/T1w_acpc_dc_restore_brain.nii.gz -in {}/T1w_acpc_dc_restore_brain.nii.gz \
                    -o {} -applyisoxfm 3 -interp nearestneighbour'.format(T1_dir, T1_dir, target_format))
    # print(f'Running DTI postprocess for subject: {subject_path}')
    
    # os.system("fslroi {}/data.nii {}/nodif 0 1".format(DTI_dir, DTI_dir))
    # os.system("bet {}/nodif.nii.gz {}/nodif_brain -m".format(DTI_dir, DTI_dir))
    # os.system(f"dtifit -k {DTI_dir}/data.nii -m {DTI_dir}/nodif_brain_mask.nii.gz -r {DTI_dir}/bvecs -b {DTI_dir}/bvals -o {DTI_dir}/dti")
