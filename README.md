# TCGA Breast Cancer Hypermethylation Analysis

## Overview

**Research Paper**: [Download / View Full Paper](https://docs.google.com/document/d/1946EeG09cPgDRlKi_8D6Ld2tORhn3289/edit?usp=sharing&ouid=100564994122883841903&rtpof=true&sd=true) 

This project investigates **DNA hypermethylation patterns** in **metastatic breast cancer**, focusing on **Triple-Negative Breast Cancer (TNBC)** patients using data from **The Cancer Genome Atlas (TCGA)**. It combines epigenetic profiling, data mining, and machine learning to identify CpG sites that are differentially methylated in metastatic tumors and uses those to build a predictive model for metastatic status.

---

## Objectives

- Identify CpG sites hypermethylated in metastatic (M1) vs. non-metastatic (M0) breast cancer patients.
- Map CpG sites to corresponding genes as potential biomarkers or therapeutic targets.
- Develop a machine learning model (SVM) to predict metastatic status from methylation data.
- Compare results with existing literature to validate findings.

---

## Tools & Technologies

- **Python**: Data mining, modeling (`pandas`, `scikit-learn`)
- **MySQL**: Data storage and efficient querying for millions of methylation records
- **Visualization**: Heatmaps, line charts for data interpretation
- **Data Sources**: TCGA BRCA clinical + Illumina 450K DNA methylation arrays
- **Machine Learning**: Support Vector Machine classifier for metastasis prediction

---

## Data Sources

- **TCGA BRCA Clinical Data**:  
  Clinical information such as age, tumor stage, metastasis status (M0, M1, MX), hormone receptor status, etc.
- **Illumina HumanMethylation450K Arrays**:  
  Genome-wide methylation levels at ~450,000 CpG sites per patient.
- **GDC Data Portal**:  
  [https://portal.gdc.cancer.gov/](https://portal.gdc.cancer.gov/)

---

## Methodology

1. **Data Collection**:
   - Extracted patient IDs from `nationwidechildrens.org_clinical_patient_brca.txt`.
   - Downloaded methylation profiles for 86 patients (14 M1, 72 M0).
   - Loaded ~38.7 million methylation records into a SQL database.

2. **Filtering Criteria**:
   - Selected CpG sites with:
     - β > 0.4 in **all M1 patients**
     - β < 0.4 in **all M0 patients**
   - Result: **193,305** CpG sites identified as differentially methylated.

3. **Data Reduction**:
   - Removed sites with missing values in any M1 patient.
   - Final filtered matrix: **~35,000 sites**.
   - Top **50** sites analyzed visually; top **10** ranked by methylation intensity.

4. **Gene Mapping**:
   - Annotated CpG sites using the 450K annotation file.
   - Identified **9 genes** corresponding to the top 10 hypermethylated sites.

5. **Machine Learning**:
   - SVM model trained on methylation profiles of 11 M1 and 9 M0 patients.
   - Tested on remaining 3 M1 and 2 M0 patients.
   - Achieved:
     - Accuracy: **1.0**
     - Precision: **1.0**
     - Recall: **1.0**
     - F1 Score: **1.0**

6. **Validation**:
   - Literature review to compare discovered genes with prior TNBC methylation studies.

---

## Key Findings

- **193K CpG sites** show hypermethylation in metastatic samples.
- Methylation heatmaps clearly distinguish M1 from M0 patients.
- **Top 10 CpG sites** with strong methylation contrast may serve as biomarkers.
- **SVM classifier** shows perfect performance on available data (limited sample size).
- **Genes such as ARID5A, SORBS1, CUX1, DYSF, TRERF1** were identified as potentially important.

---

## Research Insights

- Methylation at specific CpG sites may drive or signal the onset of metastasis in TNBC.
- Computational limitations restricted full-scale analysis; filtering and reduction were critical.
- The project highlights the **feasibility of data-driven metastasis prediction** using epigenetic features.

---

## Data Availability

Due to GitHub's file size limits, the following large files are **not included** in this repository:

### Excluded Files:
- Raw methylation arrays (~450K sites × 1097 patients)
- MySQL database dump of 38.7M records
- Pivoted methylation matrix (193K sites × 86 patients)
- Filtered datasets used for training/testing ML models

### How to Access or Reproduce:
- Download methylation data from the [GDC Data Portal](https://portal.gdc.cancer.gov/).
- Use provided scripts in the `/data_collection` or `/scripts` directory (if included) to regenerate the datasets.
- For academic use, contact the repository owner to request the processed datasets privately.

---

## Limitations

- Limited number of metastatic TNBC samples (2 M1-TNBC patients) restricts generalizability.
- Computational constraints prevented full dataset inclusion.
- Perfect ML performance on small test set may reflect overfitting—further validation required.

---

## Future Work

- Scale to full TCGA BRCA dataset using high-performance computing.
- Test model on external validation cohorts.
- Explore gene expression integration with methylation data for multi-omic predictions.

---

## License

This research is provided for academic and educational use. Please cite the TCGA and GDC Data Portal appropriately when using their data.

