<h1>Quality Attributes to Acceptance Criteria</h1>

* We currently have:

        Requirements
            ↓
        Capabilities
            ↓
        Components
            ↓
        Architecture
            ↓
        Architectural Decisions
            ↓
        Quality Attributes
            ↓
        Acceptance Criteria

* The last step is essentially asking:

    "How will we know that our architecture actually satisfies the requirements?"
1. **Reliability**
* Requirement
    * The ingestion system should handle temporary API failures
* Acceptance Criteria Could be:

        - Retry failed API requests.
        - Use a maximum retry count. 
        - Record failed requests in logs.
        - A Failed requests in logs
        - A permanently failed pipeline run must be marked Failed

Now "reliable" has become something we can actually test.

2. **Data Integrity**
* Requirement:
    * Data Entering the analytical layer must satisfy defined validation rules.

* Acceptance criteria:

        - Required fields cannot be NULL.
        - Driver IDs must reference valid drivers.
        - Race IDs must reference valid races.
        - Lap numbers must be positive.
        - Duplicate records must be detected.
        - Invalid records must be logged.

* This enventually becomes automated data-quality test.

3. **Maintainability**
* Requirement:
    * Components should have clear responsibilities.

* Accemptance criteria:

    - API communication is isolated from database code.
    - Transformation logic is isolated from ingestion.
    - Database operations are isolated from business logic.
    - Configuration is externalised.
    - Components can be tested independently. 

* This Prevents us from eventually creating one enormous main.py

4. **Scalability**
* Requriements:
    * The system should support additional F1 seasons without redesigning the architecure.

* Acceptance criteria:
    * The pipeline should support:
        * 2026
        * 2025
        * 2024
        * ...

* Without requiring a separate implementaion for every season.
* The architecture should therefore support such as:
    * Season
    * Round
    * Driver
    * Constructor

* Rather than hardcoading 2026.

5. **Performance**
* We need to be careful here.

* Don't prematurely say:
    * 'Every query must take less thank 1 second'.

* We don't yet know our dataset size or hardware

* Instead, initially:
    - Analytical queries should execute against PostgreSQL rather than repeatedly calling the F1 API.
    - Frequently queried columns should be indexed where appropriate.
    - Large datasets should be queried using appropriate filtering
    - Pipeline performance should be measurable.

* Later, where we have actual data, we can establish realistic benchmarks.

6. **Observability**
* Our pipeline should tell us what happend.
    * For Example:
        * Pipeline run
            * Run ID:           20261001-001
            * Season:           2026
            * Round:            15
            * Started:          09:00
            * Completed:        09:02
            * Status:           SUCCESS
            * Records fetched:  5,423
            * Records loaded:   5,401
            * Records rejected: 22
            * Duration:         2m 03s

* This allows us to answer:
    * What happened?
* Without opening the source code and guessing.

7. **Security** 
* Initially we are working locally, byt we should establish the correct pattern now.

        Application
            ↓
        Environment/configuration
            ↓
        Credentials
* Not:

        Python source code
                ↓
        Hardcoded password

* Acceptance criteria:

        - No Secrets Commited to Git
        - Database credentials are externalised.
        - .env is excluded from Git.
        - Production secrets will be eventually use AWS Key Management
8. **Reproducibility** 
* Suppose we download the 2026 belgian Grand Prix data today.
* Later we change our transformation logic
* We should be able to process the same raw data again
* Therefore:

            Raw data
                ↓
            Transformation v1
                ↓
            Analytics

* Can later become:

        Same raw data
            ↓
        Transformation v2
            ↓
        New analytics result

* This is one of the strongest reasons for preserving raw data.

9. **Testing**
* We want to be able to test individual components
* For Example:

        F1 API Client
            ↓
        Unit Test

        Transformer
            ↓
        Unit Test

        Validator
            ↓
        Unit Test

        Database Repository
            ↓
        Integration Test

        Complete Pipeline
            ↓
        End-to-End Test
* We don't want the only way to test the system to be:
    * Run the entire pipeline and see what happens

10. **Cost**
* For the first version:

        Local machine
            +
        PostgreSQL
            +
        Python
            +
        Docker
            +
        GitHub  
