# purchase-insights-pipeline
End-to-end data pipeline to transform ecommerce purchase data into actionable insights
 
Reproducible end-to-end data pipeline to transform ecommerce purchase data into actionable insights

### Table of contents

---

## Objective (the Why)

### Success Criteria

---

## Use Cases (the Who)

---

## Dashboard (the What)

---

## Tools & Data (the How)
### **Dataset**

### **Tools** 
Diagram

### **Implementation Plan** 

Set up a Google Cloud Platform (GCP) account and create a project.
Provision Virtual Machine (VM) instances to run the necessary infrastructure.
Use Terraform to create a network infrastructure that includes Virtual Private Cloud (VPC), subnets, firewall rules, and load balancers.
Create a Google Cloud Storage bucket to store the Kaggle dataset files.
Use Spark (pyspark) to extract the data from the Kaggle datasets and load it into BigQuery.
Use Dbt to transform and model the data in BigQuery into a structured format for reporting.
Set up Prefect for data orchestration to schedule and manage the pipeline workflow.
Use Docker to containerize the pipeline components for portability and consistency.
Set up Looker studio to connect to BigQuery and visualize the data.
Create dashboards in Looker studio to report on purchase behavior.
Schedule regular updates to the pipeline to ensure data is refreshed and up-to-date.
Monitor the pipeline to ensure it is running smoothly and troubleshoot any issues that arise.
