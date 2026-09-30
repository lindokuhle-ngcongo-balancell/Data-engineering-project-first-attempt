**F1 Data Engineering Platform, and end to end platform for ingesting, storing,transforming, analysing, and serving Formula 1 data**

0.1 **what I need to learn**

1. What Data engineering is?
-it is a practice to design,builda dn maintain system and infrastructure that allow organisation to collect, store and transform raw data into a clean, usable format.

    **Core Responsibilities**
     1. **Building Pipelines** : Writing code to Automate ETL(Extract, Transform, Load) processesso data flows smoothly between sources and destinations
     2. **Cleaning Data** : Fixing errors, standardizing formats, and organizing messy, unstructured information
     3. **Managing Infrastructure** :Setting up scalable storage solutions, databases, and cloud platforms (AWS)
     4. **Ensuring Reliability** :Monitoring systems to make sure data is secure,accurate, and available when needed

2. What is data pipeline?
-it an automated system that move raw data from multiple sources, cleans and transforms it, and delivers it to a destination for analysis

    **Core Stages**
     1. **Ingestion** : Collecting raw structured or unstructured data from databases, APIs or event streams
     2. **Transformation** : Cleaning, filtering, formatting and enriching the data to make it usable
     3. **Storage** : Loading the processed information into a repository like a data lake or data warehouse.
     4. **Orchestration** : scheduling tasks, managing dependecies and monitoring system health across the workflow

    **Processing Types**
    1. **Batch Processing**: Handles large data volumes at scheduled intervals
    2. **Streaming**: processes continuous, event-driven data in real time with low latency

    **key Architecture Patterns**
    1. **ETL vs. ELT** (Extract,Transform,Load) transforms data before loading in into a target, while ELT loads raw data first and transforms it inside destination warehousing
    2. **Lambda & Kappa**: Lambda combines separate batch and speed layers, whereas **Kappa** uses a single stream processing layer.
    3. **Reverse ETL** Pushes processed data from a central warehouse back into operational business tools

3. What is Data Architecture?
-it is a blueprint for how an organization collects,stores,integrates and uses data across its systems.

    **Core Componets**
    1. **Data Sources**: Operational databases,logs and external API's that generate raw data
    2. **Ingestion & Pipeline**: Tools that moves and transfprm data from source to storage
    3. **Storage layers**: Repositories like Modern Data Warehouse Archicture setups, data lakes and lakehouse.
    4. **Procesing && Serving**: Engines that run queries, build machine learning models and feed business intelligence tools
    5. **Governance** Policies and security rules ensuring data quality and compliance

    **Key Design Stages**
    1. **Conceptual** Maps High-level business entities and core concepts.
    2. **Logical** Defines data relationships, attributes and structures without typong a specific vendor
    3. **Physical** implements the design using specific database technologis, cload platfrom or hardware.

4. what is OLTP vs OLAP?
-OLTP(Online transaction Processing) runs real-time business operations,while OLAP(Online Analytical Processing) analyzes historical data to drive business decisions.

    **Key Differences**
    1. **Purpose** OLTP handles day to day operations like e-commerce checkouts and ATM withdrawls; OLAP handles business intelligence, reporting, and complex data mining
    2. **Storage Layout** OLTP used **row-oriented storage** optimazed for fast write; **OLAP** uses column-oriented storage optimized for scanning millions of rows.
    3. **Schema Design** OLTP uses **normalized schema** for data intergrity; **OLAP** uses **donormalised schemas** (Like start or Snowflake schemas) to speed up aggregations
    4. **Response Time** OLTP returns results in milliseconds(sub-50ms); OLAP takes seconds to minutes for heavy multi-rows scans
    5. **Examples** PostgreSQL,MySQL and Oracle and OLTP database, snowflake,bigQuery and ClickHouse and OLAP databases


