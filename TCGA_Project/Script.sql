SELECT tumor_status, count(0) FROM tnbc.clinical_patient_brca group by tumor_status 
Select tumor_status, ajcc_metastasis_pathologic_pm, count(0) from tnbc.clinical_patient_brca group by tumor_status, ajcc_metastasis_pathologic_pm

SELECT * FROM tnbc.clinical_patient_brca
select count(0) from tnbc.clinical_patient_brca cpb where cpb.er_status_by_ihc ='Negative' and cpb.pr_status_by_ihc='Negative' and cpb.her2_status_by_ihc ='Negative'
select patient_id from tnbc.clinical_patient_brca where ajcc_metastasis_pathologic_pm='M' and er_status_by_ihc ='Negative' and pr_status_by_ihc='Negative' and her2_status_by_ihc ='Negative'
select ajcc_metastasis_pathologic_pm, count(0) from tnbc.clinical_patient_brca group by ajcc_metastasis_pathologic_pm





select count(0) from tnbc.sites_beta_value sbv 

select count(distinct FileName)  from tnbc.sites_beta_values limit 20

select count(distinct sites) from tnbc.sites_beta_values


SELECT DISTINCT c.er_status_by_ihc, c.ajcc_metastasis_pathologic_pm, f.file_name, f.file_id, c.bcr_patient_uuid
FROM tnbc.clinical_patient_brca c
JOIN tnbc.case_file_id f ON c.bcr_patient_uuid = f.bcr_patient_uuid
WHERE c.ajcc_metastasis_pathologic_pm = 'M1'
-- AND c.er_status_by_ihc = 'ER-positive'
-- AND c.pr_status_by_ihc = 'PR-negative'
-- AND c.her2_status_by_ihc = 'HER2-positive'


select * from tnbc.sites_beta_values limit 20


