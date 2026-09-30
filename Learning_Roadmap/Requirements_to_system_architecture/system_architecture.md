<h2>What components do we need, what are their responsibilities, and how should they communicate?</h2>

this is the first proper architecture exercise for the F1 Dara Engineering Platform.

the key principle is:
    
        Requirements
            ↓
        Capabilities
            ↓
        Components
            ↓
        Responsibilities
            ↓
        Interfaces
            ↓
        Architecture
            ↓
        Technology decisions
    
We should not start with "Let's PostgreSQL,Airflow and Azure" we first determine what the system requires.

1. **Start with the requirements** 

from the previous lesson, we established requirements such as:

        FR-01  Retrieve F1 data
        FR-02  Preserve source data
        FR-03  Validate data
        FR-04  Transform data
        FR-05  Store historical data
        FR-06  Support incremental ingestion
        FR-07  Provide analytical datasets
        FR-08  Provide REST API access
        FR-09  Support BI
        FR-10  Monitor pipeline execution

Now we translate each requirement into an architectural capability

            | Requirement           | Capability                |
            | --------------------- | ------------------------- |
            | Retrieve F1 data      | Data ingestion            |
            | Preserve source data  | Raw data storage          |
            | Validate data         | Data quality              |
            | Transform data        | Data processing           |
            | Store historical data | Persistent data storage   |
            | Incremental ingestion | Pipeline state management |
            | Analytical datasets   | Data modelling            |
            | REST API              | Data serving              |
            | Power BI              | BI/analytics serving      |
            | Monitor execution     | Observability             |

This is an important Data Engineering skill:
        
    Requirements descibe what the system needs to accomplish; capabilities describe what the architecture must be able to.

2. **Indentify the Major componets**
- Now we can start defining components.
- Our first architecture will have:

        1. F1 API
        2. Ingestion Service
        3. Raw Data Store
        4. Transformation Layer
        5. Analytical Database
        6. Pipeline Control
        7. Data Quality Layer
        8. Serving API
        9. BI Layer
        10. Monitoring

At this point these **Logical Componets**, not necessarily separate applications

That's important

    For Example:
        Raw Data Store

Doesn't mean we have already decided whether it will be
    
    PostgreSQL
    Azure Blob Storage
    ADLS
    S3

That decision comes later

3. **Define reponsibilities**
- Every component should have one clear primary responsibility.

- **F1 API**

- Responsible for:
    
    Providing source data

- it is outside our system
- We don't contol it.

**Ingestion Service**
Responsible for:

    Connecting to F1 API
    Retrieving data
    Handling pagination
    Handling retries
    Recording ingestion metadata
    Passing data to storage

It should NOT:
    
    Create Power BI dashboards
    Calculate driver rankings
    Serve REST requests

Keep responsiblilities separeted

**Raw Data Store**

Responsible for:

    Preserving source data

The important property is:
        
        Raw data should remain as close a pratical to what came from source
    
This gives us reproducibility

**Transformation Layer**
-
Responsible For:

    Cleaning
    Normalising
    Converting data types
    Joining datasets
    Deriving fields
    Preparing analytical data

**Analytical Database**:
-
    Responsible for:
        Storing structured analytical data
**Example**

        dim_driver
        dim_race
        dim_constructor

        fact_race_result
        fact_qualifying_result
        fact_pit_stop

**Pipeline Control**
-

Responsible for knowning:

    What has been processed?
    When did it run?
    Did it succeed?
    How many records were processed?
    What failed?

**Data quality**
- 
* Responsible for knowing


        Is the data valid?
        Is anything missing?
        Are there duplicates?
        Are relationships valid?

**Serving API**
-
* Responsible for:

        Providing application-friendly access to processed data.

**BI**
-
* Responsible for:

        Visualisation
        Reporting
        Exploration
        Business/analytical consumption

**Monitoring**
-
* Responsible for:
        
        Pipeline health
        Errors
        Execution times
        Data freshness
        System health

4. **Create the first logical Architecture**
* Now we can connect the components

                         EXTERNAL
                    ┌─────────────────┐
                    │    F1 API       │
                    └────────┬────────┘
                             │
                             │ HTTPS
                             ▼
                    ┌─────────────────┐
                    │    INGESTION    │
                    │     SERVICE     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   RAW STORAGE   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ TRANSFORMATION  │
                    │     LAYER       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   ANALYTICAL    │
                    │    DATABASE     │
                    └───────┬─┬───────┘
                            │ │
                 ┌──────────┘ └──────────┐
                 ▼                       ▼
        ┌─────────────────┐     ┌─────────────────┐
        │    REST API     │     │    POWER BI     │
        └─────────────────┘     └─────────────────┘

                         ┌─────────────────┐
                         │   MONITORING    │
                         └─────────────────┘

This is our Logical Architecture V0.1

Notice that we haven't decide whether we need:

        Airflow
        Azure Functions
        Event Hubs
        Kafka
        Databricks
        Fabric
        Spark
yet.

this is deliberate

5. **Now define the data flow**
- Architecture isn't only boxes
- we need to understand how data moves
- Our initial data flow is:

        F1 API
            │
            │ 1. Request
            ▼
            Ingestion
            │
            │ 2. Receive JSON
            ▼
            Raw Storage
            │
            │ 3. Read raw data
            ▼
            Transformation
            │
            │ 4. Clean/validate
            ▼
            Analytical Database
            │
            ├───────────────┐
            │               │
            ▼               ▼
            FastAPI         Power BI