5. ETL vs ELT -ETL (Extract, Transform, Load) transforms data on a separate server before saving it, while ELT (Extract, Load, Transform) loads raw data directly into a target data warehouse and transforms it there

    **Main Differences**
    1. **order of steps** ETL transforms data before loading it; ELT loads raw dara first and transforms it later.
    2. **where it Happens** ETL uses external processing server or staging area; ELT uses the storage and computing power of a cloud data warehouse
    3. **Data type** ETL works best for structured data; ELT handles structured, semi-structured amd unstructued data like images.
    4. **Speed and scale** ETL can be slower with large files because of upfront processing; ELT is fast to load and scales well using modern could platforms like Snowflake

    **When to use which**
    1. **ETL** when scrict privacy or compliance rules, need to scub sensitive data before it lands in storage or work with legacy on-permises systems
    2. **ELT** when using cloud storage, deal with massive data volumes want to faster data loading for business analysts

6. Data warehouse / lake / lakehouse
- Three distinct data storage and management architectures designed for different analytical need

    **Data Warehouse**
    - 
    * A centralized repository that stores clean, structured and relational data optimized fpr business intelligence(BI) aned high-perfomance SQL queries
    * uses schema-on-write (data is structured and formatted before it is loaded) and enforces strict constraints and ACID transactaions(Atomicity, Consistency, Isolation, Durability)
    * fast reporting, dashboards and predictable enterprice analytics, though it is costly scale and maintain for raw or unstractured files
    * Snowflake, Google BigQuery, Amazon Redshift

    **Data Lake**
    -
    * A massive, low-cost storage repository that holds raw data in its native, unstructured, semi-structured or structured format.
    * Uses **Schema-on-read** (data is kept raw and structured only when it is queried) and decouples compute from storage
    * Data Sciences, A.I, M.L and heavy data exploration and heavy data exploration, though unmanaged lakes can lack quality controls and turn into "data swamps"
    * Amazon S3, Hadoop HDFS

    **Data Lakehouse**
    - 
    * A modern hybrid architecture that combines the flexible, low-cost storage of a data lake with the reliable, governance and ACID transactions of a data warehouse
    * Built on top of cheap object storage using open table formats (like Delta lake or Apeche iceberg) to add a powerful metadata and governance layers
    * Unified workloads, allowing data teams to run traditional BI reporting and advanced Machine learning on a single copy of data.
    * Databricks, Delta lake, Apache Iceberg
    


7. **Requirements and architectural thinking**
- Requirements defines what a system must accomplish, while architectural thinking determines how the system will sustainably achieve and evolve those requirements under real-world constraints.

    **The Interplay Between Requirements and Architecture**
    -
    - **Bidirentional and iterative**: Requirements drive __Requirements Elicitation and Analysis__, shaping the high-level structural design, while the chosen architecture uncovers hidden technical constraints that refine and clarify the original requirements.
    - **Bridging business and tech**: Architects translate abstract business goals(like "fast expansion" or "Hogh user trust") into concrete **Architectural Characteristics** (such as elasticity,availability, and security)

    **Core Principles of Architectural Thinking**
    -
    - **Constraint-first design**: Starting with non-negotiable boundaries-like budget, team size, scale and performance limits rather than jumping straight to implementation tools.
    - **Interface-driven focus**: Priotizing clear contracts, boundaries and communication pathways between system components so the system can adapt when individial modules changes.
    - **Optimizing for change**: Balancing runtime qualities(performance, scalability) with development qualities(maintainability, testability) to manage the cost of change over time



<h1>what is Data Engineering</h1>

    A Data Engineer builds systems that data.
    1. Available
    2. Reliable
    3. Consistent
    4. Accessible
    5. Scable
<h2>This Project High-level Archicteture example</h2>
    <li>F1 API -> Data Engineer's Pipeline -> Clean Data -> Database -> Analytics -> Dashboard</li>


- The **Data Engineer** is responsible for the infrastructure and processes that make the data usable.

- this project will focus on Data Engineer, Backend Engineer, Analytics Engineer

