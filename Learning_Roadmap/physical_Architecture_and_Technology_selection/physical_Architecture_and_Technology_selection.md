<h2>Physical Architecture and Technology Selection</h2>

Our Process is:

        Requirements
            ↓
        Logical Architecture
            ↓
        Quality Attributes
            ↓
        Architecture Principles
            ↓
        Physical Architecture
            ↓
        Technology Decisions
            ↓
        Implementation

* for the Project, we'll make decisions lile

            | Logical component | Initial technology         |
            | ----------------- | -------------------------- |
            | F1 API            | Jolpica F1 API             |
            | Ingestion         | Python                     |
            | Raw storage       | Local filesystem initially |
            | Staging           | PostgreSQL                 |
            | Analytics         | PostgreSQL                 |
            | Pipeline control  | PostgreSQL                 |
            | Data quality      | Python + pytest            |
            | API/serving       | FastAPI                    |
            | BI                | Power BI                   |
            | Containerisation  | Docker                     |
            | Version control   | Git + GitHub               |
            | Monitoring        | Python logging initially   |
            | Orchestration     | Airflow later              |
            | Cloud             | AWS later                  |

* The Important part is **why** we're choosing each technology
* For example, I would not introduce AWS yet. We first build the platform locally:

        Jolpica API
            ↓
        Python
            ↓
        Raw JSON
            ↓
        PostgreSQL
            ↓
        FastAPI
            ↓
        Power BI

* Then we progressively introduce professional data-engineeing technologies

            Local
              ↓
            Docker
            ↓
            dbt
            ↓
            Airflow
            ↓
            Azure Storage
            ↓
            Azure Database
            ↓
            Azure Functions / Data Factory
            ↓
            Monitoring
            ↓
            CI/CD

* This gives you a useful learning progression rather than deploying a complicated cloud architecture before understaning the fundamentals