"""
Skill Knowledge Base containing metadata for the top 150 software engineering skills worldwide (2026).
Includes dynamic fallback handling for unknown skills to guarantee zero runtime failures.
"""

from typing import Any, Dict, List

from app.roadmap.roadmap_defaults import get_unknown_skill_metadata

SKILL_LIBRARY: Dict[str, Dict[str, Any]] = {
    # ==========================================
    # 1. PROGRAMMING LANGUAGES (15)
    # ==========================================
    "python": {
        "name": "Python",
        "category": "Programming Languages",
        "difficulty": "Beginner",
        "estimated_days": 14,
        "xp": 200,
        "description": "High-level, interpreted programming language widely used for web development, AI, data science, and scripting.",
        "topics": ["Syntax & Data Structures", "OOP & Decorators", "Asyncio & Concurrency",
                   "Package Management (Poetry/UV)"]
    },
    "javascript": {
        "name": "JavaScript",
        "category": "Programming Languages",
        "difficulty": "Beginner",
        "estimated_days": 12,
        "xp": 180,
        "description": "Core language of the web, driving interactive client-side and server-side applications.",
        "topics": ["ES6+ Features", "Async/Await & Event Loop", "DOM Manipulation", "Prototypes & Closures"]
    },
    "typescript": {
        "name": "TypeScript",
        "category": "Programming Languages",
        "difficulty": "Intermediate",
        "estimated_days": 14,
        "xp": 220,
        "description": "Typed superset of JavaScript that compiles to plain JavaScript for robust enterprise applications.",
        "topics": ["Type Annotations & Interfaces", "Generics & Utility Types", "Type Narrowing", "TSConfig & Compiler"]
    },
    "java": {
        "name": "Java",
        "category": "Programming Languages",
        "difficulty": "Intermediate",
        "estimated_days": 21,
        "xp": 250,
        "description": "Object-oriented, class-based language used widely in enterprise backends and Android development.",
        "topics": ["JVM Architecture", "Multithreading & Concurrency", "Streams & Lambdas",
                   "Garbage Collection & Memory"]
    },
    "cplusplus": {
        "name": "C++",
        "category": "Programming Languages",
        "difficulty": "Advanced",
        "estimated_days": 30,
        "xp": 350,
        "description": "High-performance systems programming language offering fine-grained memory management and speed.",
        "topics": ["Pointers & Memory Management", "RAII & Smart Pointers", "Templates & STL",
                   "Concurrency & Threading"]
    },
    "csharp": {
        "name": "C#",
        "category": "Programming Languages",
        "difficulty": "Intermediate",
        "estimated_days": 18,
        "xp": 230,
        "description": "Modern multi-paradigm language developed by Microsoft for .NET applications, desktop, and game dev.",
        "topics": ["Async/Await", "LINQ", "Generics & Delegates", "Memory Management & Span<T>"]
    },
    "go": {
        "name": "Go (Golang)",
        "category": "Programming Languages",
        "difficulty": "Intermediate",
        "estimated_days": 14,
        "xp": 240,
        "description": "Statically typed, compiled language created by Google for scalable microservices and cloud infrastructure.",
        "topics": ["Goroutines & Channels", "Interfaces & Composition", "Error Handling", "Memory Allocation & GC"]
    },
    "rust": {
        "name": "Rust",
        "category": "Programming Languages",
        "difficulty": "Advanced",
        "estimated_days": 28,
        "xp": 350,
        "description": "Systems programming language focusing on safety, concurrency, and memory efficiency without a garbage collector.",
        "topics": ["Ownership & Borrowing", "Lifetimes", "Traits & Generics", "Fearless Concurrency"]
    },
    "kotlin": {
        "name": "Kotlin",
        "category": "Programming Languages",
        "difficulty": "Intermediate",
        "estimated_days": 14,
        "xp": 220,
        "description": "Modern language running on the JVM, fully interoperable with Java and primary language for Android.",
        "topics": ["Null Safety", "Coroutines & Flow", "Extension Functions", "Sealed Classes & Data Classes"]
    },
    "swift": {
        "name": "Swift",
        "category": "Programming Languages",
        "difficulty": "Intermediate",
        "estimated_days": 16,
        "xp": 230,
        "description": "Powerful, intuitive programming language developed by Apple for iOS, macOS, watchOS, and visionOS.",
        "topics": ["Protocols & Extensions", "Optionnal Unwrapping", "ARC & Memory", "Swift Concurrency (async/await)"]
    },
    "php": {
        "name": "PHP",
        "category": "Programming Languages",
        "difficulty": "Beginner",
        "estimated_days": 10,
        "xp": 170,
        "description": "Server-side scripting language suited for web development and content management systems.",
        "topics": ["PHP 8+ Modern Features", "Type System", "Composer Package Manager", "OOP & Design Patterns"]
    },
    "ruby": {
        "name": "Ruby",
        "category": "Programming Languages",
        "difficulty": "Beginner",
        "estimated_days": 12,
        "xp": 180,
        "description": "Dynamic, open-source programming language with a focus on simplicity and productivity.",
        "topics": ["Blocks, Procs & Lambdas", "Metaprogramming", "OOP Principles", "Gems & Bundler"]
    },
    "scala": {
        "name": "Scala",
        "category": "Programming Languages",
        "difficulty": "Advanced",
        "estimated_days": 24,
        "xp": 300,
        "description": "High-level language combining object-oriented and functional programming, used in Big Data processing.",
        "topics": ["Functional Programming", "Pattern Matching", "Immutability & Type System", "Akka / Pekko Actors"]
    },
    "r": {
        "name": "R",
        "category": "Programming Languages",
        "difficulty": "Intermediate",
        "estimated_days": 14,
        "xp": 200,
        "description": "Language and environment for statistical computing, graphics, and data analytics.",
        "topics": ["Data Frames & Vectors", "Tidyverse", "Statistical Analysis", "Data Visualization (ggplot2)"]
    },
    "sql_lang": {
        "name": "SQL Language",
        "category": "Programming Languages",
        "difficulty": "Beginner",
        "estimated_days": 8,
        "xp": 160,
        "description": "Domain-specific language used for managing data stored in relational database management systems.",
        "topics": ["Queries & Joins", "Aggregations & Grouping", "Window Functions", "CTEs & Subqueries"]
    },

    # ==========================================
    # 2. FRONTEND DEVELOPMENT (15)
    # ==========================================
    "html5": {
        "name": "HTML5",
        "category": "Frontend Development",
        "difficulty": "Beginner",
        "estimated_days": 5,
        "xp": 120,
        "description": "Standard markup language for document structure on the World Wide Web.",
        "topics": ["Semantic Markup", "Accessibility (ARIA)", "Web Storage API", "Forms & Validation"]
    },
    "css3": {
        "name": "CSS3",
        "category": "Frontend Development",
        "difficulty": "Beginner",
        "estimated_days": 8,
        "xp": 150,
        "description": "Style sheet language used for describing the presentation and layout of web documents.",
        "topics": ["Flexbox & CSS Grid", "Responsive Design & Media Queries", "Animations & Transitions",
                   "CSS Variables"]
    },
    "react": {
        "name": "React 19",
        "category": "Frontend Development",
        "difficulty": "Intermediate",
        "estimated_days": 14,
        "xp": 230,
        "description": "Declarative component-based UI library for building modern web and mobile applications.",
        "topics": ["Hooks & Custom Hooks", "Server Components", "State Management", "Virtual DOM & Reconciliation"]
    },
    "nextjs": {
        "name": "Next.js",
        "category": "Frontend Development",
        "difficulty": "Intermediate",
        "estimated_days": 12,
        "xp": 240,
        "description": "React framework enabling server-side rendering, static site generation, and full-stack capabilities.",
        "topics": ["App Router & Server Actions", "SSR, SSG, & ISR", "API Routes", "SEO & Optimization"]
    },
    "vuejs": {
        "name": "Vue.js",
        "category": "Frontend Development",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 200,
        "description": "Progressive JavaScript framework for building user interfaces and single-page applications.",
        "topics": ["Composition API", "Reactivity System", "Vue Router", "Pinia State Management"]
    },
    "angular": {
        "name": "Angular",
        "category": "Frontend Development",
        "difficulty": "Advanced",
        "estimated_days": 20,
        "xp": 280,
        "description": "Comprehensive platform and framework for building single-page client applications.",
        "topics": ["Dependency Injection", "Signals & Reactivity", "RxJS & Observables",
                   "Modules & Standalone Components"]
    },
    "svelte": {
        "name": "Svelte / SvelteKit",
        "category": "Frontend Development",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 210,
        "description": "Compiler-driven UI framework that compiles components to minimal, high-performance vanilla JS.",
        "topics": ["Runes & Reactivity", "Component Props & Events", "SvelteKit Routing", "Transitions & Animation"]
    },
    "tailwindcss": {
        "name": "Tailwind CSS",
        "category": "Frontend Development",
        "difficulty": "Beginner",
        "estimated_days": 6,
        "xp": 140,
        "description": "Utility-first CSS framework for rapidly building custom UI components without custom CSS.",
        "topics": ["Utility Classes", "Responsive Modifiers", "Theme Customization", "JIT Engine & Directives"]
    },
    "material_ui": {
        "name": "Material UI (MUI)",
        "category": "Frontend Development",
        "difficulty": "Intermediate",
        "estimated_days": 6,
        "xp": 150,
        "description": "React component library implementing Google's Material Design principles.",
        "topics": ["Component Customization", "Theming & Palette", "Grid System", "Emotion / Dynamic Styling"]
    },
    "redux": {
        "name": "Redux Toolkit",
        "category": "Frontend Development",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 180,
        "description": "Predictable state container for JS apps, providing centralized state management.",
        "topics": ["Slices & Reducers", "RTK Query", "Middleware & Async Thunks", "Immer & State Mutation"]
    },
    "vite": {
        "name": "Vite",
        "category": "Frontend Development",
        "difficulty": "Beginner",
        "estimated_days": 4,
        "xp": 130,
        "description": "Next-generation frontend tooling offering fast dev server startup and optimized builds.",
        "topics": ["ES Modules Dev Server", "Rollup Bundling", "Plugin API", "Environment Variables"]
    },
    "webpack": {
        "name": "Webpack",
        "category": "Frontend Development",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 190,
        "description": "Static module bundler for modern JavaScript applications.",
        "topics": ["Loaders & Plugins", "Code Splitting", "Tree Shaking", "Module Federation"]
    },
    "web_components": {
        "name": "Web Components",
        "category": "Frontend Development",
        "difficulty": "Intermediate",
        "estimated_days": 7,
        "xp": 170,
        "description": "Suite of browser technology standards allowing creation of reusable custom HTML tags.",
        "topics": ["Custom Elements", "Shadow DOM", "HTML Templates", "Lit Framework"]
    },
    "webassembly": {
        "name": "WebAssembly (Wasm)",
        "category": "Frontend Development",
        "difficulty": "Advanced",
        "estimated_days": 18,
        "xp": 300,
        "description": "Binary instruction format for a stack-based virtual machine, bringing near-native speed to browsers.",
        "topics": ["Wasm Compilation", "C++/Rust Integration", "Memory Shared Buffers", "WASI"]
    },
    "rxjs": {
        "name": "RxJS",
        "category": "Frontend Development",
        "difficulty": "Advanced",
        "estimated_days": 12,
        "xp": 220,
        "description": "Reactive extensions library for JavaScript using observables to compose asynchronous code.",
        "topics": ["Observables & Observers", "Operators (map, switchMap)", "Subjects & BehaviorSubjects",
                   "Backpressure"]
    },

    # ==========================================
    # 3. BACKEND DEVELOPMENT (15)
    # ==========================================
    "fastapi": {
        "name": "FastAPI",
        "category": "Backend Development",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 220,
        "description": "Modern, high-performance web framework for building APIs with Python 3.8+ based on standard type hints.",
        "topics": ["Async Routes", "Pydantic Schemas", "Dependency Injection", "OpenAPI & Swagger Specs"]
    },
    "django": {
        "name": "Django / Django REST Framework",
        "category": "Backend Development",
        "difficulty": "Intermediate",
        "estimated_days": 16,
        "xp": 240,
        "description": "High-level Python web framework encouraging rapid development and clean pragmatic design.",
        "topics": ["Django ORM & Migrations", "DRF Serializers & ViewSets", "Auth & Permissions", "Middleware"]
    },
    "flask": {
        "name": "Flask",
        "category": "Backend Development",
        "difficulty": "Beginner",
        "estimated_days": 7,
        "xp": 160,
        "description": "Lightweight WSGI web application framework in Python.",
        "topics": ["Routing & Blueprints", "Jinja2 Templating", "Extension Ecosystem", "Application Context"]
    },
    "expressjs": {
        "name": "Express.js",
        "category": "Backend Development",
        "difficulty": "Beginner",
        "estimated_days": 8,
        "xp": 170,
        "description": "Minimalist and flexible Node.js web application framework providing robust features.",
        "topics": ["Middleware Pattern", "RESTful Routing", "Error Handling", "Request Processing"]
    },
    "nestjs": {
        "name": "NestJS",
        "category": "Backend Development",
        "difficulty": "Intermediate",
        "estimated_days": 14,
        "xp": 230,
        "description": "Progressive Node.js framework for building efficient, reliable, and scalable server-side applications.",
        "topics": ["Decorators & Modules", "Dependency Injection", "Guards & Interceptors", "Microservices Module"]
    },
    "spring_boot": {
        "name": "Spring Boot",
        "category": "Backend Development",
        "difficulty": "Advanced",
        "estimated_days": 21,
        "xp": 280,
        "description": "Java-based framework used to create stand-alone, production-grade Spring applications.",
        "topics": ["Spring Core & DI", "Spring Data JPA", "Spring Security", "Actuator & Telemetry"]
    },
    "aspnet_core": {
        "name": "ASP.NET Core",
        "category": "Backend Development",
        "difficulty": "Intermediate",
        "estimated_days": 16,
        "xp": 240,
        "description": "Cross-platform, high-performance framework for building modern cloud-enabled backend applications.",
        "topics": ["Entity Framework Core", "Dependency Injection Container", "Middleware Pipeline", "Minimal APIs"]
    },
    "nodejs": {
        "name": "Node.js Runtime",
        "category": "Backend Development",
        "difficulty": "Intermediate",
        "estimated_days": 12,
        "xp": 200,
        "description": "Asynchronous event-driven JavaScript runtime designed to build scalable network applications.",
        "topics": ["Event Loop & libuv", "Streams & Buffers", "Cluster Module", "Worker Threads"]
    },
    "graphql": {
        "name": "GraphQL",
        "category": "Backend Development",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 210,
        "description": "Query language for APIs and runtime for fulfilling queries with existing data.",
        "topics": ["Schemas & Types", "Resolvers & DataLoader", "Mutations & Subscriptions", "Apollo / Relay"]
    },
    "rest_api": {
        "name": "REST API Architecture",
        "category": "Backend Development",
        "difficulty": "Beginner",
        "estimated_days": 6,
        "xp": 150,
        "description": "Architectural style for designing networked applications using HTTP protocol standard operations.",
        "topics": ["HTTP Verbs & Status Codes", "Resource Naming", "Statelessness & Idempotency",
                   "Pagination & Filtering"]
    },
    "grpc": {
        "name": "gRPC",
        "category": "Backend Development",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 230,
        "description": "High-performance RPC framework built on HTTP/2 and Protocol Buffers for polyglot systems.",
        "topics": ["Protocol Buffers (.proto)", "Streaming RPCs", "Service Definitions", "gRPC Interceptors"]
    },
    "websockets": {
        "name": "WebSockets & Realtime API",
        "category": "Backend Development",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 190,
        "description": "Full-duplex communication channels over a single TCP connection for real-time applications.",
        "topics": ["Handshake Protocol", "Socket.io Integration", "Connection Management", "Scaling Connection State"]
    },
    "microservices": {
        "name": "Microservices Architecture",
        "category": "Backend Development",
        "difficulty": "Advanced",
        "estimated_days": 18,
        "xp": 300,
        "description": "Architectural pattern dividing monolithic apps into loosely coupled, independently deployable services.",
        "topics": ["Service Discovery", "API Gateways", "Event-Driven Communication", "Saga Pattern & Resilience"]
    },
    "celery": {
        "name": "Celery & Task Queues",
        "category": "Backend Development",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 180,
        "description": "Asynchronous task queue/job queue based on distributed message passing in Python.",
        "topics": ["Workers & Tasks", "Brokers (Redis/RabbitMQ)", "Celery Beat Scheduler", "Retry & Fault Tolerance"]
    },
    "elixir": {
        "name": "Elixir / Phoenix",
        "category": "Backend Development",
        "difficulty": "Advanced",
        "estimated_days": 20,
        "xp": 270,
        "description": "Functional language running on the Erlang VM (BEAM), built for low-latency and fault-tolerant systems.",
        "topics": ["BEAM Concurrency & OTP", "GenServer Processes", "Phoenix LiveView", "Pattern Matching"]
    },

    # ==========================================
    # 4. DATABASES & STORAGE (15)
    # ==========================================
    "postgresql": {
        "name": "PostgreSQL",
        "category": "Databases & Storage",
        "difficulty": "Intermediate",
        "estimated_days": 14,
        "xp": 230,
        "description": "Advanced, open-source relational database supporting SQL, JSON indexing, and complex queries.",
        "topics": ["Indexes (B-Tree, GIN, GiST)", "ACID Transactions & Isolation", "JSONB Operations",
                   "Query Optimization & EXPLAIN"]
    },
    "mysql": {
        "name": "MySQL",
        "category": "Databases & Storage",
        "difficulty": "Beginner",
        "estimated_days": 10,
        "xp": 180,
        "description": "Widely deployed relational database management system operating standard SQL.",
        "topics": ["InnoDB Engine", "Indexing Strategies", "Replication & Clustering", "Backup & Recovery"]
    },
    "mongodb": {
        "name": "MongoDB",
        "category": "Databases & Storage",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 200,
        "description": "Document-oriented NoSQL database storing JSON-like documents with dynamic schemas.",
        "topics": ["Document Modeling", "Aggregation Pipeline", "Indexing & Sharding", "Replica Sets"]
    },
    "redis": {
        "name": "Redis",
        "category": "Databases & Storage",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 190,
        "description": "In-memory data structure store used as a database, cache, message broker, and streaming engine.",
        "topics": ["Data Structures (Hashes, Sets, Lists)", "Eviction Policies", "Pub/Sub Messaging",
                   "Redis Cluster & Persistence"]
    },
    "cassandra": {
        "name": "Apache Cassandra",
        "category": "Databases & Storage",
        "difficulty": "Advanced",
        "estimated_days": 16,
        "xp": 280,
        "description": "Distributed NoSQL database designed to handle large amounts of data across many commodity servers.",
        "topics": ["Masterless Architecture", "Consistency Levels (CQL)", "Data Modeling & Partition Keys",
                   "Compaction & SSTables"]
    },
    "dynamodb": {
        "name": "Amazon DynamoDB",
        "category": "Databases & Storage",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 220,
        "description": "Fully managed NoSQL database service that provides fast and predictable performance with seamless scalability.",
        "topics": ["Partition Keys & Sort Keys", "Global & Local Secondary Indexes", "DynamoDB Streams",
                   "Single-Table Design"]
    },
    "sqlite": {
        "name": "SQLite",
        "category": "Databases & Storage",
        "difficulty": "Beginner",
        "estimated_days": 4,
        "xp": 130,
        "description": "Self-contained, serverless, zero-configuration, transactional SQL database engine.",
        "topics": ["File-Based Storage", "WAL Mode", "Embedded Queries", "Pragma Configuration"]
    },
    "neo4j": {
        "name": "Neo4j",
        "category": "Databases & Storage",
        "difficulty": "Intermediate",
        "estimated_days": 12,
        "xp": 230,
        "description": "Graph database management system designed to process complex interconnected networks of data.",
        "topics": ["Cypher Query Language", "Nodes, Relationships & Properties", "Graph Algorithms",
                   "Index-Free Adjacency"]
    },
    "elasticsearch": {
        "name": "Elasticsearch",
        "category": "Databases & Storage",
        "difficulty": "Intermediate",
        "estimated_days": 12,
        "xp": 240,
        "description": "Distributed, RESTful search and analytics engine built on Apache Lucene.",
        "topics": ["Inverted Indexing", "Search Queries & Filters", "Aggregations", "Cluster Node Roles"]
    },
    "opensearch": {
        "name": "OpenSearch",
        "category": "Databases & Storage",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 220,
        "description": "Open-source search and analytics suite derived from Elasticsearch.",
        "topics": ["Index Management", "OpenSearch Dashboards", "Vector Search Plugin", "Log Analytics"]
    },
    "cockroachdb": {
        "name": "CockroachDB",
        "category": "Databases & Storage",
        "difficulty": "Advanced",
        "estimated_days": 14,
        "xp": 260,
        "description": "Cloud-native, distributed SQL database designed for high availability and consistency across regions.",
        "topics": ["Distributed Consensus (Raft)", "Multi-Region Deployments", "PostgreSQL Compatibility",
                   "Serializable Isolation"]
    },
    "clickhouse": {
        "name": "ClickHouse",
        "category": "Databases & Storage",
        "difficulty": "Advanced",
        "estimated_days": 14,
        "xp": 270,
        "description": "Column-oriented DBMS for real-time analytical processing (OLAP) on large datasets.",
        "topics": ["Columnar Storage Mechanics", "MergeTree Engine Family", "Realtime Ingestion",
                   "SQL Analytical Functions"]
    },
    "supabase": {
        "name": "Supabase / PostgREST",
        "category": "Databases & Storage",
        "difficulty": "Beginner",
        "estimated_days": 7,
        "xp": 170,
        "description": "Open-source Firebase alternative based on PostgreSQL providing instant APIs, Auth, and Storage.",
        "topics": ["Row Level Security (RLS)", "Realtime Subscriptions", "Database Functions & Triggers",
                   "Edge Functions"]
    },
    "firebase": {
        "name": "Firebase / Firestore",
        "category": "Databases & Storage",
        "difficulty": "Beginner",
        "estimated_days": 7,
        "xp": 160,
        "description": "Google app development platform offering NoSQL cloud database, Auth, and Cloud Functions.",
        "topics": ["Firestore Document Structure", "Security Rules", "Realtime Listeners", "Offline Persistence"]
    },
    "snowflake": {
        "name": "Snowflake Data Cloud",
        "category": "Databases & Storage",
        "difficulty": "Intermediate",
        "estimated_days": 12,
        "xp": 250,
        "description": "Cloud-built data warehousing platform featuring separate compute and storage layers.",
        "topics": ["Virtual Warehouses", "Data Sharing & Micro-partitions", "Snowpipe", "Time Travel & Cloning"]
    },

    # ==========================================
    # 5. MESSAGING & STREAMING (5)
    # ==========================================
    "kafka": {
        "name": "Apache Kafka",
        "category": "Messaging & Streaming",
        "difficulty": "Advanced",
        "estimated_days": 16,
        "xp": 290,
        "description": "Distributed event streaming platform designed for high-throughput event logs.",
        "topics": ["Topics, Partitions & Offsets", "Producers & Consumer Groups", "Kafka Connect & Streams",
                   "Log Retention"]
    },
    "rabbitmq": {
        "name": "RabbitMQ",
        "category": "Messaging & Streaming",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 220,
        "description": "Reliable message broker supporting multiple messaging protocols (AMQP).",
        "topics": ["Exchanges & Routing Keys", "Queues & Bindings", "Dead Letter Exchanges", "Message Acknowledgments"]
    },
    "apache_pulsar": {
        "name": "Apache Pulsar",
        "category": "Messaging & Streaming",
        "difficulty": "Advanced",
        "estimated_days": 14,
        "xp": 270,
        "description": "Distributed pub-sub messaging and event-streaming platform featuring tiered storage.",
        "topics": ["Multi-tenancy", "BookKeeper Storage", "Functions Architecture", "Geo-replication"]
    },
    "activemq": {
        "name": "Apache ActiveMQ",
        "category": "Messaging & Streaming",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 180,
        "description": "Open source JMS and message broker supporting enterprise enterprise protocols.",
        "topics": ["JMS Specifications", "Point-to-Point vs Pub/Sub", "Message Redelivery", "Broker Clustering"]
    },
    "amazon_sqs": {
        "name": "Amazon SQS & SNS",
        "category": "Messaging & Streaming",
        "difficulty": "Beginner",
        "estimated_days": 6,
        "xp": 160,
        "description": "Fully managed message queuing and pub/sub notification services by AWS.",
        "topics": ["Standard vs FIFO Queues", "Visibility Timeouts", "Dead Letter Queues", "Fanout Pattern with SNS"]
    },

    # ==========================================
    # 6. DEVOPS, CLOUD & INFRASTRUCTURE (20)
    # ==========================================
    "docker": {
        "name": "Docker & Containerization",
        "category": "DevOps & Infrastructure",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 210,
        "description": "Platform for developing, shipping, and running applications inside lightweight isolated containers.",
        "topics": ["Dockerfile Best Practices", "Multi-Stage Builds", "Docker Compose",
                   "Container Networking & Volumes"]
    },
    "kubernetes": {
        "name": "Kubernetes (K8s)",
        "category": "DevOps & Infrastructure",
        "difficulty": "Advanced",
        "estimated_days": 21,
        "xp": 320,
        "description": "Production-grade container orchestration system automating deployment, scaling, and management.",
        "topics": ["Pods, Deployments & Services", "Ingress Controllers", "ConfigMaps & Secrets",
                   "Helm Charts & Operators"]
    },
    "terraform": {
        "name": "HashiCorp Terraform",
        "category": "DevOps & Infrastructure",
        "difficulty": "Intermediate",
        "estimated_days": 12,
        "xp": 240,
        "description": "Infrastructure as Code (IaC) tool to provision and manage cloud infrastructure safely and predictably.",
        "topics": ["HCL Syntax & Modules", "State Management & Remote Backends", "Providers & Resources",
                   "Terraform Plan & Apply Workflow"]
    },
    "aws": {
        "name": "Amazon Web Services (AWS)",
        "category": "DevOps & Infrastructure",
        "difficulty": "Intermediate",
        "estimated_days": 20,
        "xp": 280,
        "description": "Comprehensive cloud platform providing compute, storage, networking, and serverless services.",
        "topics": ["EC2 & S3", "IAM Roles & Security Groups", "Lambda & API Gateway", "VPC Networking"]
    },
    "azure": {
        "name": "Microsoft Azure",
        "category": "DevOps & Infrastructure",
        "difficulty": "Intermediate",
        "estimated_days": 18,
        "xp": 270,
        "description": "Cloud computing platform offering infrastructure, platform, and software services.",
        "topics": ["Azure App Service & Functions", "Azure Entra ID (Active Directory)", "Virtual Networks (VNets)",
                   "Blob Storage"]
    },
    "google_cloud": {
        "name": "Google Cloud Platform (GCP)",
        "category": "DevOps & Infrastructure",
        "difficulty": "Intermediate",
        "estimated_days": 18,
        "xp": 270,
        "description": "Suite of cloud computing services provided by Google for infrastructure, data, and AI.",
        "topics": ["Compute Engine & Cloud Run", "BigQuery", "GKE (Google Kubernetes Engine)", "IAM & Service Accounts"]
    },
    "cloudflare": {
        "name": "Cloudflare Network & Workers",
        "category": "DevOps & Infrastructure",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 190,
        "description": "Global edge network providing security, performance, and serverless compute capabilities.",
        "topics": ["Edge Workers & Pages", "DNS Management & SSL", "WAF & DDoS Mitigation", "R2 & KV Storage"]
    },
    "ansible": {
        "name": "Ansible",
        "category": "DevOps & Infrastructure",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 210,
        "description": "Agentless automation engine for configuration management, application deployment, and orchestration.",
        "topics": ["Playbooks & Tasks", "Inventory Management", "Roles & Galaxy", "Handlers & Templates"]
    },
    "helm": {
        "name": "Helm",
        "category": "DevOps & Infrastructure",
        "difficulty": "Intermediate",
        "estimated_days": 6,
        "xp": 170,
        "description": "Package manager for Kubernetes allowing configuration and deployment of applications.",
        "topics": ["Charts & Templates", "values.yaml Override", "Release Lifecycle", "Chart Repositories"]
    },
    "prometheus": {
        "name": "Prometheus",
        "category": "DevOps & Infrastructure",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 220,
        "description": "Open-source systems monitoring and alerting toolkit with a time-series database.",
        "topics": ["PromQL Queries", "Metrics Types (Counter, Gauge, Histogram)", "Exporters & Scraping",
                   "Alertmanager Configuration"]
    },
    "grafana": {
        "name": "Grafana",
        "category": "DevOps & Infrastructure",
        "difficulty": "Beginner",
        "estimated_days": 6,
        "xp": 160,
        "description": "Multi-platform analytics and interactive visualization web application for telemetry data.",
        "topics": ["Dashboards & Panels", "Data Source Connections", "Alerting Rules", "Loki & Tempo Integration"]
    },
    "datadog": {
        "name": "Datadog",
        "category": "DevOps & Infrastructure",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 200,
        "description": "Observability service providing monitoring of servers, databases, tools, and services.",
        "topics": ["APM & Distributed Tracing", "Synthetic Monitoring", "Log Ingestion & Parsing", "Custom Dashboards"]
    },
    "jenkins": {
        "name": "Jenkins",
        "category": "DevOps & Infrastructure",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 200,
        "description": "Open source automation server enabling developers to build, test, and deploy software.",
        "topics": ["Jenkinsfile Syntax", "Pipeline Stages", "Plugins Ecosystem", "Node & Agent Management"]
    },
    "github_actions": {
        "name": "GitHub Actions",
        "category": "DevOps & Infrastructure",
        "difficulty": "Beginner",
        "estimated_days": 6,
        "xp": 170,
        "description": "CI/CD tool built directly into GitHub for automating software build, test, and release pipelines.",
        "topics": ["Workflows & Triggers", "Matrix Builds", "Custom Actions", "Secrets & Environment Management"]
    },
    "gitlab_ci": {
        "name": "GitLab CI/CD",
        "category": "DevOps & Infrastructure",
        "difficulty": "Intermediate",
        "estimated_days": 7,
        "xp": 180,
        "description": "Integrated continuous integration and continuous delivery engine built into GitLab.",
        "topics": [".gitlab-ci.yml Config", "Runners & Executors", "Artifacts & Caching", "Environments & Deployments"]
    },
    "linux": {
        "name": "Linux System Administration",
        "category": "DevOps & Infrastructure",
        "difficulty": "Intermediate",
        "estimated_days": 12,
        "xp": 220,
        "description": "Core operating system administration, process management, file permissions, and CLI navigation.",
        "topics": ["File Hierarchy & Permissions", "Process Signals & systemd", "User Management",
                   "SSH & System Logging"]
    },
    "bash": {
        "name": "Bash & Shell Scripting",
        "category": "DevOps & Infrastructure",
        "difficulty": "Beginner",
        "estimated_days": 7,
        "xp": 160,
        "description": "Command language and shell scripting for task automation in Unix environments.",
        "topics": ["Variables & Control Flow", "Pipes & Redirection", "Text Processing (awk, sed, grep)",
                   "Script Robustness (set -e)"]
    },
    "nginx": {
        "name": "NGINX",
        "category": "DevOps & Infrastructure",
        "difficulty": "Intermediate",
        "estimated_days": 7,
        "xp": 180,
        "description": "High-performance web server, reverse proxy, load balancer, and HTTP cache.",
        "topics": ["Reverse Proxying", "Load Balancing Algorithms", "SSL/TLS Offloading",
                   "Rate Limiting & Security Headers"]
    },
    "open_telemetry": {
        "name": "OpenTelemetry (OTel)",
        "category": "DevOps & Infrastructure",
        "difficulty": "Advanced",
        "estimated_days": 10,
        "xp": 240,
        "description": "Vendor-neutral observability framework for creating, managing, and exporting telemetry data (traces, metrics, logs).",
        "topics": ["OTel Collector Config", "Context Propagation", "Trace Instrumentation", "Metrics Exporting"]
    },
    "hashicorp_vault": {
        "name": "HashiCorp Vault",
        "category": "DevOps & Infrastructure",
        "difficulty": "Advanced",
        "estimated_days": 10,
        "xp": 250,
        "description": "Secrets management system for securely storing, accessing, and dynamically generating credentials.",
        "topics": ["Secrets Engines", "Authentication Methods", "Policy Creation", "Dynamic Database Credentials"]
    },

    # ==========================================
    # 7. AI, MACHINE LEARNING & LLM ECOSYSTEM (25)
    # ==========================================
    "machine_learning": {
        "name": "Machine Learning Fundamentals",
        "category": "AI & Machine Learning",
        "difficulty": "Intermediate",
        "estimated_days": 21,
        "xp": 300,
        "description": "Algorithms and statistical models that enable systems to perform tasks through pattern extraction.",
        "topics": ["Supervised vs Unsupervised", "Regression & Classification", "Feature Engineering",
                   "Model Evaluation & Cross Validation"]
    },
    "deep_learning": {
        "name": "Deep Learning & Neural Networks",
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "estimated_days": 25,
        "xp": 350,
        "description": "Subfield of ML based on artificial neural networks with multiple layers.",
        "topics": ["Forward/Backpropagation", "CNNs & RNNs", "Transformers Architecture",
                   "Optimization Algorithms (Adam, SGD)"]
    },
    "pytorch": {
        "name": "PyTorch",
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "estimated_days": 20,
        "xp": 320,
        "description": "Open-source machine learning framework emphasizing flexibility and dynamic computation graphs.",
        "topics": ["Tensors & Autograd", "nn.Module & Custom Layers", "DataLoaders & Datasets",
                   "PyTorch Lightning / GPU Acceleration"]
    },
    "tensorflow": {
        "name": "TensorFlow / Keras",
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "estimated_days": 20,
        "xp": 310,
        "description": "End-to-end open-source ecosystem for machine learning and neural network execution.",
        "topics": ["Keras Sequential & Functional APIs", "TensorBoard Debugging", "SavedModel Format",
                   "TF Data Pipeline"]
    },
    "openai_api": {
        "name": "OpenAI API Integration",
        "category": "AI & Machine Learning",
        "difficulty": "Beginner",
        "estimated_days": 5,
        "xp": 180,
        "description": "SDK integration for GPT models, Function Calling, Assistants API, and Structured Outputs.",
        "topics": ["Chat Completion API", "Tool / Function Calling", "Structured Outputs (JSON Schema)",
                   "Tokens & Cost Estimation"]
    },
    "anthropic_api": {
        "name": "Anthropic Claude API",
        "category": "AI & Machine Learning",
        "difficulty": "Beginner",
        "estimated_days": 5,
        "xp": 180,
        "description": "Integration with Claude models featuring long context windows, vision, and system prompt formatting.",
        "topics": ["Messages API", "Claude Tool Use", "Prompt Formatting & System Prompts", "Vision Capabilities"]
    },
    "gemini_api": {
        "name": "Google Gemini API",
        "category": "AI & Machine Learning",
        "difficulty": "Beginner",
        "estimated_days": 5,
        "xp": 180,
        "description": "Multimodal API integration accessing Gemini models for text, audio, image, and code processing.",
        "topics": ["Multimodal Prompts", "Gemini SDK Integration", "Function Calling", "Context Caching"]
    },
    "prompt_engineering": {
        "name": "Prompt Engineering",
        "category": "AI & Machine Learning",
        "difficulty": "Beginner",
        "estimated_days": 5,
        "xp": 150,
        "description": "Techniques for structuring input text to guide Large Language Models to optimal outputs.",
        "topics": ["Zero-shot & Few-shot Prompting", "Chain-of-Thought (CoT)", "System Prompt Framing",
                   "Prompt Injection Defense"]
    },
    "langchain": {
        "name": "LangChain Framework",
        "category": "AI & Machine Learning",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 230,
        "description": "Framework designed to simplify creating applications using large language models.",
        "topics": ["LCEL (LangChain Expression Language)", "Chains & Prompt Templates",
                   "Document Loaders & Text Splitters", "VectorStore Retrievers"]
    },
    "langgraph": {
        "name": "LangGraph Agentic Workflows",
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "estimated_days": 12,
        "xp": 270,
        "description": "Library for building stateful, multi-actor applications with LLMs using graph structures.",
        "topics": ["State Graphs & Nodes", "Human-in-the-loop", "Persistence & Memory", "Multi-Agent Coordination"]
    },
    "crewai": {
        "name": "CrewAI",
        "category": "AI & Machine Learning",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 220,
        "description": "Framework for orchestrating role-playing autonomous AI agents.",
        "topics": ["Agent Roles & Goals", "Tasks & Tools Allocation", "Hierarchical Execution",
                   "Agent Collaboration Protocols"]
    },
    "autogen": {
        "name": "Microsoft AutoGen",
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "estimated_days": 10,
        "xp": 250,
        "description": "Framework for developing LLM applications using multiple conversational agents.",
        "topics": ["Conversational Agents", "Code Execution Environments", "Group Chat Managers",
                   "Custom Agent Interfaces"]
    },
    "model_context_protocol": {
        "name": "Model Context Protocol (MCP)",
        "category": "AI & Machine Learning",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 240,
        "description": "Open standard enabling secure, structured connections between LLMs and local or remote resources.",
        "topics": ["MCP Client & Server Architecture", "Resource & Tool Exposure", "JSON-RPC Protocol Mechanics",
                   "Prompt Templates"]
    },
    "rag": {
        "name": "Retrieval-Augmented Generation (RAG)",
        "category": "AI & Machine Learning",
        "difficulty": "Intermediate",
        "estimated_days": 12,
        "xp": 260,
        "description": "Architecture grounding LLMs on external domain knowledge via vector search retrieval.",
        "topics": ["Chunking Strategies", "Dense Retrieval & Hybrid Search", "Reranking Models",
                   "Evaluation Metrics (RAGAS)"]
    },
    "text_embeddings": {
        "name": "Text Embeddings & Vector Representations",
        "category": "AI & Machine Learning",
        "difficulty": "Intermediate",
        "estimated_days": 7,
        "xp": 200,
        "description": "Numerical vector representations of text capturing semantic relationships.",
        "topics": ["Embedding Models (OpenAI, HuggingFace)", "Cosine Similarity & Distance Metrics", "Dimensionality",
                   "Cross-Encoders"]
    },
    "faiss": {
        "name": "Meta FAISS",
        "category": "AI & Machine Learning",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 210,
        "description": "Library for efficient similarity search and clustering of dense vectors developed by Meta AI.",
        "topics": ["IndexFlatL2 vs IndexIVFFlat", "HNSW Indexing", "GPU Acceleration",
                   "Quantization & Memory Compression"]
    },
    "chromadb": {
        "name": "ChromaDB",
        "category": "AI & Machine Learning",
        "difficulty": "Beginner",
        "estimated_days": 5,
        "xp": 170,
        "description": "Open-source AI-native vector database designed for simple local and cloud deployment.",
        "topics": ["Collections Management", "Filtering & Metadata Queries", "Persistence Setup",
                   "Embedding Functions Integration"]
    },
    "pinecone": {
        "name": "Pinecone",
        "category": "AI & Machine Learning",
        "difficulty": "Intermediate",
        "estimated_days": 7,
        "xp": 200,
        "description": "Serverless vector database designed for enterprise-scale machine learning applications.",
        "topics": ["Serverless Indexes", "Namespaces & Metadata Filtering", "Upserting Vector Batches", "Hybrid Search"]
    },
    "qdrant": {
        "name": "Qdrant",
        "category": "AI & Machine Learning",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 220,
        "description": "Vector similarity search engine and database with extended filtering support.",
        "topics": ["Payload Filtering", "Distance Metrics", "HNSW Graphs", "Snapshot & Cloud Deployment"]
    },
    "milvus": {
        "name": "Milvus",
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "estimated_days": 12,
        "xp": 260,
        "description": "Cloud-native open-source vector database built for scalable vector search.",
        "topics": ["Distributed Architecture", "Collection Partitioning", "Attributed Querying",
                   "Zilliz Cloud Operations"]
    },
    "mlops": {
        "name": "MLOps & Model Lifecycle",
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "estimated_days": 16,
        "xp": 290,
        "description": "Practices for deploying, monitoring, and maintaining machine learning models in production.",
        "topics": ["MLflow Experiment Tracking", "Model Registry", "Data Drift Monitoring",
                   "Model Serving (Triton/vLLM)"]
    },
    "huggingface": {
        "name": "Hugging Face Ecosystem",
        "category": "AI & Machine Learning",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 220,
        "description": "Central hub and open-source library for pretrained transformer models and datasets.",
        "topics": ["Transformers Library", "Datasets API", "Hub Model Hosting", "Accelerate & PEFT"]
    },
    "fine_tuning": {
        "name": "LLM Fine-Tuning & LoRA",
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "estimated_days": 14,
        "xp": 310,
        "description": "Adapting base LLMs to specific tasks using parameter-efficient fine-tuning methods.",
        "topics": ["LoRA & QLoRA", "Instruction Tuning Data Prep", "SFT Trainer", "Quantization (GGUF/AWQ)"]
    },
    "vllm": {
        "name": "vLLM Inference Engine",
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "estimated_days": 8,
        "xp": 260,
        "description": "High-throughput and memory-efficient LLM serving engine featuring PagedAttention.",
        "topics": ["PagedAttention Mechanics", "Continuous Batching", "OpenAI-Compatible Server Setup",
                   "Quantized Model Inference"]
    },
    "ollama": {
        "name": "Ollama Local LLMs",
        "category": "AI & Machine Learning",
        "difficulty": "Beginner",
        "estimated_days": 4,
        "xp": 150,
        "description": "Tool for running open-source large language models locally on individual devices.",
        "topics": ["Modelfile Customization", "CLI Commands", "REST API Endpoints", "Quantization Models Selection"]
    },

    # ==========================================
    # 8. DATA ENGINEERING & BIG DATA (10)
    # ==========================================
    "apache_spark": {
        "name": "Apache Spark / PySpark",
        "category": "Data Engineering",
        "difficulty": "Advanced",
        "estimated_days": 18,
        "xp": 290,
        "description": "Unified analytics engine for large-scale data processing.",
        "topics": ["DataFrame API & RDDs", "Spark SQL", "Spark Streaming", "Memory Tuning & Partitioning"]
    },
    "apache_airflow": {
        "name": "Apache Airflow",
        "category": "Data Engineering",
        "difficulty": "Intermediate",
        "estimated_days": 12,
        "xp": 240,
        "description": "Platform to programmatically author, schedule, and monitor data pipeline workflows.",
        "topics": ["DAGs & Task Dependencies", "Operators & Sensors", "Airflow Executors", "XComs & Task Flow API"]
    },
    "dbt": {
        "name": "dbt (Data Build Tool)",
        "category": "Data Engineering",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 210,
        "description": "Transform data in warehouse using SQL SELECT statements.",
        "topics": ["Models & Materializations", "Jinja Templating", "Data Testing & Documentation", "dbt Lineage DAGs"]
    },
    "apache_flink": {
        "name": "Apache Flink",
        "category": "Data Engineering",
        "difficulty": "Advanced",
        "estimated_days": 16,
        "xp": 300,
        "description": "Framework and distributed processing engine for stateful computations over data streams.",
        "topics": ["Stream Processing vs Batching", "Event Time & Watermarks", "State Backends & Checkpoints",
                   "Flink SQL"]
    },
    "databricks": {
        "name": "Databricks Platform",
        "category": "Data Engineering",
        "difficulty": "Intermediate",
        "estimated_days": 12,
        "xp": 250,
        "description": "Unified analytics platform for big data and machine learning powered by Lakehouse architecture.",
        "topics": ["Delta Lake Mechanics", "Notebook Workflows", "Unity Catalog Governance", "Databricks Jobs"]
    },
    "delta_lake": {
        "name": "Delta Lake",
        "category": "Data Engineering",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 220,
        "description": "Open-source storage layer that brings ACID transactions to Apache Spark and big data workloads.",
        "topics": ["ACID Transactions", "Time Travel", "Schema Enforcement", "Compaction & OPTIMIZE"]
    },
    "pandas": {
        "name": "Pandas",
        "category": "Data Engineering",
        "difficulty": "Beginner",
        "estimated_days": 8,
        "xp": 170,
        "description": "Data manipulation and analysis library for Python providing high-performance data structures.",
        "topics": ["DataFrames & Series", "Data Cleaning & Imputation", "Grouping & Merging", "I/O Operations"]
    },
    "numpy": {
        "name": "NumPy",
        "category": "Data Engineering",
        "difficulty": "Beginner",
        "estimated_days": 6,
        "xp": 150,
        "description": "Fundamental package for scientific computing in Python with powerful N-dimensional arrays.",
        "topics": ["NDArrays & Vectorization", "Broadcasting Rules", "Indexing & Slicing", "Linear Algebra Operations"]
    },
    "etl_pipeline": {
        "name": "ETL / ELT Pipeline Architecture",
        "category": "Data Engineering",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 220,
        "description": "Design patterns for extracting, transforming, and loading data across enterprise data systems.",
        "topics": ["Data Validation & Quality Checks", "Change Data Capture (CDC)", "Batch vs Streaming Pipelines",
                   "Idempotence in Data Pipelines"]
    },
    "polars": {
        "name": "Polars DataFrames",
        "category": "Data Engineering",
        "difficulty": "Intermediate",
        "estimated_days": 6,
        "xp": 190,
        "description": "Lightning-fast DataFrame library written in Rust with parallel processing capability.",
        "topics": ["Lazy vs Eager Execution", "Polars Expression Syntax", "Memory Efficiency", "Streaming Big Datasets"]
    },

    # ==========================================
    # 9. TESTING & QUALITY ASSURANCE (8)
    # ==========================================
    "pytest": {
        "name": "Pytest",
        "category": "Testing & QA",
        "difficulty": "Beginner",
        "estimated_days": 6,
        "xp": 160,
        "description": "Robust Python testing framework for writing clean, readable unit and integration tests.",
        "topics": ["Fixtures & Scope", "Parametrization", "Mocking & Patching", "Coverage Reports"]
    },
    "jest": {
        "name": "Jest",
        "category": "Testing & QA",
        "difficulty": "Beginner",
        "estimated_days": 6,
        "xp": 160,
        "description": "Delightful JavaScript testing framework with a focus on simplicity.",
        "topics": ["Matchers & Assertions", "Mock Functions & Spies", "Async Testing", "Snapshot Testing"]
    },
    "cypress": {
        "name": "Cypress",
        "category": "Testing & QA",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 180,
        "description": "Front end testing tool built for the modern web for end-to-end (E2E) testing.",
        "topics": ["DOM Interactivity", "Network Stubbing & Interception", "Custom Commands",
                   "CI/CD Headless Execution"]
    },
    "playwright": {
        "name": "Playwright",
        "category": "Testing & QA",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 190,
        "description": "Framework for Web Testing and Automation enabling reliable cross-browser end-to-end testing.",
        "topics": ["Cross-Browser Automation", "Auto-Waiting Mechanics", "Trace Viewer", "API Testing Capabilities"]
    },
    "selenium": {
        "name": "Selenium WebDriver",
        "category": "Testing & QA",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 180,
        "description": "Automated testing suite for web applications across browser engines.",
        "topics": ["Page Object Model (POM)", "Explicit & Implicit Waits", "WebDriver Protocols", "Grid Execution"]
    },
    "mockito": {
        "name": "Mockito",
        "category": "Testing & QA",
        "difficulty": "Beginner",
        "estimated_days": 5,
        "xp": 150,
        "description": "Popular mocking framework for unit tests written in Java.",
        "topics": ["Mocking & Stubbing", "Argument Matchers", "Verifying Behavior", "InjectMocks"]
    },
    "junit": {
        "name": "JUnit 5",
        "category": "Testing & QA",
        "difficulty": "Beginner",
        "estimated_days": 5,
        "xp": 150,
        "description": "Standard unit testing framework for Java applications.",
        "topics": ["Annotations (@Test, @BeforeEach)", "Assertions & Assumptions", "Parameterized Tests", "Test Suites"]
    },
    "load_testing_k6": {
        "name": "Grafana k6 Load Testing",
        "category": "Testing & QA",
        "difficulty": "Intermediate",
        "estimated_days": 6,
        "xp": 180,
        "description": "Developer-centric performance and load testing tool scripting in JS.",
        "topics": ["Virtual Users (VUs) & Stages", "Thresholds & Metrics", "HTTP Protocol Scripting",
                   "Load Scenarios Design"]
    },

    # ==========================================
    # 10. SECURITY & AUTHORIZATION (7)
    # ==========================================
    "oauth2": {
        "name": "OAuth 2.0 & OpenID Connect",
        "category": "Security & Auth",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 230,
        "description": "Industry-standard protocol for authorization and identity verification.",
        "topics": ["Authorization Code Flow with PKCE", "Access & Refresh Tokens", "ID Tokens & Claims",
                   "Scopes & Consent"]
    },
    "jwt": {
        "name": "JSON Web Tokens (JWT)",
        "category": "Security & Auth",
        "difficulty": "Beginner",
        "estimated_days": 5,
        "xp": 150,
        "description": "Compact, URL-safe means of representing claims to be transferred between two parties.",
        "topics": ["Header, Payload & Signature", "Symmetric vs Asymmetric Signing", "Expiration & Revocation",
                   "Storage Security (HTTPOnly Cookies)"]
    },
    "web_security_owasp": {
        "name": "OWASP Top 10 Security",
        "category": "Security & Auth",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 220,
        "description": "Standard awareness document representing broad consensus on critical web application vulnerabilities.",
        "topics": ["SQL Injection & XSS", "CSRF Mitigation", "Broken Access Control", "Security Misconfigurations"]
    },
    "zero_trust": {
        "name": "Zero Trust Architecture",
        "category": "Security & Auth",
        "difficulty": "Advanced",
        "estimated_days": 12,
        "xp": 260,
        "description": "Security model requiring strict identity verification for every person and device.",
        "topics": ["Least Privilege Access", "Microsegmentation", "Continuous Verification", "mTLS Authentication"]
    },
    "encryption": {
        "name": "Cryptography & Encryption",
        "category": "Security & Auth",
        "difficulty": "Advanced",
        "estimated_days": 14,
        "xp": 280,
        "description": "Foundational techniques for securing communication using mathematical primitives.",
        "topics": ["Symmetric Encryption (AES)", "Asymmetric Encryption (RSA/ECC)", "Hashing (SHA, Argon2)",
                   "TLS/SSL Protocols"]
    },
    "iam": {
        "name": "Identity & Access Management (IAM)",
        "category": "Security & Auth",
        "difficulty": "Intermediate",
        "estimated_days": 8,
        "xp": 200,
        "description": "Framework of policies and technologies ensuring proper authorization access.",
        "topics": ["RBAC vs ABAC Models", "Principal & Permission Policies", "Privilege Escalation Defense",
                   "Audit Logging"]
    },
    "webauthn": {
        "name": "WebAuthn & Passkeys",
        "category": "Security & Auth",
        "difficulty": "Intermediate",
        "estimated_days": 7,
        "xp": 210,
        "description": "Web standard for authenticating users via public key cryptography without passwords.",
        "topics": ["Public Key Credentials", "Authenticator Types (TouchID, YubiKey)", "Attestation", "FIDO2 Framework"]
    },

    # ==========================================
    # 11. COMPUTER SCIENCE & SYSTEM DESIGN (15)
    # ==========================================
    "data_structures_and_algorithms": {
        "name": "Data Structures & Algorithms",
        "category": "CS Fundamentals",
        "difficulty": "Intermediate",
        "estimated_days": 21,
        "xp": 300,
        "description": "Core methods of organizing data and algorithmic techniques for solving computational problems.",
        "topics": ["Big O Notation", "Arrays, Linked Lists, Trees & Graphs", "Sorting & Searching",
                   "Dynamic Programming"]
    },
    "system_design": {
        "name": "System Design Architecture",
        "category": "CS Fundamentals",
        "difficulty": "Advanced",
        "estimated_days": 21,
        "xp": 350,
        "description": "Designing large-scale, high-availability, distributed systems.",
        "topics": ["Scalability (Vertical vs Horizontal)", "Load Balancing & Caching",
                   "Database Sharding & Replication", "CAP Theorem & Consistency"]
    },
    "object_oriented_programming": {
        "name": "Object-Oriented Programming (OOP)",
        "category": "CS Fundamentals",
        "difficulty": "Beginner",
        "estimated_days": 7,
        "xp": 160,
        "description": "Programming paradigm based on the concept of objects containing data and code.",
        "topics": ["Encapsulation", "Abstraction", "Inheritance", "Polymorphism"]
    },
    "functional_programming": {
        "name": "Functional Programming",
        "category": "CS Fundamentals",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 220,
        "description": "Programming paradigm treating computation as the evaluation of mathematical functions.",
        "topics": ["Pure Functions & Immutability", "First-Class & Higher-Order Functions", "Function Composition",
                   "Currying & Monads"]
    },
    "solid_principles": {
        "name": "SOLID Principles",
        "category": "CS Fundamentals",
        "difficulty": "Intermediate",
        "estimated_days": 6,
        "xp": 180,
        "description": "Five design principles for writing understandable, flexible, and maintainable software.",
        "topics": ["Single Responsibility", "Open/Closed", "Liskov Substitution",
                   "Interface Segregation & Dependency Inversion"]
    },
    "clean_architecture": {
        "name": "Clean Architecture / Hexagonal",
        "category": "CS Fundamentals",
        "difficulty": "Advanced",
        "estimated_days": 12,
        "xp": 260,
        "description": "Software architecture guidelines separating code into distinct concentric layers.",
        "topics": ["Domain Entities", "Use Cases / Interactors", "Ports & Adapters Pattern", "Dependency Rule"]
    },
    "domain_driven_design": {
        "name": "Domain-Driven Design (DDD)",
        "category": "CS Fundamentals",
        "difficulty": "Advanced",
        "estimated_days": 14,
        "xp": 280,
        "description": "Software development approach focusing on modeling complex software based on real business domain.",
        "topics": ["Bounded Contexts", "Ubiquitous Language", "Entities, Value Objects & Aggregates", "Domain Events"]
    },
    "design_patterns": {
        "name": "Software Design Patterns",
        "category": "CS Fundamentals",
        "difficulty": "Intermediate",
        "estimated_days": 12,
        "xp": 230,
        "description": "Reusable solutions to commonly occurring software design problems.",
        "topics": ["Creational (Factory, Singleton, Builder)", "Structural (Adapter, Decorator, Proxy)",
                   "Behavioral (Observer, Strategy, Command)", "Pattern Selection Criteria"]
    },
    "concurrency_and_multithreading": {
        "name": "Concurrency & Multithreading",
        "category": "CS Fundamentals",
        "difficulty": "Advanced",
        "estimated_days": 14,
        "xp": 290,
        "description": "Execution of multiple instruction sequences simultaneously.",
        "topics": ["Threads vs Processes", "Locks, Mutexes & Semaphores", "Race Conditions & Deadlocks",
                   "Atomic Operations & Thread Pools"]
    },
    "memory_management": {
        "name": "Memory Management & Pointers",
        "category": "CS Fundamentals",
        "difficulty": "Advanced",
        "estimated_days": 12,
        "xp": 270,
        "description": "Understanding how application computer memory is allocated, utilized, and freed.",
        "topics": ["Stack vs Heap Memory", "Garbage Collection Algorithms", "Memory Leaks & Profiling",
                   "Virtual Memory & Paging"]
    },
    "networking_fundamentals": {
        "name": "Computer Networking",
        "category": "CS Fundamentals",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 200,
        "description": "Foundational principles governing computer communication across networks.",
        "topics": ["OSI & TCP/IP Models", "HTTP/1.1 vs HTTP/2 vs HTTP/3", "DNS Resolution", "Sockets & TCP Handshake"]
    },
    "operating_systems": {
        "name": "Operating System Concepts",
        "category": "CS Fundamentals",
        "difficulty": "Intermediate",
        "estimated_days": 10,
        "xp": 200,
        "description": "Understanding underlying OS abstractions, scheduling, and system calls.",
        "topics": ["CPU Scheduling Algorithms", "Inter-Process Communication (IPC)", "Virtual Memory",
                   "System Calls & Kernel Space"]
    },
    "distributed_systems": {
        "name": "Distributed Systems Concepts",
        "category": "CS Fundamentals",
        "difficulty": "Advanced",
        "estimated_days": 18,
        "xp": 310,
        "description": "Principles for designing autonomous networked computers that communicate and coordinate.",
        "topics": ["Consensus Algorithms (Raft, Paxos)", "Vector Clocks & Logical Time",
                   "Distributed Transactions (2PC)", "Fault Tolerance & Partitioning"]
    },
    "performance_optimization": {
        "name": "Performance Optimization & Profiling",
        "category": "CS Fundamentals",
        "difficulty": "Advanced",
        "estimated_days": 10,
        "xp": 250,
        "description": "Systematic process of identifying bottlenecks and speeding up software execution.",
        "topics": ["Flame Graphs & CPU Profilers", "Memory Leak Detection", "Database Query Optimization",
                   "Benchmarking Methodologies"]
    },
    "caching_strategies": {
        "name": "Caching Strategies & Patterns",
        "category": "CS Fundamentals",
        "difficulty": "Intermediate",
        "estimated_days": 7,
        "xp": 190,
        "description": "Techniques for storing copies of frequently requested data in fast memory.",
        "topics": ["Cache-Aside, Write-Through & Write-Behind", "Eviction Policies (LRU, LFU)",
                   "Cache Stampede Defense", "CDNs & HTTP Caching"]
    },
}