<h1>The Data Lifecycle</h1>
    <h2>Every data system has a lifecycle</h2>
    <li>SOURCE -> INGESTION -> STORAGE -> PROCESSING -> MODELLING -> ANALYSIS -> CONSUMPTION</li>

<h3>SOURCE</h3>
<p1>Where does the data originate</p1>
<h4>Jolpica F1 API</h4>
endpoints
<table>
<td>Drivers <br> Teams <br> Circuits <br> Races <br> Qualifying <br> Race results <br> Pit stops <br> Standings</td>
</table>


<h3>Ingestion</h3>
<li>
How do we get data?
</li>
<li>
python -> HTTP -> F1 API
</li>

<h3>Storage</h3>
<li>Where do we put it?</li>
<ul>initially: <br>PostgreSQL</ul>
<bold>later we will introduce cloud storage.</bold>

<h3>processing</h3>
<li>How do we make the data usable</li>

<table>
<td><li>Raw data <br> <li>Validation <br> <li>Cleaning <br> <li>Transformation</td>
</table>

<h3>Modeling</h3>
<li> how should the data be structured for analysis? <br>

<table><td><li>For Example: <br><li>Drivers <br><li>Races <br><li>Constructors <br><li>Results</table>

<h3>Analysis</h3>
<li>What information can we derive?</li>
<table><td><li>Driver performance <br> <li>Constructor performance <br> <li>Race pace <br><li>Pit-stop performance <br><li>Reliability</table>

<h3>Consumption</h3>
<table><td>Who and What uses the results? <br> <li>Power BI <br> <li>FastAPI <br> <li>Reports <br> <li>Applications</table>

<h1>The First Architecture (High-level Architecture)</h1>
<p>At this stage, don't worry about the technologies</p>
<li>Think in term of responsibilities<li>

                  ┌───────────────┐
                  │   F1 API      │
                  │    SOURCE     │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  INGESTION    │
                  │               │
                  │    Python     │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │     RAW       │
                  │     DATA      │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ TRANSFORMATION│
                  │               │
                  │ Clean/Validate│
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │   ANALYTICS   │
                  │     DATA      │
                  └───────┬───────┘
                          │
                ┌─────────┴─────────┐
                ▼                   ▼
          ┌──────────┐        ┌──────────┐
          │ FastAPI  │        │ Power BI │
          └──────────┘        └──────────┘

**Notice something important**
- Power BI does not connect directly to the F1 API

- We are building a data platform between the source and the consu,ers.
- that is the fundamentals Data Engineering mindset

<h3>ETL vs ELT</h3>
    You need to understand these two approaches
<table><th>ETL</table>
    <td><li>Extract <br><li>Transform <br><li>Load <br></td>
<h4>Example</h4>
<table><td><li>F1 API <br> <li> Python cleans data <br> <li> PostgreSQL</table>

<h3>ELT<h3>
<td><li>Extract <br><li> Load <br><li>transform</td>

<h4>Example</h4>
<td><li>F1 API <br> <li> Raw PostgreSQL <br> <li> dbt <br> <li>Analytics tables

<br>
For our project, we'll eventually use a combination: <br>
<table><li>API <br> <li>Extract <br><li>Raw <br><li>Load <br><li>transform <br><li>STAGING <br><li> ANALYTICS</table>

This give us Historical/Raw data that can be reprocessed
- 
<h2>OLTP vs OLAP</h2>
this is important <br>

<h2>OLTP</h2>
<h4>Online Transaction Processing</h4>
Designed for applications

Examples:

<td><li>Users <li>Orders <li> Payments <li>Accounts</td>

**Characteristics**

    - Many small transactions
    - Frequent INSERT/UPDATE
    - Highly normalized
    - Fast individual operations

<h2>OLAP</h2>
Online Analytics Processing

Designed for analysis
<h4>Examples:</h4>
<td><li>Sales Analytics <li> Fleet Analytics <li> F1 Analytics <li>Financial reporting </td>

<br>

**Characteristics**
- 
- Large Queries
- Aggregations
- Historical Data
- Read-heavy
- Analytical models

