# README for Fiber Tract Tracing Pipeline

This pipeline processes diffusion MRI data to perform fiber tract tracing from the striatum to the cortex and generates 72-dimensional fiber tract connectivity features for each voxel. The workflow is modular and handles both hemispheres dynamically.

## Prerequisites

### Software Dependencies

- Python 3.6+
- `nibabel`
- `numpy`
- `scipy`
- `sklearn`
- FSL (installed and accessible via command line)

### Directory Structure

Ensure the data is organized as follows:

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
- Generates low-resolution masks for various brain regions (striatum, cortex, white matter).

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

All scripts are set up to process multiple subjects automatically. Modify `data_directory` to point to your dataset root.

## Running the Pipeline

Run each script in sequence to complete the pipeline:

```bash
python generate_masks.py
python generate_seeds.py
python run_bedpostx.py
python run_tractseg.py
python run_probtrack.py
python post_probtrack.py
```

## Output

- Processed masks and segmentation results are stored in the respective subject folders.
- Connectivity fingerprints for each hemisphere are saved as `finger_print_fiber_R.npz` and `finger_print_fiber_L.npz`.

## Customization

- Parameters for hemisphere-specific processing (e.g., `R` and `L`) are passed dynamically to avoid code duplication.
- Adjust tractography parameters (e.g., `-P 5000`) directly in `run_probtrack.py` if needed.

## Troubleshooting

- Ensure FSL binaries are accessible via `$PATH`.
- Verify input files and directory structure before running the scripts.
- Check log outputs for errors during intermediate steps.

