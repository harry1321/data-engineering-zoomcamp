## Module 1 Homework

ATTENTION: At the very end of the submission form, you will be required to include a link to your GitHub repository or other public code-hosting site. This repository should contain your code for solving the homework. If your solution includes code that is not in file format (such as SQL queries or shell commands), please include these directly in the README file of your repository.

## Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

- `--delete`
- `--rc`
- `--rmc`
- `--rm`


## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

- 0.42.0
- 1.0.0
- 23.0.1
- 58.1.0


# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

::: info

To run python script use Dockerfile.app

`
docker build -f Dockerfile.app
`

`
docker run --rm -it --env-file ./postgres_python/.env --network ny_taxi_postgres_postgres-sql -v ./postgres_python:/app/postgres_python ny_taxi:v1 bash
`

load green taxi trips data to postgres database

`
python ingest.py \
  --tb=green_taxi_trip \
  --fp=green_tripdata_2019-09.csv
`
load zone data to postgres database

`
python ingest.py \
  --tb=taxi_zone_lookup \
  --fp=taxi_zone_lookup.csv
`
:::

## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 15767
- <span style="color:orange">15612</span>
- 15859
- 89009

Answer
```SQL
SELECT COUNT(*) AS total_trips
FROM public.green_taxi_trip t
WHERE CAST(t.lpep_pickup_datetime AS DATE) >= CAST('2019-09-18' AS DATE) AND CAST(t.lpep_dropoff_datetime AS DATE) <= CAST('2019-09-18' AS DATE)
```

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance?
Use the pick up time for your calculations.

Tip: For every trip on a single day, we only care about the trip with the longest distance. 

- 2019-09-18
- <span style="color:orange">2019-09-16</span>
- 2019-09-26
- 2019-09-21

Answer
```SQL
SELECT CAST(t.lpep_pickup_datetime AS DATE) AS pickup_date, MAX(t."trip_distance") AS max_trips
FROM public.green_taxi_trip t
GROUP BY pickup_date
ORDER BY max_trips DESC
LIMIT 1
```

## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
- <span style="color:orange">"Brooklyn" "Manhattan" "Queens"</span>
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"

Answer
```SQL
SELECT sub."pdate", sub."Borough", SUM(sub."total_amount")
FROM (SELECT CAST(t.lpep_pickup_datetime AS date) AS pdate, t."total_amount", zp."Borough"
		FROM public.green_taxi_trip t
		 JOIN public.taxi_zone_lookup zp ON t."PULocationID" = zp."LocationID"
		 ) sub
WHERE sub."pdate" = '2019-09-18'
GROUP BY sub."Borough", sub."pdate"
HAVING SUM(sub."total_amount") > 50000
```

## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- <span style="color:orange">**JFK Airport**</span>
- Long Island City/Queens Plaza

Answer:
```SQL
SELECT sub."drop_zone", sub."tips", zd."Zone"
FROM (SELECT t."PULocationID" pick_zone, t."DOLocationID" drop_zone, t."tip_amount" tips, zp."Zone"
		FROM public.green_taxi_trip t
		JOIN public.taxi_zone_lookup zp ON t."PULocationID" = zp."LocationID"
		WHERE zp."Zone" = 'Astoria'
		 		 ) sub
JOIN public.taxi_zone_lookup zd ON sub."drop_zone" = zd."LocationID"
ORDER BY sub."tips" DESC
```

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.


## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw01
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 29 January, 23:00 CET