Now we can ask important architectural questions.

for example:
    
    What happens if transformation fails?
we shouldn't lose the source data

Therefore:
        
            F1 API
            ↓
            RAW
            ↓
            Transformation ❌

The raw data remain availble.

We can retry transformation later

That leads to our Architectural principle

6. **Architectural Decision #1: Preserve raw data**
- ADR-001: Raw data preservation
- Decision: 
    
    The system will preserve the original source response before performing transformations.

- Reason:
    
    - This allows us to:
        
        - Resprocess historical data
        - debug transformation problems
        - investigate source changes.
        - rebuild analytical tables.
        - maintain source traceablity

- Rejected Approach:
        
        API
        ↓
        Transform
        ↓
        Database
- because the original repsonse would be lost.

- Selected approach:
        
        API
        ↓
        RAW
        ↓
        Transform
        ↓
        Analytics

- This is our first Architecture Decision Record.

7. **Architectural Decision #2: Separate raw and analytical data**
- we don't want:
        
        raw_api_data
- Mixed with: 

        driver_performance
- In the same conceptual layer
- Instead:

        RAW
        │
        ▼
        STAGING
        │
        ▼
        ANALYTICS
- why?
- Because each layer has a different responsibility
- **Raw**
    -
* "What did the source give us?"

- **Staging**
    -
* "How do we standardise it?"

- **Analytics** 
    -
- What does the business/analyst need?

therefore:

ADR-002: Layered data architecure

we'll use:

        1. Raw
        2. Staging
        3. Analytics
- as logic data layers.

8. **Architectural Decision #3: Batch processing initially**
- Now Ask:
    
    Does the Platform need real-time streaming?
- Initially, No.
    
    * We are dealing with race and historical data.
    * We can retreive data periodically

* Therefore:
        
        F1 API
        ↓
        Scheduled ingestion
        ↓
        Process data
        ↓
        Database
    
* Rather than:
        
        F1 API
        ↓
        Kafka
        ↓
        Streaming consumers
        ↓
        Data Lake

* Decision - start with batch processing, later we can introduce streaming as a learning exercise.
* This teaches us an important engineering principle: 
    * Use architecture appropriate to the problem rather than adding infrastructure because it is popular.

9. **Architectural Design #4: PostgresSQL initially**
- We need a persistent analytical store.
- Possible Choices include:
    * PostgreSQL
    * MySQL
    * SQL Server
    * Snowflake
    * BigQuery
    * Fabric
    * synapse

For this project, PostgreSQl make sense because it will give us understanding:
* SQL
* Relational Modelling
* Indexing
* Constriants
* Transactions
* views
* Query Optimisation

Without introducing unnecessary cloud complexity.

**Therefore**
* ADR-004
    * initial database = PostgreSQL
* Later:
    * PostgreSQL -> AWS PostgreSQL Database

10. **Architectual Decision #5: Python for ingestion**
* Python has strong support for:
    * HTTP
    * JSON
    * Data Processing
    * Validation 
    * Testing 
    * Database access
    * Automation
* Which meaning:
    * Ingestion Service = python

* Potential Libriaries:
    * httpx
    * pydantic
    * SQLAlchemy
    * Pandas/Polars
    * pytest

11. **Architectural Decision #6: API and BI are consumers**
* This is an important destinction
* API is not the database.
* Power BI is not the database.
* They are only consuming analytical data

                 PostgreSQL
                Analytics
                    │
             ┌──────┴──────┐
             ▼             ▼
          FastAPI       Power BI

* This means we can change the cunsumers without rebuilding the ingestion pipeline

12. **Define boundaries**
* Now we can introduce a useful architectural concept:
* <u>**Boundaries**</u>
* We should have a boundaries between:

        External source
            │
            ▼
        Ingestion
            │
            ▼
        Storage
            │
            ▼
        Transformation
            │
            ▼
        Serving
* Suppose the F1 API Changes its response Formar.
* Ideally
        
        F1 API changes
            ↓
        Ingestion adapter changes
            ↓
        Internal system remains stable

* Rather than: 

        F1 API changes
           ↓
        Everything breaks

* This is why we do not every part of the application to directly call the external API

13. **Define the system boundary**
* Our Architecture Dcocument should explicitly state what is inside the outside the platform.

                            SYSTEM BOUNDARY

            ┌──────────────────────────────────────────────┐
            │                                              │
            │          F1 DATA ENGINEERING PLATFORM        │
            │                                              │
            │  Ingestion                                   │
            │      ↓                                       │
            │  Raw Storage                                 │
            │      ↓                                       │
            │  Transformation                              │
            │      ↓                                       │
            │  Analytical Database                         │
            │      ↓                                       │
            │  API / BI                                    │
            │                                              │
            └──────────────────────────────────────────────┘
                        ▲                         │
                        │                         │
                    External API              Users/BI

* Extenal: 
    * API 
    * Power BI client
    * Users

* Internal
    * Ingestion
    * Storage
    * transformation
    * Database
    * Serving API
    * Monitoring

