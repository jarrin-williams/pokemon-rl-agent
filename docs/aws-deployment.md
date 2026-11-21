# Running a Pokemon experiment on AWS

## Purpose

	Deploy a Pokemon Showdown experiment on AWS EC2, save battle records and
settings in a private S3 bucket, and then retrieve battle records for anaylysis
locally. A successful deployment completes the requested battles, with the 
desired agents and number of battles, stores the matching CSV and JSON files
and allows the results to be analyzed and downloaded after the instance is 
stopped.

## Architecture


