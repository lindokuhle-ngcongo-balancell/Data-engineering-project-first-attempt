Yes. I would turn the F1 project into a structured Data Engineering course where you learn each concept immediately by implementing it.
The rule will be: learn → implement → test → document → improve. We should not jump to Azure, Spark, Kafka, or advanced tooling before the fundamentals are working.
F1 Data Engineering Learning Roadmap
PHASE 0  → Engineering fundamentals
PHASE 1  → API & data acquisition
PHASE 2  → Python data engineering
PHASE 3  → SQL & PostgreSQL
PHASE 4  → Data modelling
PHASE 5  → ETL / ELT pipeline
PHASE 6  → Data quality
PHASE 7  → Analytics engineering + dbt
PHASE 8  → Orchestration + Airflow
PHASE 9  → API / serving layer
PHASE 10 → Docker + CI/CD
PHASE 11 → Azure
PHASE 12 → Data lake / warehouse
PHASE 13 → Streaming
PHASE 14 → Spark
PHASE 15 → Production architecture
We can treat each phase as a mini-course.
Phase 0 — Understand the Data Engineering problem
Before touching code, learn what a data engineer actually builds.
Learn
Understand:
Data source
Data ingestion
Raw data
ETL
ELT
Data transformation
Data warehouse
Data lake
Data pipeline
Data quality
Data orchestration
Data lineage
Data serving
BI
You should be able to explain:
Source
  ↓
Ingestion
  ↓
Raw
  ↓
Transformation
  ↓
Storage
  ↓
Analytics
  ↓
Consumption
Project task
Write:
docs/
    requirements.md
    architecture.md
    data-flow.md
Do not code yet.
You have completed Phase 0 when:
You can explain why the system has each layer and what responsibility belongs to each layer.
Phase 1 — Learn APIs and acquire the F1 data
Now we touch the real data.
Learn
You need to understand:
HTTP
REST
GET
POST
Status codes
Headers
Parameters
JSON
Pagination
Rate limiting
Timeouts
Retries
Then learn the F1 API structure.
For example:
API
 │
 ├── seasons
 ├── races
 ├── drivers
 ├── constructors
 ├── results
 ├── qualifying
 └── pit stops
Build
Create:
src/
    ingestion/
        api_client.py
Your first objective is simply:
client.get_races(2025)
and receive structured Python data.
Don't use PostgreSQL yet.
First understand the source.
Deliverables
api_client.py
sample_api_response.json
api-notes.md
Phase 2 — Python for Data Engineering
You already know Python, so this phase should focus on writing production-quality Python, not learning basic syntax.
Learn
Focus on:
Functions
Classes
Type hints
Dataclasses
Pydantic
Exceptions
Logging
Configuration
Packages
Virtual environments
Testing
Then:
httpx
Pandas
Polars
Build
Create:
src/
    ingestion/
    models/
    config/
    utils/
For example:
class Race:

    season: int
    round: int
    name: str
    date: datetime
Then validate API responses with Pydantic.
Project task
Take this:
API JSON
and convert it into:
Validated Python objects
Important concept
Learn the difference between:
Raw API data
and:
Application/domain models
Phase 3 — SQL
This is a major phase.
Do not rush through it.
Learn SQL in this order
First:
SELECT
WHERE
ORDER BY
GROUP BY
HAVING
Then:
JOIN
LEFT JOIN
INNER JOIN
FULL JOIN
Then:
CASE
CTE
SUBQUERY
UNION
Then:
WINDOW FUNCTIONS
Especially:
ROW_NUMBER()
RANK()
LAG()
LEAD()
SUM() OVER()
AVG() OVER()
Then learn database concepts
Primary keys
Foreign keys
Indexes
Constraints
Transactions
ACID
Normalization
Isolation
Project task
Install PostgreSQL.
Create:
f1_database
Then manually create your first tables.
For example:
drivers
races
constructors
circuits
Populate them with a small amount of data.
Goal
You should be able to answer questions such as:
Which drivers participated in the 2025 season?
What was each driver's average finishing position?
Which constructor scored the most points?
without Python.
Phase 4 — Data Modelling
Now learn how a Data Engineer decides what the database should look like.
Learn
Entities
Relationships
Cardinality
Normalization
Fact tables
Dimension tables
Star schema
Grain
Surrogate keys
Natural keys
The most important concept is grain.
For example:
One row in fact_race_result represents one driver participating in one race.
That determines everything else.
Build
Your analytical model could become:
dim_driver
dim_constructor
dim_circuit
dim_race
dim_season