* Is sufficient
* There is no Reason to immediately deploy:

            Azure Functions
            Azure Data Factory
            Azure Storage
            Azure Database
            Databricks
            Kafka
            Kubernetes
            
            or 
            AWS services

* Just because they exist.

* The architecture should evolve when there is a requirement that justifies the technology

<h1>Now we create our Architecture Principles</h1>
- These are slightly different from requirements

* What must the system achieve?

Architecture principles say:
* What rules will guide our design?

For our Project, I will would establish these:
* Principle 1, Preserve Source data
    * Never destroy the original data after ingestion.
* Principle 2, Separate responsibilities 
    * Ingestion
    * transformation
    * storage
    * analytics
    * serving should clear boundaries.
* Principle 3, Validate before analytics
    * Data quality problems should be identified before data reaches the analytical layer
* Principle 4 , Prefer batch initially
    * Do not introduce streaming infrastructure without a real requirement.
* Principle 5, Design for incremental processing
    * the pipeline should eventually process only the data that needs processing.
* Principle 6, Separate configuration from code
    * Credentials, API config and env specific settings should not be hardcoded
* Principle 7, Make failures observable
    * A failed pipeline should produce enough information to determine what failed and why.
* Principle 8, Design for reprocessing
    * We should be able to rerun transformations againt previously ingested raw data.
* Principle 9, Technology follows requirements
    We don't introduce technologies simply because they are popular
* Prinicle 10, Start simple, evolve deliverately
    * The first architecture should be simple enough to understand but structured enough to evolve into a production architecture.

<h1>Our Architecture Decision Record structure</h1>

At this point, we can also formalise our architectural decisions

* for example
        
        ADR-001
        Title: Preserve Raw F1 Data

        Status: Accepted

        Context:
        The F1 API is an external source and transformation failures
        must not result in loss of source data.

        Decision:
        Store the original API response before transformation.

        Consequences:
        + Enables reprocessing
        + Improves debugging
        + Provides source traceability
        + Protects against transformation errors

        Trade-offs:
        - Requires additional storage
        - Requires raw-data management

* We will eventually have something like"

        docs/
            │
            ├── requirements.md
            ├── non-functional-requirements.md
            ├── architecture.md
            ├── data-model.md
            ├── data-pipeline.md
            │
            └── adr/
                ├── ADR-001-preserve-raw-data.md
                ├── ADR-002-data-layers.md
                ├── ADR-003-batch-processing.md
                ├── ADR-004-postgresql.md
                └── ADR-005-python-ingestion.md

* This is starting to resemble an actual engineering project rather than a tutorial project

**The architecture baseline**
-
* At the end of Phase 0, our current architecture is

                            EXTERNAL
                    ┌─────────────────┐
                    │    Jolpica F1   │
                    │       API       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    INGESTION    │
                    │     Python      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   RAW STORAGE   │
                    │ Source Data     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     STAGING     │
                    │ Clean/Validate  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    ANALYTICS    │
                    │ Business Models │
                    └───────┬─┬───────┘
                            │ │
                  ┌─────────┘ └─────────┐
                  ▼                     ▼
          ┌───────────────┐     ┌───────────────┐
          │    FastAPI    │     │    Power BI   │
          │ Data Serving  │     │  Visualisation│
          └───────────────┘     └───────────────┘

                  ┌─────────────────────┐
                  │ Logs / Monitoring   │
                  │ Data Quality        │
                  │ Pipeline Metadata   │
                  └─────────────────────┘

* We have deliberately **Not Chosen every physical technology yet**. That's interntional.
* The next step is **Phase 1: Physical Architecture & Technology Selection**.
* There we will take this architecture and decide exactly what implements each component:

        Logical Component       → Physical Technology
        ------------------------------------------------
        Ingestion               → Python
        Raw Storage             → ?
        Staging                 → PostgreSQL?
        Analytics               → PostgreSQL
        Pipeline Control        → ?
        Data Quality            → ?
        API                     → FastAPI
        BI                      → Power BI
        Monitoring              → ?
        Development             → Docker
        Version Control         → Git/GitHub
* This is where we start making the first concrete technology architecture for the project
