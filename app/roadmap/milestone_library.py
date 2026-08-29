"""
app/roadmap/milestone_library.py

Milestone Knowledge Base defining the progressive learning steps for skills.
Includes dynamic fallback handling for unknown skills.
"""

from typing import Any, Dict, List

from app.roadmap.roadmap_defaults import get_unknown_milestones

MILESTONE_LIBRARY: Dict[str, List[Dict[str, str]]] = {
    # 1. PROGRAMMING LANGUAGES
    "python": [{"title": "Master Core Syntax & Data Types", "description": "Learn lists, dicts, loops, and functions."}, {"title": "Advanced Python & Async", "description": "Master decorators, OOP, and asyncio."}],
    "javascript": [{"title": "DOM & Events", "description": "Understand event loops and DOM manipulation."}, {"title": "Modern ES6+", "description": "Master Promises, async/await, and closures."}],
    "typescript": [{"title": "Type Annotations", "description": "Learn basic types, interfaces, and classes."}, {"title": "Advanced Generics", "description": "Master utility types and complex generics."}],
    "java": [{"title": "Java OOP Basics", "description": "Understand classes, interfaces, and inheritance."}, {"title": "Concurrency & Streams", "description": "Master multithreading and the Java Stream API."}],
    "cplusplus": [{"title": "Pointers & Memory", "description": "Understand manual memory allocation."}, {"title": "STL & Modern C++", "description": "Master smart pointers and standard template libraries."}],
    "csharp": [{"title": "C# Fundamentals", "description": "Learn types, LINQ, and OOP."}, {"title": "Asynchronous Programming", "description": "Master Task Parallel Library and async/await."}],
    "go": [{"title": "Go Basics", "description": "Learn structs, interfaces, and error handling."}, {"title": "Concurrency with Go", "description": "Master Goroutines and Channels."}],
    "rust": [{"title": "Ownership & Borrowing", "description": "Understand Rust's unique memory safety model."}, {"title": "Fearless Concurrency", "description": "Master multi-threading without data races."}],
    "kotlin": [{"title": "Kotlin Interoperability", "description": "Learn basic syntax and Java interop."}, {"title": "Coroutines", "description": "Master async flow and state management."}],
    "swift": [{"title": "Swift Basics", "description": "Understand Optionals and Protocols."}, {"title": "Swift UI & Concurrency", "description": "Master actors and async/await."}],
    "php": [{"title": "PHP Basics", "description": "Learn scripting, arrays, and form handling."}, {"title": "Modern PHP & OOP", "description": "Master classes, traits, and Composer."}],
    "ruby": [{"title": "Ruby Syntax", "description": "Learn blocks, procs, and basic OOP."}, {"title": "Metaprogramming", "description": "Master dynamic method definition."}],
    "scala": [{"title": "Functional Scala", "description": "Learn immutability and pattern matching."}, {"title": "Concurrent Scala", "description": "Master Futures and Akka actors."}],
    "r": [{"title": "Data Manipulation", "description": "Learn vectors, matrices, and data frames."}, {"title": "Statistical Analysis", "description": "Master Tidyverse and ggplot2 visualization."}],
    "sql_lang": [{"title": "Basic Queries", "description": "Master SELECT, WHERE, and JOINs."}, {"title": "Advanced Aggregation", "description": "Learn CTEs, Subqueries, and Window Functions."}],

    # 2. FRONTEND DEVELOPMENT
    "html5": [{"title": "Semantic HTML", "description": "Structure documents properly."}, {"title": "Web Accessibility", "description": "Implement ARIA roles and keyboard navigation."}],
    "css3": [{"title": "Layout Foundations", "description": "Master Flexbox and CSS Grid."}, {"title": "Responsive Design", "description": "Implement media queries and modern variables."}],
    "react": [{"title": "Component State", "description": "Understand Hooks and unidirectional data flow."}, {"title": "Advanced React Patterns", "description": "Master Context API and performance optimization."}],
    "nextjs": [{"title": "Routing & Rendering", "description": "Understand App Router and SSR/SSG."}, {"title": "Full-Stack Features", "description": "Master Server Actions and API integration."}],
    "vuejs": [{"title": "Vue Reactivity", "description": "Learn the Options and Composition APIs."}, {"title": "State Management", "description": "Master Pinia and Vue Router."}],
    "angular": [{"title": "Components & Directives", "description": "Understand Angular modular architecture."}, {"title": "RxJS & Services", "description": "Master Dependency Injection and Observables."}],
    "svelte": [{"title": "Svelte Basics", "description": "Learn reactive declarations and props."}, {"title": "SvelteKit", "description": "Master routing and server-side data loading."}],
    "tailwindcss": [{"title": "Utility-First Styling", "description": "Learn core classes and responsive modifiers."}, {"title": "Custom Configuration", "description": "Master tailwind.config.js and directives."}],
    "material_ui": [{"title": "MUI Components", "description": "Implement buttons, grids, and typography."}, {"title": "Custom Theming", "description": "Master the ThemeProvider palette override."}],
    "redux": [{"title": "Redux Toolkit Basics", "description": "Set up slices and store."}, {"title": "Async Thunks", "description": "Master RTK Query and middleware."}],
    "vite": [{"title": "Vite Setup", "description": "Initialize and configure a Vite project."}, {"title": "Build Optimization", "description": "Master plugin integration and asset handling."}],
    "webpack": [{"title": "Core Concepts", "description": "Understand entry, output, and loaders."}, {"title": "Advanced Bundling", "description": "Master code splitting and tree shaking."}],
    "web_components": [{"title": "Custom Elements", "description": "Register vanilla JS web components."}, {"title": "Shadow DOM", "description": "Master encapsulated styling and templates."}],
    "webassembly": [{"title": "Wasm Compilation", "description": "Compile C/Rust to Wasm."}, {"title": "JS Interoperability", "description": "Master passing data between JS and Wasm."}],
    "rxjs": [{"title": "Observables", "description": "Understand basic streams and subscriptions."}, {"title": "Complex Operators", "description": "Master switchMap, mergeMap, and catchError."}],

    # 3. BACKEND DEVELOPMENT
    "fastapi": [{"title": "API Routing", "description": "Set up async endpoints and Pydantic validation."}, {"title": "Dependency Injection", "description": "Master auth dependencies and background tasks."}],
    "django": [{"title": "Models & Views", "description": "Understand the ORM and MVT pattern."}, {"title": "Django REST Framework", "description": "Master serializers and viewsets."}],
    "flask": [{"title": "Basic Routing", "description": "Set up a simple Flask application."}, {"title": "Extensions", "description": "Master Flask-SQLAlchemy and Blueprints."}],
    "expressjs": [{"title": "Middleware", "description": "Understand request processing pipeline."}, {"title": "REST Architecture", "description": "Master routing, controllers, and error handling."}],
    "nestjs": [{"title": "Modules & Controllers", "description": "Understand NestJS architecture."}, {"title": "Advanced Providers", "description": "Master Guards, Interceptors, and Microservices."}],
    "spring_boot": [{"title": "Spring Core", "description": "Understand Dependency Injection and Beans."}, {"title": "Data & Security", "description": "Master Spring Data JPA and Spring Security."}],
    "aspnet_core": [{"title": "Web API Basics", "description": "Set up controllers and routing."}, {"title": "Entity Framework", "description": "Master database integration and identity."}],
    "nodejs": [{"title": "Node Modules", "description": "Understand the event loop and core modules."}, {"title": "Streams & Buffers", "description": "Master handling large data asynchronously."}],
    "graphql": [{"title": "Schema Definition", "description": "Create Queries, Mutations, and Types."}, {"title": "Resolvers", "description": "Master data fetching and N+1 problem mitigation."}],
    "rest_api": [{"title": "REST Principles", "description": "Understand HTTP verbs and statelessness."}, {"title": "Advanced API Design", "description": "Master pagination, filtering, and HATEOAS."}],
    "grpc": [{"title": "Protocol Buffers", "description": "Define messages and services in .proto."}, {"title": "Streaming RPCs", "description": "Master bidirectional gRPC streaming."}],
    "websockets": [{"title": "Socket Connection", "description": "Establish a two-way communication channel."}, {"title": "Scaling Websockets", "description": "Master connection state across load balancers."}],
    "microservices": [{"title": "Service Decomposition", "description": "Split a monolith into independent domains."}, {"title": "Inter-Service Communication", "description": "Master event-driven architecture and API Gateways."}],
    "celery": [{"title": "Task Definition", "description": "Set up Celery with a Redis/RabbitMQ broker."}, {"title": "Task Scheduling", "description": "Master Celery Beat and retry mechanisms."}],
    "elixir": [{"title": "Functional Core", "description": "Understand immutability and pattern matching."}, {"title": "OTP & Phoenix", "description": "Master GenServers and concurrent state."}],

    # 4. DATABASES & STORAGE
    "postgresql": [{"title": "Relational Modeling", "description": "Design normalized tables and constraints."}, {"title": "Query Optimization", "description": "Master indexing and execution plans."}],
    "mysql": [{"title": "MySQL Basics", "description": "Understand InnoDB and basic CRUD."}, {"title": "Replication", "description": "Master primary-replica setups and backups."}],
    "mongodb": [{"title": "Document Design", "description": "Model NoSQL data structures."}, {"title": "Aggregation", "description": "Master the MongoDB Aggregation Pipeline."}],
    "redis": [{"title": "Data Structures", "description": "Understand Hashes, Lists, and Sets."}, {"title": "Persistence & Pub/Sub", "description": "Master caching strategies and messaging."}],
    "cassandra": [{"title": "Data Modeling", "description": "Understand partition and clustering keys."}, {"title": "Distributed Architecture", "description": "Master consistency levels and compaction."}],
    "dynamodb": [{"title": "Table Design", "description": "Understand Primary Keys and GSIs."}, {"title": "Single-Table Design", "description": "Master advanced access patterns."}],
    "sqlite": [{"title": "Embedded DB Integration", "description": "Set up a local SQLite file database."}, {"title": "Concurrency Control", "description": "Master WAL mode for better performance."}],
    "neo4j": [{"title": "Graph Modeling", "description": "Design Nodes and Relationships."}, {"title": "Cypher Queries", "description": "Master complex graph traversal."}],
    "elasticsearch": [{"title": "Indexing Documents", "description": "Understand the inverted index."}, {"title": "Complex Queries", "description": "Master aggregations and fuzzy searching."}],
    "opensearch": [{"title": "Cluster Setup", "description": "Initialize an OpenSearch cluster."}, {"title": "Log Analytics", "description": "Master dashboards and anomaly detection."}],
    "cockroachdb": [{"title": "Distributed SQL Setup", "description": "Initialize a multi-node cluster."}, {"title": "Geo-Partitioning", "description": "Master data locality and survivability goals."}],
    "clickhouse": [{"title": "Columnar Basics", "description": "Understand the MergeTree engine."}, {"title": "Analytical Queries", "description": "Master real-time materialized views."}],
    "supabase": [{"title": "Database Setup", "description": "Initialize Postgres and tables."}, {"title": "Row Level Security", "description": "Master RLS policies and Edge Functions."}],
    "firebase": [{"title": "Firestore Basics", "description": "Set up collections and documents."}, {"title": "Security Rules", "description": "Master real-time listeners and security rules."}],
    "snowflake": [{"title": "Data Loading", "description": "Load data via Snowpipe or COPY INTO."}, {"title": "Warehouse Optimization", "description": "Master clustering and time travel."}],

    # 5. MESSAGING & STREAMING
    "kafka": [{"title": "Topics & Partitions", "description": "Understand the commit log architecture."}, {"title": "Kafka Streams", "description": "Master real-time stream processing."}],
    "rabbitmq": [{"title": "Exchanges & Queues", "description": "Understand basic routing configurations."}, {"title": "Resilience", "description": "Master Dead Letter Exchanges and acks."}],
    "apache_pulsar": [{"title": "Tenants & Namespaces", "description": "Set up a multi-tenant environment."}, {"title": "Tiered Storage", "description": "Master BookKeeper integration."}],
    "activemq": [{"title": "JMS Basics", "description": "Implement point-to-point and pub-sub."}, {"title": "Broker Clustering", "description": "Master high-availability setups."}],
    "amazon_sqs": [{"title": "Standard Queues", "description": "Send and receive messages via SDK."}, {"title": "FIFO & DLQ", "description": "Master exact-once processing and failure handling."}],

    # 6. DEVOPS, CLOUD & INFRASTRUCTURE
    "docker": [{"title": "Containerization Basics", "description": "Write a basic Dockerfile."}, {"title": "Docker Compose", "description": "Master multi-container environments."}],
    "kubernetes": [{"title": "Pods & Deployments", "description": "Understand basic K8s objects."}, {"title": "Services & Ingress", "description": "Master networking and auto-scaling."}],
    "terraform": [{"title": "Infrastructure as Code", "description": "Write basic HCL configurations."}, {"title": "State Management", "description": "Master remote state and modules."}],
    "aws": [{"title": "Core Services", "description": "Understand EC2, S3, and IAM."}, {"title": "Serverless Architecture", "description": "Master Lambda, API Gateway, and VPCs."}],
    "azure": [{"title": "Azure Fundamentals", "description": "Deploy an App Service and DB."}, {"title": "Enterprise Networking", "description": "Master VNets, Entra ID, and ARM templates."}],
    "google_cloud": [{"title": "GCP Basics", "description": "Deploy to Cloud Run and Compute Engine."}, {"title": "Data & Identity", "description": "Master IAM and BigQuery integration."}],
    "cloudflare": [{"title": "DNS & CDN Setup", "description": "Configure domain routing and caching."}, {"title": "Edge Compute", "description": "Master Cloudflare Workers and WAF."}],
    "ansible": [{"title": "Inventory & Playbooks", "description": "Write automation scripts for remote servers."}, {"title": "Roles & Galaxy", "description": "Master modular configuration management."}],
    "helm": [{"title": "Chart Basics", "description": "Deploy a pre-existing Helm chart."}, {"title": "Custom Charts", "description": "Master templating your own applications."}],
    "prometheus": [{"title": "Metrics Collection", "description": "Expose and scrape application metrics."}, {"title": "PromQL & Alerts", "description": "Master querying and Alertmanager."}],
    "grafana": [{"title": "Data Source Connection", "description": "Link Grafana to Prometheus/Loki."}, {"title": "Dashboard Design", "description": "Master creating interactive visualization panels."}],
    "datadog": [{"title": "Agent Installation", "description": "Deploy the Datadog agent to a server."}, {"title": "APM & Tracing", "description": "Master distributed tracing and log parsing."}],
    "jenkins": [{"title": "Freestyle Projects", "description": "Set up a basic CI build."}, {"title": "Pipeline as Code", "description": "Master Jenkinsfiles and shared libraries."}],
    "github_actions": [{"title": "Workflow Configuration", "description": "Create a basic YAML CI workflow."}, {"title": "Custom Actions", "description": "Master matrix builds and secrets."}],
    "gitlab_ci": [{"title": "GitLab CI Runner", "description": "Understand .gitlab-ci.yml syntax."}, {"title": "Advanced Pipelines", "description": "Master artifacts, caching, and environments."}],
    "linux": [{"title": "CLI Navigation", "description": "Master basic commands and file permissions."}, {"title": "System Administration", "description": "Master process management and SSH."}],
    "bash": [{"title": "Shell Scripting Basics", "description": "Write scripts with variables and loops."}, {"title": "Text Processing", "description": "Master grep, awk, sed, and pipes."}],
    "nginx": [{"title": "Web Server Config", "description": "Serve static files via NGINX."}, {"title": "Reverse Proxy", "description": "Master load balancing and SSL termination."}],
    "open_telemetry": [{"title": "Instrumentation", "description": "Instrument an app to emit traces."}, {"title": "OTel Collector", "description": "Master configuring exporters to backends."}],
    "hashicorp_vault": [{"title": "Secrets Management", "description": "Store and retrieve static secrets."}, {"title": "Dynamic Secrets", "description": "Master temporary database credential generation."}],

    # 7. AI, MACHINE LEARNING & LLM
    "machine_learning": [{"title": "Data Preprocessing", "description": "Clean and scale datasets."}, {"title": "Model Training", "description": "Master regression, classification, and evaluation metrics."}],
    "deep_learning": [{"title": "Neural Network Basics", "description": "Understand layers and activation functions."}, {"title": "Advanced Architectures", "description": "Master CNNs, RNNs, and Transformers."}],
    "pytorch": [{"title": "Tensors & Autograd", "description": "Perform basic tensor operations."}, {"title": "Custom Models", "description": "Master defining and training nn.Module classes."}],
    "tensorflow": [{"title": "Keras API", "description": "Build models using the Sequential API."}, {"title": "Custom Training Loops", "description": "Master GradientTape and TF Data pipelines."}],
    "openai_api": [{"title": "Chat Completions", "description": "Generate text using the OpenAI API."}, {"title": "Function Calling", "description": "Master structured outputs and tool use."}],
    "anthropic_api": [{"title": "Messages API", "description": "Generate responses using Claude."}, {"title": "Advanced Contexting", "description": "Master vision and long-document processing."}],
    "gemini_api": [{"title": "Multimodal Prompts", "description": "Query the API with text and images."}, {"title": "Advanced Gemini Features", "description": "Master context caching and system instructions."}],
    "prompt_engineering": [{"title": "Basic Prompt Structuring", "description": "Learn zero-shot and few-shot techniques."}, {"title": "Advanced Prompting", "description": "Master Chain-of-Thought and defensive prompting."}],
    "langchain": [{"title": "Chains & Templates", "description": "Build basic LLM interaction chains."}, {"title": "RAG Implementation", "description": "Master Document Loaders and VectorStores in LangChain."}],
    "langgraph": [{"title": "Graph Basics", "description": "Define nodes, edges, and state."}, {"title": "Complex Workflows", "description": "Master cyclic graphs and multi-agent coordination."}],
    "crewai": [{"title": "Agent Roles", "description": "Define Agents, Tasks, and Tools."}, {"title": "Hierarchical Crews", "description": "Master complex multi-agent delegation."}],
    "autogen": [{"title": "Conversational Agents", "description": "Set up a two-agent dialogue."}, {"title": "Code Execution Agents", "description": "Master agents that write and run code."}],
    "model_context_protocol": [{"title": "MCP Client Setup", "description": "Connect an LLM to an MCP server."}, {"title": "Custom MCP Server", "description": "Master exposing local tools via the MCP protocol."}],
    "rag": [{"title": "Naive RAG Architecture", "description": "Implement chunking, embedding, and retrieval."}, {"title": "Advanced RAG", "description": "Master reranking and hybrid search techniques."}],
    "text_embeddings": [{"title": "Generating Embeddings", "description": "Convert text into vector representations."}, {"title": "Vector Math", "description": "Master cosine similarity and clustering concepts."}],
    "faiss": [{"title": "Index Basics", "description": "Create an IndexFlatL2 for exact search."}, {"title": "Approximate Search", "description": "Master IVFFlat and memory optimization."}],
    "chromadb": [{"title": "Local Setup", "description": "Initialize collections and add documents."}, {"title": "Vector Retrieval", "description": "Master similarity search and metadata filtering."}],
    "pinecone": [{"title": "Index Creation", "description": "Set up a serverless vector index."}, {"title": "Production Search", "description": "Master upserting batches and hybrid search queries."}],
    "qdrant": [{"title": "Payload Management", "description": "Insert vectors with complex JSON payloads."}, {"title": "Advanced Filtering", "description": "Master combining semantic search with hard filters."}],
    "milvus": [{"title": "Collection Partitioning", "description": "Define schemas and partitions."}, {"title": "Distributed Search", "description": "Master high-throughput similarity search on Milvus."}],
    "mlops": [{"title": "Experiment Tracking", "description": "Log parameters and metrics with MLflow."}, {"title": "Model Deployment", "description": "Master serving models and monitoring data drift."}],
    "huggingface": [{"title": "Transformers Library", "description": "Load and run pre-trained models."}, {"title": "Fine-Tuning Prep", "description": "Master dataset preparation and the Trainer API."}],
    "fine_tuning": [{"title": "Data Preparation", "description": "Format data for instruction tuning."}, {"title": "PEFT & LoRA", "description": "Master parameter-efficient fine-tuning on consumer hardware."}],
    "vllm": [{"title": "Model Serving", "description": "Deploy an LLM using the vLLM engine."}, {"title": "High-Throughput Optimization", "description": "Master continuous batching and PagedAttention."}],
    "ollama": [{"title": "Local Execution", "description": "Run Llama 3 locally via CLI."}, {"title": "Modelfile Configuration", "description": "Master creating custom system prompts and parameters."}],

    # 8. DATA ENGINEERING
    "apache_spark": [{"title": "RDDs & DataFrames", "description": "Understand basic Spark data structures."}, {"title": "Performance Tuning", "description": "Master partitioning, broadcasting, and Spark SQL."}],
    "apache_airflow": [{"title": "DAG Creation", "description": "Define tasks and dependencies."}, {"title": "Advanced Scheduling", "description": "Master Sensors, XComs, and custom Operators."}],
    "dbt": [{"title": "Model Initialization", "description": "Write basic select statements in dbt."}, {"title": "Advanced dbt", "description": "Master Jinja macros, tests, and materializations."}],
    "apache_flink": [{"title": "Stream Basics", "description": "Understand unbounded data processing."}, {"title": "State & Time", "description": "Master watermarks, event time, and checkpoints."}],
    "databricks": [{"title": "Workspace Navigation", "description": "Run Spark jobs in Databricks notebooks."}, {"title": "Lakehouse Architecture", "description": "Master Unity Catalog and Databricks Jobs."}],
    "delta_lake": [{"title": "Delta Tables", "description": "Convert Parquet files to Delta format."}, {"title": "ACID Operations", "description": "Master Time Travel, OPTIMIZE, and VACUUM."}],
    "pandas": [{"title": "DataFrames Series", "description": "Perform basic data selection and cleaning."}, {"title": "Advanced Aggregation", "description": "Master GroupBy, Merges, and Pivot Tables."}],
    "numpy": [{"title": "NDArray Operations", "description": "Create and manipulate multidimensional arrays."}, {"title": "Vectorization", "description": "Master broadcasting and linear algebra functions."}],
    "etl_pipeline": [{"title": "Pipeline Architecture", "description": "Design an Extract and Load process."}, {"title": "Robust Pipelines", "description": "Master idempotency, backfilling, and error handling."}],
    "polars": [{"title": "Polars Basics", "description": "Load data and use Expressions."}, {"title": "Lazy Evaluation", "description": "Master the LazyFrame API for high-speed processing."}],

    # 9. TESTING & QA
    "pytest": [{"title": "Test Functions", "description": "Write basic assertions and test cases."}, {"title": "Fixtures & Mocking", "description": "Master reusable fixtures and patching."}],
    "jest": [{"title": "Assertions & Matchers", "description": "Write unit tests for JS functions."}, {"title": "Async & Mocks", "description": "Master testing asynchronous code and mocking modules."}],
    "cypress": [{"title": "E2E Basics", "description": "Write a test that interacts with the DOM."}, {"title": "Network Interception", "description": "Master stubbing API requests and custom commands."}],
    "playwright": [{"title": "Browser Automation", "description": "Record and run cross-browser tests."}, {"title": "Advanced Playwright", "description": "Master auto-waiting, trace viewer, and fixtures."}],
    "selenium": [{"title": "WebDriver Setup", "description": "Open browsers and find elements programmatically."}, {"title": "Page Object Model", "description": "Master POM architecture and Explicit Waits."}],
    "mockito": [{"title": "Basic Mocking", "description": "Mock a class and verify a method call."}, {"title": "Advanced Stubbing", "description": "Master argument matchers and InjectMocks."}],
    "junit": [{"title": "JUnit Basics", "description": "Use @Test and lifecycle annotations."}, {"title": "Parameterized Tests", "description": "Master testing multiple inputs and assumptions."}],
    "load_testing_k6": [{"title": "Script Creation", "description": "Write a basic JS load test script."}, {"title": "Advanced Scenarios", "description": "Master thresholds, stages, and custom metrics."}],

    # 10. SECURITY & AUTH
    "oauth2": [{"title": "OAuth Flow Understanding", "description": "Understand roles and token exchange."}, {"title": "Implementation", "description": "Master Authorization Code flow with PKCE."}],
    "jwt": [{"title": "Token Structure", "description": "Understand Headers, Payloads, and Signatures."}, {"title": "Secure Implementation", "description": "Master token expiration and secure cookie storage."}],
    "web_security_owasp": [{"title": "Vulnerability Identification", "description": "Understand XSS, SQLi, and CSRF."}, {"title": "Mitigation Strategies", "description": "Master input validation and security headers."}],
    "zero_trust": [{"title": "Zero Trust Concepts", "description": "Understand continuous verification."}, {"title": "Architecture Implementation", "description": "Master micro-segmentation and Identity Aware Proxies."}],
    "encryption": [{"title": "Cryptography Basics", "description": "Understand Symmetric vs Asymmetric encryption."}, {"title": "Applied Encryption", "description": "Master hashing (Argon2), salts, and TLS setups."}],
    "iam": [{"title": "Identity Basics", "description": "Understand Authentication vs Authorization."}, {"title": "Policy Design", "description": "Master RBAC, ABAC, and Least Privilege principles."}],
    "webauthn": [{"title": "FIDO2 Protocols", "description": "Understand public key credentials."}, {"title": "Passkey Implementation", "description": "Master registration and authentication ceremonies."}],

    # 11. CS & SYSTEM DESIGN
    "data_structures_and_algorithms": [{"title": "Basic Data Structures", "description": "Master Arrays, Hash Maps, and Linked Lists."}, {"title": "Algorithmic Paradigms", "description": "Master Trees, Graphs, and Dynamic Programming."}],
    "system_design": [{"title": "Architecture Basics", "description": "Understand Scalability and Load Balancing."}, {"title": "Distributed Concepts", "description": "Master Sharding, Caching, and Microservices."}],
    "object_oriented_programming": [{"title": "OOP Fundamentals", "description": "Understand Classes and Objects."}, {"title": "Advanced Paradigms", "description": "Master Polymorphism, Inheritance, and Encapsulation."}],
    "functional_programming": [{"title": "Pure Functions", "description": "Understand immutability and side effects."}, {"title": "Advanced FP", "description": "Master Monads, Currying, and Higher-Order Functions."}],
    "solid_principles": [{"title": "SRP & OCP", "description": "Understand Single Responsibility and Open/Closed."}, {"title": "LSP, ISP & DIP", "description": "Master Liskov, Interface Segregation, and Dependency Inversion."}],
    "clean_architecture": [{"title": "Architecture Layers", "description": "Understand Domain vs Infrastructure."}, {"title": "Dependency Rule", "description": "Master the Ports and Adapters (Hexagonal) pattern."}],
    "domain_driven_design": [{"title": "Strategic Design", "description": "Understand Ubiquitous Language and Bounded Contexts."}, {"title": "Tactical Design", "description": "Master Entities, Value Objects, and Aggregates."}],
    "design_patterns": [{"title": "Creational Patterns", "description": "Master Singleton, Factory, and Builder."}, {"title": "Structural & Behavioral", "description": "Master Strategy, Observer, and Decorator patterns."}],
    "concurrency_and_multithreading": [{"title": "Threads & Processes", "description": "Understand OS-level multitasking."}, {"title": "Synchronization", "description": "Master Locks, Mutexes, and avoiding Deadlocks."}],
    "memory_management": [{"title": "Stack vs Heap", "description": "Understand how memory is allocated."}, {"title": "Garbage Collection", "description": "Master GC algorithms and memory leak prevention."}],
    "networking_fundamentals": [{"title": "OSI & TCP/IP", "description": "Understand network layers and protocols."}, {"title": "Application Layer", "description": "Master HTTP/2, DNS resolution, and WebSockets."}],
    "operating_systems": [{"title": "OS Basics", "description": "Understand Kernel, User Space, and System Calls."}, {"title": "Process & Memory", "description": "Master CPU Scheduling and Virtual Memory (Paging)."}],
    "distributed_systems": [{"title": "Distributed Basics", "description": "Understand the CAP Theorem and Network Partitions."}, {"title": "Consensus & Clocks", "description": "Master Raft, Vector Clocks, and distributed transactions."}],
    "performance_optimization": [{"title": "Identifying Bottlenecks", "description": "Master profiling tools and flame graphs."}, {"title": "System Tuning", "description": "Master caching, indexing, and I/O optimization."}],
    "caching_strategies": [{"title": "Caching Fundamentals", "description": "Understand Cache Hits, Misses, and Eviction policies."}, {"title": "Distributed Caching", "description": "Master Cache-Aside, Write-Through, and CDN integration."}],
}

def get_fallback_milestones(skill_name: str) -> List[Dict[str, str]]:
    """Safe fallback for unknown skills to prevent crashes."""
    return get_unknown_milestones(skill_name)

def get_milestones(skill_key: str) -> List[Dict[str, str]]:
    """Retrieves milestones, ensuring a safe fallback if key doesn't exist."""
    milestones = MILESTONE_LIBRARY.get(skill_key)
    return milestones if milestones is not None else get_fallback_milestones(skill_key)
