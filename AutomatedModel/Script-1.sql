SELECT f.file_name FileName FROM tnbc.case_file_id f 
inner join tnbc.clinical_patient_brca p on f.bcr_patient_uuid = p.bcr_patient_uuid 
WHERE p.ajcc_metastasis_pathologic_pm = 'M1' 
or (p.ajcc_metastasis_pathologic_pm = 'M0' and p.er_status_by_ihc = 'Negative' AND p.pr_status_by_ihc = 'Negative' AND p.her2_status_by_ihc = 'Negative')

SELECT f.file_name, p.ajcc_metastasis_pathologic_pm, p.ajcc_pathologic_tumor_stage, 
    p.anatomic_neoplasm_subdivision, p.metastasis_site, 
    CONCAT(p.ajcc_metastasis_pathologic_pm, '_', p.bcr_patient_uuid)
FROM tnbc.case_file_id f 
INNER JOIN tnbc.clinical_patient_brca p 
ON f.bcr_patient_uuid = p.bcr_patient_uuid 
WHERE p.ajcc_metastasis_pathologic_pm = 'M1' 
    OR (p.ajcc_metastasis_pathologic_pm = 'M0' 
        AND p.er_status_by_ihc = 'Negative' 
        AND p.pr_status_by_ihc = 'Negative' 
        AND p.her2_status_by_ihc = 'Negative')

        
SELECT CONCAT(p.ajcc_metastasis_pathologic_pm, '_', p.bcr_patient_uuid)
FROM tnbc.case_file_id f
INNER JOIN tnbc.clinical_patient_brca p ON f.bcr_patient_uuid = p.bcr_patient_uuid

SELECT * FROM tnbc.clinical_patient_brca cpb

SELECT * FROM tnbc.case_file_id cfi 

SELECT CONCAT(cpb.ajcc_metastasis_pathologic_pm, '_', cfi.bcr_patient_uuid) as patient_name, 
       cpb.ajcc_metastasis_pathologic_pm, cpb.ajcc_pathologic_tumor_stage, 
       cpb.anatomic_neoplasm_subdivision, cpb.metastasis_site 
FROM tnbc.case_file_id cfi 
INNER JOIN tnbc.clinical_patient_brca cpb ON cfi.bcr_patient_uuid = cpb.bcr_patient_uuid
WHERE cpb.ajcc_metastasis_pathologic_pm = 'M1' 
   OR cpb.ajcc_metastasis_pathologic_pm = 'M0' 
   OR cpb.ajcc_metastasis_pathologic_pm = 'MX';
  
SELECT cpb.ajcc_metastasis_pathologic_pm,
       cpb.ajcc_pathologic_tumor_stage,
       cpb.anatomic_neoplasm_subdivision,
       cpb.metastasis_site,
       COUNT(DISTINCT CONCAT(cpb.ajcc_metastasis_pathologic_pm, '_', cfi.bcr_patient_uuid)) as unique_patient_count
FROM tnbc.case_file_id cfi
INNER JOIN tnbc.clinical_patient_brca cpb ON cfi.bcr_patient_uuid = cpb.bcr_patient_uuid
WHERE cpb.ajcc_metastasis_pathologic_pm IN ('M1', 'M0', 'MX')
GROUP BY cpb.ajcc_metastasis_pathologic_pm, cpb.ajcc_pathologic_tumor_stage, cpb.anatomic_neoplasm_subdivision, cpb.metastasis_site;

 
SELECT 
    cpb.ajcc_metastasis_pathologic_pm,
    cpb.ajcc_pathologic_tumor_stage,
    cpb.anatomic_neoplasm_subdivision,
    cpb.metastasis_site,
    COUNT(DISTINCT CONCAT(cpb.ajcc_metastasis_pathologic_pm, '_', cfi.bcr_patient_uuid)) as unique_patient_count
FROM tnbc.case_file_id cfi
INNER JOIN tnbc.clinical_patient_brca cpb ON cfi.bcr_patient_uuid = cpb.bcr_patient_uuid
WHERE cpb.ajcc_metastasis_pathologic_pm IN ('M0', 'M1', 'MX')
    AND cpb.ajcc_metastasis_pathologic_pm != '[Not Available]'
    AND cpb.ajcc_pathologic_tumor_stage != '[Not Available]'
    AND cpb.anatomic_neoplasm_subdivision != '[Not Available]'
    AND cpb.metastasis_site != '[Not Available]'
GROUP BY 
    cpb.ajcc_metastasis_pathologic_pm,
    cpb.ajcc_pathologic_tumor_stage,
    cpb.anatomic_neoplasm_subdivision,
    cpb.metastasis_site;
   
   
   
SELECT
    CONCAT(cpb.ajcc_metastasis_pathologic_pm, '_', cfi.bcr_patient_uuid) as patient_name,
    cfi.file_name,
    cpb.ajcc_metastasis_pathologic_pm,
    cpb.ajcc_pathologic_tumor_stage,
    cpb.anatomic_neoplasm_subdivision,
    cpb.metastasis_site,
    COUNT(DISTINCT CONCAT(cpb.ajcc_metastasis_pathologic_pm, '_', cfi.bcr_patient_uuid)) as distinct_count
FROM
    tnbc.case_file_id cfi
INNER JOIN
    tnbc.clinical_patient_brca cpb ON cfi.bcr_patient_uuid = cpb.bcr_patient_uuid
WHERE
    cpb.ajcc_metastasis_pathologic_pm IN ('M0', 'M1', 'MX')
    AND cpb.ajcc_metastasis_pathologic_pm != '[Not Available]'
    AND cpb.ajcc_pathologic_tumor_stage != '[Not Available]'
    AND cpb.anatomic_neoplasm_subdivision != '[Not Available]'
    AND cpb.metastasis_site != '[Not Available]'
GROUP BY
    cpb.ajcc_metastasis_pathologic_pm,
    cfi.bcr_patient_uuid,
    cfi.file_name,
    cpb.ajcc_pathologic_tumor_stage,
    cpb.anatomic_neoplasm_subdivision,
    cpb.metastasis_site;

    
    
 



 