fact_race_result
fact_qualifying_result
fact_pit_stop
Project task
Create:
docs/data-model.md
sql/schema.sql
Draw your ERD.
Phase 5 — Build the first ETL pipeline
Now the project becomes a real Data Engineering project.
Learn:
Extract
Transform
Load
Your first pipeline:
F1 API
  ↓
Python
  ↓
Transform
  ↓
PostgreSQL
But we then improve it.
Phase 6 — Raw / Staging / Analytics architecture
This is where the project starts looking professional.
Implement:
RAW
 ↓
STAGING
 ↓
ANALYTICS
Raw
Store the original API response.
raw_api_responses
Staging
Clean and normalize:
stg_drivers
stg_races
stg_results
Analytics
Business-ready:
dim_driver
dim_race
dim_constructor
fact_race_result
Your architecture becomes:
                 F1 API
                   │
                   ▼
             Python Ingestion
                   │
                   ▼
                  RAW
                   │
                   ▼
                STAGING
                   │
                   ▼
               ANALYTICS
                   │
                   ▼
              PostgreSQL
Phase 7 — Data Quality
Now learn how to make sure the pipeline isn't producing garbage.
Study:
Completeness
Accuracy
Validity
Consistency
Uniqueness
Timeliness
Implement checks such as:
Driver ID cannot be NULL
Race ID must exist
Position cannot be negative
Points cannot be negative
Race must belong to a valid season
Duplicate race results must be rejected
Create:
data_quality_checks
pipeline_errors
Eventually:
Records received: 500
Valid:             495
Rejected:            5
You should know exactly why those five were rejected.
Phase 8 — Incremental loading
This is an important Data Engineering concept.
Don't do:
Every execution
      ↓
Download everything
      ↓
Delete database
      ↓
Reload everything
Learn:
Incremental ingestion
Upsert
Watermark
Change detection
Idempotency
Backfill
Your system should know:
Last processed:
2026 Round 15
Then retrieve only what is necessary.
This is directly transferable to telemetry systems.
Phase 9 — Analytics Engineering with dbt
Once your raw/staging architecture works, introduce dbt.
Learn:
Sources
Models
Staging
Intermediate models
Marts
Tests
Documentation
Lineage
Architecture:
F1 API
   ↓
Python ingestion
   ↓
PostgreSQL RAW
   ↓
dbt
   ├── staging
   ├── intermediate
   └── marts
          ↓
       Power BI
Your dbt models could be:
stg_f1_results
stg_f1_drivers
stg_f1_races

fct_race_results

dim_drivers
dim_races
dim_constructors
Phase 10 — Orchestration
Now you need to stop manually running Python.
Learn:
Scheduling
DAGs
Tasks
Dependencies
Retries
Backfills
Failure handling
Start with simple scheduling.
Then learn Apache Airflow.
Your DAG:
                F1 DAG
                   │
                   ▼
             Fetch race data
                   │
                   ▼
             Store raw data
                   │
                   ▼
             Validate data
                   │
                   ▼
             Transform data
                   │
                   ▼
             Run dbt models
                   │
                   ▼
             Data quality
                   │
                   ▼
             Pipeline success
Phase 11 — Build the API serving layer
Now learn how other applications consume your data.
Use FastAPI.
PostgreSQL
     ↓
Repository
     ↓
Service
     ↓
FastAPI
Endpoints:
GET /drivers
GET /drivers/{driver_id}
GET /races
GET /races/{race_id}
GET /constructors
GET /results
GET /analytics/driver-performance
Learn:
REST
OpenAPI
Pydantic
Pagination
Filtering
Authentication
HTTP status codes
Phase 12 — Docker
Containerize everything.
Learn:
Dockerfile
Images
Containers
Volumes
Networks
Environment variables
Docker Compose
Eventually:
docker-compose.yml

PostgreSQL
FastAPI
Airflow
You should be able to clone your project on another machine and run:
docker compose up
Phase 13 — Testing and CI/CD
Now introduce proper software engineering.
Learn:
Unit testing
Integration testing
Mocking
Test fixtures
Code coverage
Linting
Formatting
CI/CD
Use:
pytest
ruff
GitHub Actions
Pipeline:
git push
   ↓
