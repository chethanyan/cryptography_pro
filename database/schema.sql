CREATE DATABASE clinical_trial;
USE clinical_trial;

CREATE TABLE patients (
    patient_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    ssn VARCHAR(20),
    diagnosis VARCHAR(100),
    treatment VARCHAR(100),
    lab_results VARCHAR(100)
);

INSERT INTO patients VALUES
('P001','Alice Patel','1985-04-15','111-22-3333','Hypertension','DrugA','BP 140/90'),
('P002','Ravi Kumar','1978-09-02','222-33-4444','Diabetes','DrugB','HbA1c 7.5');
