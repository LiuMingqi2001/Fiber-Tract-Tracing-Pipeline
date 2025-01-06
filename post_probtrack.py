import os
import numpy as np
from sklearn.preprocessing import normalize
import scipy.sparse as sparse
from pathlib import Path
import nibabel as nib


def read_coomat(file):
    """
    Reads a coordinate matrix (COO format) from a file.

    Args:
        file (Path): Path to the file.

    Returns:
        tuple: Lists of row indices, column indices, and values.
    """
    with open(file, 'r') as f:
        mat = [line.rstrip().split('  ') for line in f]
    print('Finished loading file:', file)
    i = [int(l[0]) - 1 for l in mat]
    j = [int(l[1]) - 1 for l in mat]
    v = [int(l[2]) for l in mat]
    return i, j, v


def compress_sparse(file):
    """
    Converts a dense matrix to a sparse format and saves it as an NPZ file.

    Args:
        file (Path): Path to the `.dot` file.
    """
    npz_file = file.parent / 'fdt_matrix2.npz'
    if file.exists() and not npz_file.exists():
        i, j, v = read_coomat(file)
        coo_mat = sparse.csr_matrix((v, (i, j)))
        sparse.save_npz(npz_file, coo_mat)
        print(f"Compressed and saved: {npz_file}")
        os.remove(file)
    else:
        print(f"File already processed or does not exist: {file}")


def PostProbtrack(work_dir, hemisphere):
    """
    Converts output files from probtrackx2 to sparse format for a given hemisphere.

    Args:
        work_dir (str): Working directory of the subject.
        hemisphere (str): Hemisphere ('R' or 'L').
    """
    work_dir = Path(work_dir)
    file = work_dir / f'probtrackx_{hemisphere}_omatrix2' / 'fdt_matrix2.dot'
    compress_sparse(file)


def fiber2target(no_diff_path, fiber):
    """
    Maps fiber data to target ROIs.

    Args:
        no_diff_path (Path): Path to the nodif_brain_mask NIfTI file.
        fiber (Path): Path to the fiber bundle segmentations NIfTI file.

    Returns:
        tuple: Sparse matrix of fiber-to-target connections and ROI sizes.
    """
    fiber_img = nib.load(fiber).get_fdata()
    roi_size = np.array([fiber_img[..., i].sum() for i in range(fiber_img.shape[-1])])
    mask_img = nib.load(no_diff_path).get_fdata()
    z, y, x = np.nonzero(mask_img.T)

    if fiber_img.shape[:3] != mask_img.shape:
        fiber_img = reshape_fiber(fiber_img, mask_img)

    mat = fiber_img[x, y, z, :]
    return sparse.csr_matrix(mat), roi_size


def reshape_fiber(fiber_img, mask_img):
    """
    Reshapes the fiber image to match the mask dimensions.

    Args:
        fiber_img (np.ndarray): Fiber image data.
        mask_img (np.ndarray): Mask image data.

    Returns:
        np.ndarray: Reshaped fiber image.
    """
    new_shape = mask_img.shape + (fiber_img.shape[-1],)
    reshaped_img = np.zeros(new_shape)
    common_dims = tuple(min(a, b) for a, b in zip(fiber_img.shape[:3], mask_img.shape))
    reshaped_img[:common_dims[0], :common_dims[1], :common_dims[2], :] = fiber_img[:common_dims[0], :common_dims[1], :common_dims[2], :]
    return reshaped_img


def get_fiber_fingerprint(workpath, hemisphere, recreation=False):
    """
    Generates and normalizes fiber fingerprints for a given hemisphere.

    Args:
        workpath (Path): Working directory of the subject.
        hemisphere (str): Hemisphere ('R' or 'L').
        recreation (bool): Whether to recreate fingerprints if they exist.
    """
    workpath = Path(workpath)
    file = workpath / f'probtrackx_{hemisphere}_omatrix2' / 'fdt_matrix2.npz'
    target_file = workpath / f'probtrackx_{hemisphere}_omatrix2' / f'finger_print_fiber_{hemisphere}.npz'

    if file.exists() and (not target_file.exists() or recreation):
        print(f"Generating fingerprint for {hemisphere} hemisphere from {file}")
        no_diff_path = workpath / 'DTI' / 'LowResMask.nii.gz'
        fiber = workpath / 'DTI' / 'LowRes_Fibers.nii.gz'
        sps_mat = sparse.load_npz(file)
        mat, roi_size = fiber2target(no_diff_path, fiber)
        fp = sps_mat.dot(mat)
        fp = normalize_fingerprint(fp, roi_size)
        sparse.save_npz(target_file, fp)
        print(f"Saved fingerprint for {hemisphere} hemisphere: {target_file}")
    else:
        print(f"Fingerprint already exists or file missing for {hemisphere}: {file}")


def normalize_fingerprint(fp, roi_size):
    """
    Normalizes a fingerprint matrix by ROI sizes.

    Args:
        fp (sparse matrix): Fingerprint matrix.
        roi_size (np.ndarray): Sizes of ROIs.

    Returns:
        sparse matrix: Normalized fingerprint matrix.
    """
    for i in range(len(roi_size)):
        fp[:, i] /= roi_size[i]
    return fp


def main():
    """
    Main function to process all subjects for post-probtrackx analysis.
    """
    data_directory = "/home/test/lmq/data/HCP"

    for subject_dir in os.listdir(data_directory):
        workpath = os.path.join(data_directory, subject_dir)
        if os.path.isdir(workpath):
            for hemisphere in ['R', 'L']:
                PostProbtrack(workpath, hemisphere)
                get_fiber_fingerprint(workpath, hemisphere)


if __name__ == "__main__":
    main()