GitHub Actions
   ↓
Lint
   ↓
Unit tests
   ↓
Integration tests
   ↓
Build
Phase 14 — Power BI
Now build the BI layer.
Don't use Power BI to perform all your transformations.
The database should already provide:
clean
validated
analytical
data.
Build:
F1 Overview
Driver Performance
Constructor Performance
Race Analysis
Circuit Analysis
Pit Stop Analysis
Learn:
Data modelling
Relationships
DAX
Measures
Calculated columns
Filters
Time intelligence
Dashboard design
Phase 15 — Azure
Only now move to cloud.
Your local architecture:
API
 ↓
Python
 ↓
PostgreSQL
 ↓
dbt
 ↓
Power BI
becomes:
                  Azure
                    │
        ┌───────────┼────────────┐
        │           │            │
        ▼           ▼            ▼
   Functions     Storage       Key Vault
        │
        ▼
   PostgreSQL
        │
        ▼
      dbt
        │
        ▼
    Power BI
Learn:
Azure Functions
Azure Storage
Azure Database for PostgreSQL
Azure Data Factory
Azure Key Vault
Azure Monitor
Application Insights
Microsoft Entra ID
Phase 16 — Data Lake
Now learn modern data architecture.
Study:
Data Lake
Data Warehouse
Lakehouse
Bronze
Silver
Gold
Parquet
Partitioning
Data Catalog
Data Lineage
Your architecture could become:
                 F1 API
                   │
                   ▼
             Azure Function
                   │
                   ▼
              ADLS Gen2
                   │
          ┌────────┴────────┐
          ▼                 ▼
       Bronze             Silver
          │                 │
          └────────┬────────┘
                   ▼
                 Gold
                   │
                   ▼
              Power BI
Phase 17 — Streaming
This is where you start connecting the F1 project to your telematics background.
Learn:
Event-driven architecture
Message brokers
Kafka
Azure Event Hubs
Partitions
Consumer groups
Offsets
Event ordering
Exactly-once vs at-least-once
Then imagine:
Telemetry Device
      │
      ▼
 MQTT
      │
      ▼
 Event Hub
      │
      ▼
 Stream Processing
      │
      ▼
 Data Lake
The concepts are extremely transferable to battery telemetry.
Phase 18 — Spark
Only after the previous phases.
Learn:
Spark DataFrames
Transformations
Actions
Partitions
Shuffles
Joins
Aggregations
Spark SQL
PySpark
Then modify your project:
Large dataset
      ↓
PySpark
      ↓
Parquet
      ↓
Data Lake
At this stage you're learning distributed data processing rather than just Python data manipulation.
Phase 19 — Production Data Engineering
Finally learn how to operate the platform.
Study:
Monitoring
Alerting
Logging
Data lineage
Data contracts
Schema evolution
Disaster recovery
Backups
Security
Cost optimization
Performance optimization
SLA/SLO
Your final architecture might look like:
                         F1 API
                            │
                            ▼
                    Azure Functions
                            │
                            ▼
                     Azure Event Hub
                            │
                            ▼
                     ADLS Gen2
                     Bronze Layer
                            │
                            ▼
                     Transformation
                            │
                    ┌───────┴────────┐
                    ▼                ▼
                 Silver             Gold
                    │                │
                    └───────┬────────┘
                            ▼
                     Data Warehouse
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
             FastAPI                 Power BI
                │
                ▼
          Applications
The learning rule
For every technology, follow this sequence:
1. Understand the concept
        ↓
2. Learn the technology
        ↓
3. Build a small example
        ↓
4. Add it to the F1 platform
        ↓
5. Test it
        ↓
6. Document it
        ↓
7. Break it intentionally
        ↓
8. Fix it
For example, don't spend three weeks watching Airflow tutorials.
Learn DAGs → build one DAG → make the F1 pipeline run through it → introduce a failure → implement retries → document what you learned.
That produces actual engineering experience.
What I recommend we do next
We should start with Phase 0, and I can act as your Data Engineering instructor throughout the project.
The first lesson would be:
Lesson 1 — What is a Data Engineering Platform?
You would learn the difference between:
Data Analyst
Data Scientist
Analytics Engineer
Data Engineer
Software Engineer
Then we'd define the F1 project's requirements and produce the first version of:
docs/
├── requirements.md
├── architecture.md
└── data-flow.md

