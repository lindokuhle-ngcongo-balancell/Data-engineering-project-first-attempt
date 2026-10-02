<h2>Non-Functional Requirements</h2>

    | Quality         | Requirement | Architectural implication         |
    | --------------- | -------------------------------------------------- | |
    | Reliability     | Pipeline should handle temporary API failures      | Retries + error handling          |
    | Data integrity  | Data should not be silently corrupted              | Validation + constraints          |
    | Maintainability | Components should be easy to modify                | Separation of responsibilities    |
    | Scalability     | System should handle more seasons/races            | Incremental ingestion + indexing  |
    | Performance     | Analytical queries should return quickly           | Indexes + proper modelling        |
    | Observability   | We should know when something fails                | Logs + pipeline run records       |
    | Security        | Credentials should not be stored in code           | Environment variables/Key Vault   |
    | Reproducibility | Same input should produce predictable output       | Versioned code + raw data         |
    | Testability     | Components should be testable independently        | Modular architecture              |
    | Cost            | Infrastructure should remain inexpensive initially | Local PostgreSQL/batch processing |

* these are called Non-Functional Requirement, also called quality attributes

1. Reliability
- imagine this happen:

        F1 API
        ↓
        Ingestion
        ↓
        RAW
        ↓
        Transformation
        ↓
        PostgreSQL

* The API temporarily returns:
    * HTTP 500 Error

* A poor system will simply crash
* A more Reliable system should:

        Request API
            ↓
        Failure
            ↓
        Retry
            ↓
        Failure
            ↓
        Retry
            ↓
        Failure
            ↓
        Log error
            ↓
        Mark pipeline run as FAILED

* This is important because external systems are outside our control.

2. **Data Integrity**
- Suppose the API key us:
            
        {
            "driver": "VER",
            "position": "1"
        }
* But somewhere during the processing we accidentally convert:
    * "1"
* into:
    * 101
* the database may still accept it.
* The system therefore needs rules such as:

        position must be >= 1
        driver_id must exist
        race_id must exist
        lap_number must be >= 1  
* This is why data engineeing is not simple:
    * API -> Database
* It is :
    * API -> Validate -> transform -> enforce rules -> database

3. **Maintainability**
* Consider two designs
    * bad:
        * having one page project
            
                main.py

                API request
                API authentication
                JSON processing
                cleaning
                database connection
                SQL
                business calculations
                logging
                error handling
                Power BI logic
* One huge program becomes difficult to change.
* Better:
    * having seperate programs

            ingestion/
                f1_client.py
                extractor.py

            processing/
                cleaner.py
                transformer.py

            storage/
                raw_store.py
                postgres.py

            quality/
                validators.py

            monitoring/
                logger.py
* Each component has a responsibility.
* This is directly connected to the architecture principle already identified:
    * Separete responsibilities

4. Scalability.
* we might start with 2026 which has 24 races
* later we may want 1950 to-date which will have:

        1950 ─────────────── 2026
        hundreds of races
        thousands of drivers
        millions of lap records

* We therefore shouldn't design the:
    * load_2026_data()

* We want something conceptually closer to:

            load(season=2026)
            load(season=2025)
            load(season=2024)

* And eventually:

        load(
            season=2026
            round=15
        )
* This leads directly into **incremental ingestion**, which we will implement later.

5. **Perfomance**
* Suppose Power BI Asks:
    * "Show Average lap time by driver for the 2026 season."
* We don't want the system to retrieve everything from the F1 API every time

        F1 API
            ↓
        Pipeline
            ↓
        PostgreSQL
            ↓
        Power BI

* The expensive API work happens during ingestion
* The analytical database is then optimised for querying.
* This is another reason the database sits between the source and BI

<br>

6. **Observability**
* A production data engineer needs to answer questions like:
    * When did the pipeline last run?
    * How many records were loaded?
    * Did the API fail?
    * How long did ingestion take?
    * WHen was the data last updated?
* We therefore eventually want something like :

         Pipeline Run
        -------------------------
        Run ID:       1024
        Started:      14:00
        Finished:     14:02
        Status:       SUCCESS
        Records:      4,582
        Failed:       12
        Duration:     2m 14s
* This becomes extremely important when you more from a personal project into professional

7. **Security**
- Our Local Architecture might use:

        .env
- for configuration
- We should **Never** do this 

        password = "MyDatabasePassword"

- And we should never commit secrets to GitHub.
- Later, when we move to Azure, the conceptual Architecture becomes:

            Application
                ↓
        AWS Key Management
                ↓
            Secrets

* The principle remains the same even though the technology changes

8. **Reproducibility**

- Suppose we run our pipeline today and get
    * 100000 records

- Then we change our transformation code.

- We should be able to run the transformation again against the same raw dataset and understand why the result changed.

- This is one of the major advantages of

        RAW
        ↓
        STAGING
        ↓
        ANALYTICS

* Rather than:

           API
            ↓
        TRANSFORM
            ↓
        DELETE SOURCE

* Let test the Architecture
    - 
1. We can now add the NFRs to our architecture.

* Our current architecture become:

                                ┌──────────────────┐
                                │    F1 API        │
                                │ External Source  │
                                └────────┬─────────┘
                                         │
                                         ▼
                                ┌──────────────────┐
                                │    Ingestion     │
                                │ Python Service   │
                                └────────┬─────────┘
                                         │
                                         ▼
                                ┌──────────────────┐
                                │   RAW STORAGE    │
                                │ Source Data      │
                                └────────┬─────────┘
                                         │
                                         ▼
                                ┌──────────────────┐
                                │    STAGING       │
                                │ Clean/Standardise│
                                └────────┬─────────┘
                                         │
                                         ▼
                                ┌──────────────────┐
                                │    ANALYTICS     │
                                │ Business Models  │
                                └───────┬───┬──────┘
                                        │   │
                               ┌────────┘   └─────────┐
                               ▼                      ▼
                        ┌──────────────┐       ┌──────────────┐
                        │   FastAPI    │       │   Power BI   │
                        │  Data API    │       │  Analytics   │
                        └──────────────┘       └──────────────┘

                        ┌─────────────────────────────┐
                        │ Logging / Monitoring / DQ   │
                        └─────────────────────────────┘

* Notice something important:
    - The Architecture has not changed dramatically because of the NFRs
    - Instead, the NFRs tell us **How much each component must behave**
* For example

        Reliability
            ↓
        Ingestion needs retries

        Data integrity
            ↓
        Staging needs validation

        Maintainability
            ↓
        Components need clear boundaries

        Performance
            ↓
        Analytics database needs indexes

        Security
            ↓
        Secrets must be externalised

        Observability
            ↓
        Pipeline needs logs and run metadata