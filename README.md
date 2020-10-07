# Serverless data pipelines using Amazon Glue to move data between AWS S3 buckets 

This activity can consist of the below steps.

* Step 1: Creation of a source S3 bucket
* Step 2: Uploading desired data to the S3 bucket created
* Step 3: Creation of the target S3 bucket to copy the data
* Step 4: Creation of Glue crawlers
* Step 5: Creation of the ETL jobs for the data movement between S3 buckets

### Step 1: 
An S3 bucket and a prefix are created to place the data file.
![image](https://user-images.githubusercontent.com/72220952/94967920-ed52ec80-04f7-11eb-825b-6e9064a0bc67.png)

### Step 2: 
Data downloaded from the Kaggle has been uploaded into the S3 bucket created in previous step. The data set known as Iris.csv was used in this example
### Step 3: 
A target S3 bucket is created, which act as the target bucket to move the data placed in the source S3 bucket
### Step 4: 
AWS Glue crawler is created to create the meta data catalog about the source S3 buckets. 
In order to create the crawler below options were selected in the console.

	* Crawler source type -Data Stores
	* Choose data store -S3
	* Crawl data in - path of the source s3 prefix
	* Choose an IAM role - select an IAM role with necessary permisions on the Glue. A new role with below policies were 
	  created to perform this hands-on.
	
![image](https://user-images.githubusercontent.com/72220952/94969010-df9e6680-04f9-11eb-8936-ae408371b268.png)
	
	* Frequency - run on Demand
	* Crawler output - Create a new database where the crawler stores the metadata information of the sources.
	

Once the crawler is ready, we can run the same to generate the meta data details. On successful run, the specified database will be created and we can verify that a metadata table is created in the databasewith the schema details.

![image](https://user-images.githubusercontent.com/72220952/94969681-15901a80-04fb-11eb-8346-79739ed444be.png)

 
### Step 5: 
A Glue ETL job is created to move data from Source S3 bucket to target bucket. Below options were selected to create the ETL job.

	* Type -Spark
	* Glue version -default
	* This job runs - A proposed script generated by AWS Glue
	* Specify script file name and s3 path to store the script

Select the datasource which we have created in the previous steps. and transform type is selected as ' Change schema'. 
In the choose data target page, below options were opted.
	
	* Data Store -Amazon S3
	* Format - CSV
	* Target path - select the created target bucket in the S3

Next page shows the details of source and target column mappings.

![image](https://user-images.githubusercontent.com/72220952/95356713-dda02300-08be-11eb-8635-bc355cfba29b.png)


The default script generated by AWS is given below.

```
import sys
from awsglue.transforms import *
from datetime import datetime
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import lit

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [database = "gluesampledata", table_name = "sampledata", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "gluesampledata", table_name = "sampledata", transformation_ctx = "datasource0")
## @type: ApplyMapping
## @args: [mapping = [("id", "long", "id", "long"), ("sepallengthcm", "double", "sepallengthcm", "double"), ("sepalwidthcm", "double", "sepalwidthcm", "double"), ("petallengthcm", "double", "petallengthcm", "double"), ("petalwidthcm", "double", "petalwidthcm", "double"), ("species", "string", "species", "string")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]

applymapping1 = ApplyMapping.apply(frame = datasource1, mappings = [("id", "long", "id", "long"), ("sepallengthcm", "double", "sepallengthcm", "double"), ("sepalwidthcm", "double", "sepalwidthcm", "double"), ("petallengthcm", "double", "petallengthcm", "double"), ("petalwidthcm", "double", "petalwidthcm", "double"), ("species", "string", "species", "string")], transformation_ctx = "applymapping1")
## @type: DataSink
## @args: [connection_type = "s3", connection_options = {"path": "s3://targetglue"}, format = "csv", transformation_ctx = "datasink2"]
## @return: datasink2
## @inputs: [frame = applymapping1]
datasink2 = glueContext.write_dynamic_frame.from_options(frame = applymapping1, connection_type = "s3", connection_options = {"path": "s3://targetglue"}, format = "csv", transformation_ctx = "datasink2")
job.commit()

```



