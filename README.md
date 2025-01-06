# Fiber Tract Tracing Pipeline

This repository contains a pipeline for processing diffusion MRI (dMRI) data. It performs fiber tract tracing from the striatum to the cortex, generating 72-dimensional connectivity features for each voxel. The modular workflow supports both hemispheres dynamically.

## Prerequisites

### Software Dependencies

- Python 3.6+
- `nibabel`
- `numpy`
- `scipy`
- `sklearn`
- FSL (installed and accessible via the command line)

### Directory Structure

Organize your data as follows:

```
/home/test/lmq/data/HCP/
    ├── Subject1/
    │   ├── DTI/
    │   │   ├── bvals
    │   │   ├── bvecs
    │   │   ├── data.nii.gz
    │   │   ├── nodif_brain_mask.nii.gz
    │   ├── T1/
    │       ├── T1w_acpc_dc_restore_brain.nii.gz
    │       ├── wmparc.nii.gz
    ├── Subject2/
    ...
```

## Pipeline Steps

### 1. Downsampling and Mask Generation

**Script:** `generate_masks.py`

- Downsamples T1 and DTI data.
- Generates low-resolution masks for various brain regions (e.g., striatum, cortex, white matter).

### 2. Seed Generation for Fiber Tractography

**Script:** `generate_seeds.py`

- Processes T1 segmentation to produce seed masks for both hemispheres.

### 3. Running BedpostX

**Script:** `run_bedpostx.py`

- Prepares data and runs BedpostX to model fiber orientations.

### 4. Running TractSeg

**Script:** `run_tractseg.py`

- Segments major fiber bundles using TractSeg and downscales the outputs.

### 5. Running ProbtrackX2

**Script:** `run_probtrack.py`

- Executes probabilistic tractography to compute connectivity matrices for left and right hemispheres.

### 6. Post-processing and Feature Extraction

**Script:** `post_probtrack.py`

- Converts connectivity matrices into sparse format.
- Computes 72-dimensional connectivity fingerprints for each voxel.

## Configuration

Modify `data_directory` in the scripts to point to the root of your dataset. All scripts are designed to process multiple subjects automatically.

## Running the Pipeline

Run the scripts in sequence:

```bash
python generate_masks.py
python generate_seeds.py
python run_bedpostx.py
python run_tractseg.py
python run_probtrack.py
python post_probtrack.py
```

## Outputs

- **Processed Masks and Segmentations:** Stored in subject-specific folders.
- **Connectivity Features:** Saved as `finger_print_fiber_R.npz` and `finger_print_fiber_L.npz` for each hemisphere.

## Customization

- Hemisphere-specific parameters (e.g., `R` and `L`) are passed dynamically.
- Adjust tractography settings (e.g., `-P 5000`) in `run_probtrack.py`.

## Troubleshooting

- Ensure FSL binaries are accessible in `$PATH`.
- Verify the input directory structure and file integrity.
- Check log outputs for errors during execution.

## References

- Smith SM, et al. (2004). Advances in functional and structural MR image analysis and implementation as FSL. *NeuroImage*, 23(S1):208-219.
- [FSL - FMRIB Software Library](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/)

## Acknowledgments

We appreciate the contributions of the neuroimaging community and tools like FSL and TractSeg.
