import os
import numpy as np
from sklearn.preprocessing import normalize
import scipy.sparse as sparse
from pathlib import Path
import nibabel as nib

def read_coomat(file):
    with open(str(file), 'r') as f:
        mat = [line.rstrip().split('  ') for line in f]
    print('Finished loading file')
    i = [int(l[0]) - 1 for l in mat]
    j = [int(l[1]) - 1 for l in mat]
    v = [int(l[2]) for l in mat]
    return i, j, v

def compress_sparse(file):
    if file.exists() and not (file.parent / 'fdt_matrix2.npz').exists():
        i, j, v = read_coomat(file)
        coo_mat = sparse.csr_matrix((v, (i, j)))
        sparse.save_npz(str(file.parent / 'fdt_matrix2'), coo_mat)
        print(f"Compressed and saved: {file}")
        os.remove(str(file))
    else:
        print(f"File already processed or does not exist: {file}")

def PostProbtrack(work_dir, hemisphere):
    """Convert output files from probtrackx2 to sparse format for a given hemisphere."""
    work_dir = Path(work_dir)
    file = work_dir / f'probtrackx_{hemisphere}_omatrix2' / 'fdt_matrix2.dot'
    compress_sparse(file)

def fiber2target(no_diff_path, fiber):
    fiber_img = nib.load(str(fiber)).get_fdata()
    roi_size = np.array([fiber_img[..., i].sum() for i in range(72)])
    mask_img = nib.load(str(no_diff_path)).get_fdata()
    z, y, x = np.nonzero(mask_img.T)

    if fiber_img.shape[:3] != mask_img.shape:
        fiber_img = reshape_fiber(fiber_img, mask_img)

    mat = fiber_img[x, y, z, :]
    return sparse.csr_matrix(mat), roi_size

def reshape_fiber(fiber_img, mask_img):
    new_shape = mask_img.shape + (fiber_img.shape[-1],)
    reshaped_img = np.zeros(new_shape)
    common_dims = tuple(min(a, b) for a, b in zip(fiber_img.shape[:3], mask_img.shape))
    reshaped_img[:common_dims[0], :common_dims[1], :common_dims[2], :] = fiber_img[:common_dims[0], :common_dims[1], :common_dims[2], :]
    return reshaped_img

def get_fiber_fingerprint(workpath, hemisphere, recreation=False):
    workpath = Path(workpath)
    file = workpath / f'probtrackx_{hemisphere}_omatrix2' / 'fdt_matrix2.npz'
    target_file = f'finger_print_fiber_{hemisphere}.npz'

    if file.exists() and (not (file.parent / target_file).exists() or recreation):
        print(f"Generating fingerprint for {hemisphere} hemisphere from {file}")
        no_diff_path = workpath / 'DTI' / 'LowResMask.nii.gz'
        fiber = workpath / 'DTI' / 'LowRes_Fibers.nii.gz'
        sps_mat = sparse.load_npz(str(file))
        mat, roi_size = fiber2target(no_diff_path, fiber)
        fp = sps_mat.dot(mat)
        fp = normalize_fingerprint(fp, roi_size)
        sparse.save_npz(str(file.parent / target_file), fp)
    else:
        print(f"Fingerprint already exists or file missing for {hemisphere}: {file}")

def normalize_fingerprint(fp, roi_size):
    for i in range(len(roi_size)):
        fp[:, i] /= roi_size[i]
    return fp

def main():
    """Main function to process all subjects for post-probtrackx analysis."""
    data_directory = "/home/test/lmq/data/HCP"

    for subject_dir in os.listdir(data_directory):
        workpath = os.path.join(data_directory, subject_dir)
        for hemisphere in ['R', 'L']:
            PostProbtrack(workpath, hemisphere)
            get_fiber_fingerprint(workpath, hemisphere)

if __name__ == "__main__":
    main()
