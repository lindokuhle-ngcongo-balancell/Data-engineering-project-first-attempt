1. **Physical Architecture**

- Our logical architecture was

        F1 API
            ↓
        Ingestion
            ↓
        Raw
            ↓
        Staging
            ↓
        Analytics
            ↓
        FastAPI / Power BI

* Our first physical implementation will be:

                        INTERNET
                            │
                            ▼
                 ┌────────────────────┐
                 │    Jolpica F1 API  │
                 └─────────┬──────────┘
                           HTTPS
                            │
                            ▼
              ┌─────────────────────────┐
              │       Python App        │
              │                         │
              │  F1 API Client          │
              │  Ingestion              │
              │  Validation             │
              │  Transformation         │
              └───────────┬─────────────┘
                          │
              ┌───────────┴────────────┐
              │                        │
              ▼                        ▼
       ┌──────────────┐       ┌─────────────────┐
       │ Raw JSON     │       │   PostgreSQL    │
       │ Files        │       │                 │
       │              │       │ Staging         │
       └──────────────┘       │ Analytics       │
                              │ Pipeline State  │
                              └────────┬────────┘
                                       │
                         ┌─────────────┴─────────────┐
                         ▼                           ▼
                  ┌──────────────┐           ┌──────────────┐
                  │   FastAPI    │           │   Power BI   │
                  │ Data Serving │           │  Dashboard   │
                  └──────────────┘           └──────────────┘

- Everything initially runs on your develipment machine.

That's intentinal.

2. <h2>Why Python</h2>
- Python will be our ingestion and transformation language.

- Why?
- it gives us:
    * HTTP/API libraries
    * JSON transformation
    * data trasnformation
    * PostgreSQL connectivity
    * tesing 
    * logging 
    * automation
    * excellent data-engineering ecosystem
- We can use all other programming language, but python is particularly for data engineeing.
- More importantly , you alreasy have python experience, so we can sprend our time learing effort on data engineering concepts rather then  learning another ptogramming language

- Decision:
    * Use python for ingestion, validation and transformation.

3. why PostgreSQL?
- PostgreSQL will initially perform serveral jobs

        PostgreSQL
        │
        ├── Staging data
        ├── Analytical data
        ├── Pipeline metadata
        └── Data-quality information

it gives us practical experience with:

        SQL
        Tables
        Relationships
        Primary keys
        Foreign keys
        Constraints
        Indexes
        Views
        Transactions
        Aggregations
        Query optimisation

* we could start with SQLite, but PostgreSQL gives us a more realistic database-engineering environment

* Decision: 
    * Use PostgreSQL as the initial relational data platform.

5. Why raw JSON file?
- This is as important architectural decision
- when Python recieves:

        {
        "season": 2026,
        "round": 1,
        "race": "Australian Grand Prix"
        }

* We don't immediately throw in into PostgreSQL

- insted

         API
         ↓
         JSON response
         ↓
         Raw storage
         ↓
         Transformation
         ↓
         PostgreSQL

- for our first version, raw storage can simply be:

        data/
            └── raw/
                └── 2026/
                    └── round-01/
                        ├── race.json
                        ├── drivers.json
                        ├── results.json
                        └── laps.json

#

later this concept will became

        Local filesystem
            ↓
        s3 Storage 

* this Architecture stays conceptually the same.
- decision:
    * Use immutable raw JSON files initially

#
5. Why FastAPI?
- FastAPI will be our serving layer.

it sits here:

        PostgreSQL
            ↓
        FastAPI
            ↓
        Client

for example:

            GET /api/races/2026
            GET /api/drivers
            GET /api/results/2026/1
            GET /api/standings/2026

- Power BI does not need to use FastAPI for everything. It can connect diretly to the analytical database

- This Teaches an important architectural concept:

    * A serving API and a BI platform are different consumers of the same analytical data.

- Use FastAPI for programmatic data access.

6. Why Power BI?

* Power BI is our analytical consumer.

- its Job is:

        Analytics data
              ↓
            Power BI
              ↓
            Charts
            KPIs
            Tables
            Filters
            Reports

* it should not be responsible for cleaning our entire data pipeline.
- Decision:
    * Use Power Bi for visual analytics and reporting.