def get_normalized_skill_key(raw_skill: str) -> str:
    """
    Normalizes a skill name input into a standardized key.
    E.g., "Python 3", "PYTHON", "Python" -> "python"
    """
    if not raw_skill:
        return "unknown_skill"

    cleaned = raw_skill.strip().lower()
    cleaned = cleaned.replace(".", "").replace("-", "_").replace(" ", "_")

    # Direct match check
    if cleaned in SKILL_LIBRARY:
        return cleaned

    # Match versioned or qualified names without allowing short keys such as
    # ``r`` to match arbitrary words like ``quantumforge``.
    related = [
        key for key in SKILL_LIBRARY
        if cleaned.startswith(f"{key}_") or key.startswith(f"{cleaned}_")
    ]
    if related:
        return max(related, key=len)

    return cleaned


def get_fallback_skill_metadata(skill_name: str) -> Dict[str, Any]:
    """
    Generates dynamic default skill metadata when an unknown technology is detected.
    Ensures the application NEVER crashes on unlisted skills.
    """
    return get_unknown_skill_metadata(skill_name)


def get_skill_metadata(skill_key: str) -> Dict[str, Any]:
    """
    Retrieves skill metadata from the library or returns dynamic fallback metadata.
    Guarantees a response for any given input string.
    """
    normalized_key = get_normalized_skill_key(skill_key)
    if normalized_key in SKILL_LIBRARY:
        return SKILL_LIBRARY[normalized_key]

    return get_fallback_skill_metadata(skill_key)