-- create table to store all M1 sites with beta value greater than 0.4 
CREATE TABLE `all_M1_Sites_GtPtZ4` (
  `sites` varchar(20) DEFAULT NULL,
  `beta_value` double(20,16) DEFAULT NULL,
  `FileName` varchar(300) DEFAULT NULL,
  KEY `all_M1_Sites_GtPtZ4_sites_IDX` (`sites`) USING BTREE,
  KEY `all_M1_Sites_GtPtZ4_FileName_IDX` (`FileName`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


#insert data into  all_M1_Sites_GtPtZ4
insert INTO  tnbc.all_M1_Sites_GtPtZ4  
select sites ,beta_value, FileName  from tnbc.sites_beta_values
where FileName in (
select  f.file_name  
from  tnbc.clinical_patient_brca c join tnbc.case_file_id f
	on c.bcr_patient_uuid = f.bcr_patient_uuid 
where c.ajcc_metastasis_pathologic_pm='M1'

) and beta_value > 0.4


#choose the sites that have most occurance value being gt 0.4
select sites from (
select sites, count(0) cnt from tnbc.all_M1_Sites_GtPtZ4 
group by sites order by count(0) desc ) a limit 10

 
-- create table to store all M0 sites with beta value less than 0.4 with corresponding M1 greater than 0.4 
CREATE TABLE `all_M0_LtPtZ4_w_M1GtPtZ4` (
  `sites` varchar(20) DEFAULT NULL,
  `beta_value` double(20,16) DEFAULT NULL,
  `FileName` varchar(300) DEFAULT NULL,
  KEY `all_M0_LtPtZ4_w_M1GtPtZ4_sites_IDX` (`sites`) USING BTREE,
  KEY `all_M0_LtPtZ4_w_M1GtPtZ4_FileName_IDX` (`FileName`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


#Insert using the subquery 
insert into all_M0_LtPtZ4_w_M1GtPtZ4 as
select 
#distinct sites
sites ,beta_value, filename  
from tnbc.sites_beta_values
where FileName in (
select  f.file_name  
from  tnbc.clinical_patient_brca c join tnbc.case_file_id f
	on c.bcr_patient_uuid = f.bcr_patient_uuid 
where c.ajcc_metastasis_pathologic_pm='M0'

) and beta_value < 0.4
and sites in 
(
#query from above
select distinct sites   from tnbc.sites_beta_values
where FileName in (
select  f.file_name  
from  tnbc.clinical_patient_brca c join tnbc.case_file_id f
	on c.bcr_patient_uuid = f.bcr_patient_uuid 
where c.ajcc_metastasis_pathologic_pm='M1'

) and beta_value > 0.4
)


#Insert using the subquery ----worked 
insert into tnbc.all_M0_LtPtZ4_w_M1GtPtZ4 
#create table tnbc.all_M0_LtPtZ4_w_M1GtPtZ4  as
select 
sites ,beta_value, filename  
from tnbc.sites_beta_values
where FileName in (
select  f.file_name  
from  tnbc.clinical_patient_brca c join tnbc.case_file_id f
	on c.bcr_patient_uuid = f.bcr_patient_uuid 
where c.ajcc_metastasis_pathologic_pm='M0'and c.er_status_by_ihc ='Negative' and c.pr_status_by_ihc='Negative' and c.her2_status_by_ihc ='Negative'
#Positive
#Negative
#[Not Evaluated]

) and beta_value < 0.4
and sites in 
(
select distinct sites   from tnbc.all_M1_Sites_GtPtZ4 amsgpz 
)



#drop table  tnbc.all_M0_LtPtZ4_w_M1GtPtZ4 
select count(distinct sites)  from tnbc.all_M0_LtPtZ4_w_M1GtPtZ4 
--193,306
select count(distinct FileName)  from tnbc.all_M0_LtPtZ4_w_M1GtPtZ4 
--72


select count(distinct sites) from all_M1_Sites_GtPtZ4
--308,243
select count(distinct FileName) from all_M1_Sites_GtPtZ4
--14




select  f.file_name  
from  tnbc.clinical_patient_brca c join tnbc.case_file_id f
	on c.bcr_patient_uuid = f.bcr_patient_uuid 
where c.ajcc_metastasis_pathologic_pm='M1'and c.er_status_by_ihc ='Negative' and c.pr_status_by_ihc='Negative' and c.her2_status_by_ihc ='Negative'
#NNN M1 filename
e67c69a7-6161-4dd5-9efe-9d13e632989a.methylation_array.sesame.level3betas.txt
c8e84511-71ce-4938-a374-99980bf6d7ba.methylation_array.sesame.level3betas.txt



select 
(select distinct sites from tnbc.all_M0_LtPtZ4_w_M1GtPtZ4 
where sites in  (
select sites from tnbc.all_M1_Sites_GtPtZ4 amsgpz where FileName in 
#NNN M1 filename
('e67c69a7-6161-4dd5-9efe-9d13e632989a.methylation_array.sesame.level3betas.txt',
'c8e84511-71ce-4938-a374-99980bf6d7ba.methylation_array.sesame.level3betas.txt'
) 
)
limit 10 )
#choose any 10 sites 
cg00000029
cg00000165
cg00000292
cg00000321
cg00000924
cg00001249
cg00001261
cg00001269
cg00001349
cg00001747

drop table plot_scenario_1
create table plot_scenario_1 as 
select * from (
select *, 'M1' metastasis from tnbc.all_M1_Sites_GtPtZ4 where sites in 
(
'cg00000029',
'cg00000165',
'cg00000292',
'cg00000321',
'cg00000924',
'cg00001249',
'cg00001261',
'cg00001269',
'cg00001349',
'cg00001747'
)
union 
select *, 'M0' metastasis  from tnbc.all_M0_LtPtZ4_w_M1GtPtZ4 where sites in 
(
'cg00000029',
'cg00000165',
'cg00000292',
'cg00000321',
'cg00000924',
'cg00001249',
'cg00001261',
'cg00001269',
'cg00001349',
'cg00001747'
)
) a




select sites, beta_value, metastasis from  tnbc.plot_scenario_1 where FileName ='e67c69a7-6161-4dd5-9efe-9d13e632989a.methylation_array.sesame.level3betas.txt'


update  tnbc.plot_scenario_1
set metastasis= 'M1_NNN'
where FileName in (
'e67c69a7-6161-4dd5-9efe-9d13e632989a.methylation_array.sesame.level3betas.txt',
'c8e84511-71ce-4938-a374-99980bf6d7ba.methylation_array.sesame.level3betas.txt')

update  tnbc.plot_scenario_1
set metastasis= CONCAT(metastasis,'_',SUBSTRING_INDEX(FileName,'.',1)) 


select *, CONCAT(metastasis,'_',SUBSTRING_INDEX(FileName,'.',1)) from tnbc.plot_scenario_1
select * from tnbc.plot_scenario_1


-- tnbc.plot_scenario_1_full definition

CREATE TABLE `plot_scenario_1_full` (
  `sites` varchar(20) DEFAULT NULL,
  `beta_value` double(20,16) DEFAULT NULL,
  `FileName` varchar(300) DEFAULT NULL,
  `metastasis` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  KEY `plot_scenario_1_full_FileName_IDX` (`FileName`) USING BTREE,
  KEY `plot_scenario_1_full_metastasis_IDX` (`metastasis`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

select count(distinct sites) from tnbc.plot_scenario_1_full
drop table plot_scenario_1_full

#all M1 sites M1 and same sites in M0 sites 
create table plot_scenario_1_full as 
select * from (
select *, 'M1' metastasis from tnbc.all_M1_Sites_GtPtZ4 where sites in 
(
select distinct sites from tnbc.all_M0_LtPtZ4_w_M1GtPtZ4
)
union 
select *, 'M0' metastasis  from tnbc.all_M0_LtPtZ4_w_M1GtPtZ4 where sites in 
(
select distinct sites from tnbc.all_M1_Sites_GtPtZ4
)
) a

update  tnbc.plot_scenario_1_full
set metastasis= 'M1_NNN'
where FileName in (
'e67c69a7-6161-4dd5-9efe-9d13e632989a.methylation_array.sesame.level3betas.txt',
'c8e84511-71ce-4938-a374-99980bf6d7ba.methylation_array.sesame.level3betas.txt')

update  tnbc.plot_scenario_1_full
set metastasis= CONCAT(metastasis,'_',SUBSTRING_INDEX(FileName,'-',1)) 


select * from plot_scenario_1_full



SELECT sites, count(0) FROM plot_scenario_1_full psf  
#where FileName in 
#('e67c69a7-6161-4dd5-9efe-9d13e632989a.methylation_array.sesame.level3betas.txt','c9a71a6a-451c-43d6-a183-bf42adb6ba44.methylation_array.sesame.level3betas.txt')
where SUBSTR(metastasis,0,2)  
group by sites having count(0)>70 order by 2 desc 



#79 
cg21526205
cg06761719
cg12210255
cg12231969

select count(distinct sites)  from plot_scenario_1_full where SUBSTR(metastasis,1,2)='M1'
--193306

select count(distinct sites)  from plot_scenario_1_full where SUBSTR(metastasis,1,2)='M0'
--193306

create table plot_scenario_1_full_M1
as select *  from plot_scenario_1_full where SUBSTR(metastasis,1,2)='M1'

create table plot_scenario_1_full_M0
as select *  from plot_scenario_1_full where SUBSTR(metastasis,1,2)='M0'


select * from plot_scenario_1_full_M1 where sites like 'ch.%'

select distinct sites  from plot_scenario_1_full_M0 where sites not like 'cg%'


select * from plot_scenario_1_full_M1


select distinct m1.sites, m1.metastasis ,m1.beta_value,  m0.sites, m0.metastasis , m0.beta_value, m1.beta_value - m0.beta_value diff  from 
plot_scenario_1_full_M1 m1
join 
plot_scenario_1_full_M0 m0
on m1.sites = m0.sites
and (m1.beta_value - m0.beta_value) > 0.2

select count(distinct m1.sites)
#, m1.beta_value, m1.metastasis  
from 
plot_scenario_1_full_M1 m1
join 
plot_scenario_1_full_M0 m0
on m1.sites = m0.sites
and (m1.beta_value - m0.beta_value) > 0.2

union 

select count(distinct m0.sites) e from 
plot_scenario_1_full_M1 m1
join 
plot_scenario_1_full_M0 m0
on m1.sites = m0.sites
and (m1.beta_value - m0.beta_value) > 0.02


#get MX for prediction
select distinct c.er_status_by_ihc
,c.ajcc_metastasis_pathologic_pm, f.file_name, f.file_id, c.bcr_patient_uuid, c.er_status_by_ihc, c.pr_status_by_ihc, c.her2_status_by_ihc  
from  tnbc.clinical_patient_brca c join tnbc.case_file_id f
	on c.bcr_patient_uuid = f.bcr_patient_uuid 
where c.ajcc_metastasis_pathologic_pm='MX' 


create table tnbc.all_MX_top50_Sites as 
select 
sites ,beta_value, filename, CONCAT('MX','_',SUBSTRING_INDEX(FileName,'-',1)) metastasis
from tnbc.sites_beta_values
where FileName in (
select  f.file_name  
from  tnbc.clinical_patient_brca c join tnbc.case_file_id f
	on c.bcr_patient_uuid = f.bcr_patient_uuid 
where c.ajcc_metastasis_pathologic_pm='MX')
and sites in ('cg00820405',
'cg01450807',
'cg01755336',
'cg02500075',
'cg03516335',
'cg03519967',
'cg03954048',
'cg05260877',
'cg05542646',
'cg05603610',
'cg05860566',
'cg06033949',
'cg06282596',
'cg06710328',
'cg06721601',
'cg06755262',
'cg07212543',
'cg08354372',
'cg08882099',
'cg09455513',
'cg10853431',
'cg11256956',
'cg11724393',
'cg12243738',
'cg12245706',
'cg13321956',
'cg14196395',
'cg14485744',
'cg14716686',
'cg15692360',
'cg15913725',
'cg16063018',
'cg16516248',
'cg17291767',
'cg18766900',
'cg19192065',
'cg19458787',
'cg19757422',
'cg20253855',
'cg21113446',
'cg21771569',
'cg22300566',
'cg23272369',
'cg23407151',
'cg23493787',
'cg23873703',
'cg24395504',
'cg24822602',
'cg25118606')
and FileName in (
'419508be-9162-4fd8-972e-53ea3c20cae4.methylation_array.sesame.level3betas.txt',
'aff74e23-3429-4723-b60c-3648a45c7159.methylation_array.sesame.level3betas.txt',
'486b46a8-0b5f-49a4-ba51-5749fcaffcd1.methylation_array.sesame.level3betas.txt',
'f95e0bea-2bb3-44e2-ba19-bfe0e40aa34b.methylation_array.sesame.level3betas.txt',
'238a2054-55ff-4281-b346-bf09a5af43a1.methylation_array.sesame.level3betas.txt')




select sites, beta_value, metastasis from tnbc.plot_scenario_1_full where sites in ('cg21526205','cg06761719','cg12210255','cg12231969')
SELECT distinct FileName  FROM plot_scenario_1_full where sites in ('cg21526205','cg06761719','cg12210255','cg12231969')

select * from plot_scenario_1_full where sites  ='cg06761719' and metastasis ='M1_NNN_c8e84511'

/*select 
#distinct sites
sites ,beta_value  
from tnbc.sites_beta_values
where FileName in (
select  f.file_name  
from  tnbc.clinical_patient_brca c join tnbc.case_file_id f
	on c.bcr_patient_uuid = f.bcr_patient_uuid 
where c.ajcc_metastasis_pathologic_pm='M0'

) and beta_value < 0.4
and sites in 
(
'cg27570233',
'cg27570354',
'cg27570732',
'cg27570896',
'cg27570951',
'cg27571409',
'cg27571605',
'cg27571676',
'cg27571769',
'cg27572038'

)*/








CREATE INDEX sites_beta_value_sites_IDX USING BTREE ON tnbc.sites_beta_value (sites);

ALTER TABLE tnbc.sites_beta_value MODIFY COLUMN sites CHAR(20) ;


create table tnbc.sites_beta_values as
select * from tnbc.sites_beta_value where beta_value is not null


CREATE TABLE `sites_beta_value` (
  `sites` varchar(20),
  `beta_value` double(20,16) DEFAULT NULL,
  `FileName` varchar(300)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



INSERT INTO tnbc.student
(idstudent, studentname, dob)
VALUES(1, 'Jack',  '2008-7-04');

INSERT INTO tnbc.student
(idstudent, studentname, dob)
VALUES(2, 'John',  '2008-7-04');

delete from  tnbc.student where idstudent =1

update tnbc.student 
set studentname='Jack'
where idstudent =1


DELETE FROM tnbc.clinical_patient_brca 
WHERE bcr_patient_uuid in ('bcr_patient_uuid', 'CDE_ID:');


select count(0) from tnbc.clinical_patient_brca 

select er_status_by_ihc, pr_status_by_ihc, her2_status_by_ihc 
from tnbc.clinical_patient_brca WHERE ajcc_metastasis_pathologic_pm = 'M1';

select ajcc_metastasis_pathologic_pm, er_status_by_ihc, pr_status_by_ihc, her2_status_by_ihc, gender, race, ajcc_pathologic_tumor_stage, count(0)
from tnbc.clinical_patient_brca  group by ajcc_metastasis_pathologic_pm, er_status_by_ihc, pr_status_by_ihc, her2_status_by_ihc, gender, race, ajcc_pathologic_tumor_stage
order by 1,2,3,4;

DELETE FROM tnbc.case_file_id

select p.bcr_patient_uuid, p.patient_id, f.id, f.file_id, f.bcr_patient_uuid  from tnbc.clinical_patient_brca  p left join 
			  tnbc.case_file_id f on p.bcr_patient_uuid  = f.bcr_patient_uuid


select p.bcr_patient_uuid, p.patient_id,f.file_id, 
	   p.ajcc_metastasis_pathologic_pm, p.er_status_by_ihc, p.pr_status_by_ihc, p.her2_status_by_ihc
from tnbc.clinical_patient_brca  p left join 
			  tnbc.case_file_id f 
			  on p.bcr_patient_uuid  = f.bcr_patient_uuid
			  where f.file_id is null 
			  order by p.ajcc_metastasis_pathologic_pm, p.er_status_by_ihc, p.pr_status_by_ihc, p.her2_status_by_ihc
			  
			  
select * from tnbc.clinical_patient_brca where bcr_patient_uuid='55262FCB-1B01-4480-B322-36570430C917'

select * from  tnbc.case_file_id

select bcr_patient_uuid, count(0) from  tnbc.case_file_id
   group by bcr_patient_uuid
   having count(0)>1 order by 2 desc 

c1d311df-f8db-41a4-8091-26c6511830e3

select bcr_patient_uuid, patient_id, ajcc_metastasis_pathologic_pm, er_status_by_ihc, pr_status_by_ihc, her2_status_by_ihc from tnbc.clinical_patient_brca
			  