7. **Why Docker?**
- initially, you could install everything directly
    * Python
    * PostgreSQL
    * FastAPI
- On your Machine.
- But Docker will eventually allows us to define the environment consistently.
- For Example:

        docker-compose.yml

        services:
            postgres:
            api:
            ingestion:
-  Then another Dev can clone the repository and start the environment without manually configuring everthing.
- We wont overcomplicate Docker yet, but we'll intoduce it early enough to make the project reproducible.
- Decision:
    - Use Docker for environment consistency and deployment preparation
#
<h2>Why Git/GitHub?</h2>

- Git tracks our engineering changes.
- We'll eventually have commits such as:

        initial architecture
        add F1 API client
        add raw ingestion
        add PostgreSQL schema
        add staging transformations
        add data-quality tests
        add FastAPI endpoints
        add Docker
        add CI pipeline

* This gives you an actual engineering history rather than a folder containing final code.
- Decision:
    * Use Git and GitHub source control and collaboration
#

9. **What and Airflow?**
- Not yet
    - Airflow is useful when we have multiple dependent workflows such as:
        * Extract
        * Validate
        * Transform
        * Load
        * Quality Check
        * Report

- But introducing Airflow before we understand the pipeline itself would hide some important concepts from you.
- We'll first build the pipeline ourselves

* Then we'll ask:
    * what problem does Airflow solve?
* that is a much better way to learn orchestration
#

10. What about dbt?
* Same principle.
* We will eventually use dbt for analytics transformations.
* For now:

        Python
           ↓
        PostgreSQL
* Later:

        Python
         ↓
        Raw/Staging
         ↓
        dbt
         ↓
        Analytics

* This will allow us to learn why dbt exists instead of simply adding it because it is popular.
# 

11. Our technology decision table

        | Component             | Technology       | Reason                            |
        | --------------------- | ---------------- | --------------------------------- |
        | Source                | Jolpica F1 API   | External F1 data source           |
        | Ingestion             | Python           | API + data engineering ecosystem  |
        | Raw storage           | JSON files       | Preserve source representation    |
        | Database              | PostgreSQL       | Relational data engineering       |
        | Transformation        | Python initially | Learn transformation fundamentals |
        | Data quality          | Python + pytest  | Automated validation/testing      |
        | API                   | FastAPI          | REST data serving                 |
        | BI                    | Power BI         | Analytics/reporting               |
        | Containerisation      | Docker           | Reproducible environment          |
        | Source control        | Git/GitHub       | Version control                   |
        | Logging               | Python logging   | Initial observability             |
        | Orchestration         | Airflow later    | Workflow scheduling/dependencies  |
        | Analytics engineering | dbt later        | SQL-based transformation          |
        | Cloud                 | AWS later        | Production/cloud architecture     |

**One Important architectural decision**
* We are deliberately **No building the final cloud Architecture now**.
* Our Progression will be:

                  LEVEL 1
             Local Data Platform
                    │
                    ▼
                   Docker
                    │
                    ▼
              ┌─────────────┐
              │     dbt     │
              └──────┬──────┘
                     ▼
                 Airflow
                     │
                     ▼
              ┌─────────────┐
              │    AWS      │
              └──────┬──────┘
                     ▼
             Production Platform
* Each stage introduces a new Data Engineering Concept.
* That is the learing strategy for this project.

**Phase 0 is now essentially complete**
* you have gone from
    * I want to build an F1 Project
* to

            Requirements
                ↓
            Functional requirements
                ↓
            Non-functional requirements
                ↓
            Logical architecture
                ↓
            Architecture principles
                ↓
            Architectural decisions
                ↓
            Physical architecture
                ↓
            Technology selection
* The next phase is where we start building.

<h1>Phase 1: F1 API & Data Acquisition</h1>

* we will start with the actual F1 API.
* The first things you'll learn are:

        API fundamentals
                ↓
            HTTP
                ↓
            REST
                ↓
            Endpoints
                ↓
            Parameters
                ↓
            JSON
                ↓
            Pagination
                ↓
            API errors
                ↓
            Retries
                ↓
            Python API client
                ↓
            Raw ingestion

* The first practical milestone will be veru small:
    * Build a Python program that requests one F1 dataset from the API, validates the responce, and saves the original response as a new Json file.