Out Project is primarily an OLAP/data analytics Workload.

That influence our architecture.


<h2>Data Warehouse</h2>
A data warehouse stores structured data specifically for analysis.

- For Example
    - 
    - dim_driver
    - dim_constructor
    - dim_race
    - dim_circuit

    - fact_race_result
    - fact_qualifying_result
    - fact_pit_stop

This is different from simply copying API JSON into PostgreSQL

We're designing data around analytical Questions.

**EG** <u>How many points did each driver score per season? </u>

Our model should make quetions easy to answer.
- 
<h2>Data Lake</h2>
- A data lake is designed to store large data amounts in relatively Raw form.

    - Think: 
        - F1 API
        - JSON
        - Data Lake

    We will eventually have
    data/
        ├── bronze/
        │   ├── races/
        │   ├── drivers/
        │   └── results/
        │
        ├── silver/
        │   ├── races/
        │   └── results/
        │
        └── gold/
            ├── driver_performance/
            └── constructor_performance/

The important concept is: 
- 
Bronze = raw

Silver = cleaned

Gold = analytical

we will eventually explore this properly in a later phase.

<h2>Data Warehouse vs Data Lake</h2>
Don't Memorize definitions. Understand the purpose. 

Imagine our F1 Platform:

                    F1 API
                       │
                       ▼
                ┌─────────────┐
                │ Data Lake   │
                │             │
                │ Raw JSON    │
                └──────┬──────┘
                       │
                       ▼
                Transformation
                       │
                       ▼
                ┌─────────────┐
                │ Data        │
                │ Warehouse   │
                │             │
                │ Facts/      │
                │ Dimensions  │
                └──────┬──────┘
                       │
                       ▼
                   Power BI

The lake is useful for preserving and processing source data.

The warehouse is optimized for structured analytical consumption

Later we'll learn about the **Lakehouse**, which combines ideas form both

<h2>Requirements thinking</h2>
Before implementation, we need to ask:

**What exactly should the system do?**

<br>Our first functional requirements could be:

FR-01: Retrieve F1 data

<p>The system must retain the original API response.</p> <br>

FR-02: Preserver source data.
<p>The system must validate incoming records</p> <br>

FR-03: validate data 
<p>The system must validate incoming records</p><br>

FR-04: Transform Data
<p>The system must transform source data into analytical structures</p> <br>

FR-05: Store data
<p>The system must persist historical F1 data.</p> <br>

FR-06: Support incremental Ingetion
<p>The system must expose cleaned analytical datasets.</p><br>

FR-07: Provide analytical data
<p>The system must expose cleaned analytical datasets.</p> <br>

FR-08: Provide API access
<p>The platform should expose selected analytical information through REST endpoints.</p><br>

FR-09: Support BI
<p>The analytical layer should support Power BI. </p><br>

FR-10: Monitor pipeline execution
<p>The system should record pipeline execution and failures.</p>

<h2>Non-functional requirements</h2>
These describe how well the system should operate


**For example**
- 
* Reliability - a failed API request should not corrupt the database.
* Maintainability - components should have clear responsibilities.
* Scalability - The architecture should allow the dataset and ingestion frequency to grow.
* Observability - we should know when a pipeline fails
* Security - Secerest should not be stored in source code
* Reproducibility - We should be able to reproduce analytical datasets from stored source data.
* testability - Pipeline components should be independently testable.

<h3>Architecture Principle<h3>

thing to Remember:

**DO Not Design the system around the tools. Design the system around the data flow and responsibilities, then select tols that satisfy those requirements**

For Example, do not say:   

            "We need kafka because Data Engineers use Kafka"
Instead ask:
        
    "Do we have a high-volume, real-time event-streaming problem that requires Kafka?"

If the answer is no, don't introduce Kafka.

for our initial F1 platform:
            
                Python
                PostgreSQL
                FastAPI
                dbt
                Airflow
                Docker
                Power BI
                Azure

Will be introduced only when each solves an actual proble,.


