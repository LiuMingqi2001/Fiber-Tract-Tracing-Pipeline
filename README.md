# Fiber Tract Tracing Pipeline

This repository provides a complete pipeline for processing diffusion MRI (dMRI) data. It traces fiber tracts from the striatum to the cortex, generating 72-dimensional connectivity features for each voxel. The workflow supports dynamic processing for both hemispheres.

---

## Prerequisites

### Software Dependencies

Ensure the following are installed:

- Python 3.6+
- Python Libraries:
  - `nibabel`
  - `numpy`
  - `scipy`
  - `sklearn`
- FSL (accessible via the command line)

Verify FSL installation and access with:
```bash
which fsl
```

---

## Directory Structure

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

---

## Pipeline Workflow

### Step 1: Downsampling and Mask Generation

**Script:** `generate_masks.py`

- Downsamples T1-weighted and DTI data.
- Generates low-resolution masks for brain regions:
  - Striatum
  - Cortex
  - White matter

---

### Step 2: Seed Generation for Fiber Tractography

**Script:** `generate_seeds.py`

- Processes T1 segmentation to produce seed masks for probabilistic tractography.
- Supports dynamic seed generation for left (`L`) and right (`R`) hemispheres.

---

### Step 3: Running BedpostX

**Script:** `run_bedpostx.py`

- Prepares input data and executes BedpostX for modeling fiber orientations.
- Utilizes GPU acceleration where available.

---

### Step 4: Running TractSeg

**Script:** `run_tractseg.py`

- Segments major fiber bundles using TractSeg.
- Downscales the segmented outputs for computational efficiency.

---

### Step 5: Running ProbtrackX2

**Script:** `run_probtrack.py`

- Executes probabilistic tractography to compute connectivity matrices.
- Processes left and right hemispheres dynamically.

---

### Step 6: Post-processing and Feature Extraction

**Script:** `post_probtrack.py`

- Converts connectivity matrices into compressed sparse format.
- Extracts 72-dimensional connectivity fingerprints for each voxel.

---

## Configuration

Update `data_directory` in the scripts to point to the root of your dataset:

```python
data_directory = "/path/to/your/dataset"
```

---

## Execution

Run the pipeline sequentially:

```bash
python generate_masks.py
python generate_seeds.py
python run_bedpostx.py
python run_tractseg.py
python run_probtrack.py
python post_probtrack.py
```

---

## Outputs

- **Processed Masks and Segmentations:**
  - Stored in subject-specific directories.
- **Connectivity Features:**
  - `finger_print_fiber_R.npz`
  - `finger_print_fiber_L.npz`

These files are saved in the `probtrackx_*_omatrix2` subdirectories for each subject.

---

## Customization

- **Hemisphere-specific Parameters:** Dynamically handled via script arguments.
- **Tractography Parameters:** Adjustable in `run_probtrack.py` (e.g., `-P 5000` for the number of streamline samples).

---

## Troubleshooting

- **FSL Accessibility:** Ensure FSL binaries are in your `$PATH`.
- **Input Files:** Verify the directory structure and ensure all required files exist:
  - `bvals`
  - `bvecs`
  - `data.nii.gz`
  - `nodif_brain_mask.nii.gz`
- **Error Logs:** Check terminal outputs for detailed error messages.

---

## References

1. Smith SM, et al. (2004). Advances in functional and structural MR image analysis and implementation as FSL. *NeuroImage*, 23(S1):208-219.
2. [FSL - FMRIB Software Library](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/)
3. Wasserthal J, et al. (2019). TractSeg - Fast and accurate white matter tract segmentation. *NeuroImage*, 183:239-253.

---

## Acknowledgments

We acknowledge the contributions of the neuroimaging community and tools such as FSL, TractSeg, and associated software that make this pipeline possible.

