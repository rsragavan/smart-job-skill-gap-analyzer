"""
app/roadmap/project_library.py

Project Knowledge Base for hands-on learning tasks.
Includes dynamic fallback handling for unknown skills.
"""

from typing import Any, Dict, List

from app.roadmap.roadmap_defaults import get_unknown_projects

PROJECT_LIBRARY: Dict[str, List[Dict[str, str]]] = {
    # 1. PROGRAMMING LANGUAGES
    "python": [{"title": "Data Analytics CLI App", "description": "Build a command-line tool parsing CSVs with standard libraries."}],
    "javascript": [{"title": "Interactive To-Do List", "description": "Create a vanilla JS app using DOM manipulation and LocalStorage."}],
    "typescript": [{"title": "Strongly-Typed API Wrapper", "description": "Write a TS wrapper for a public API with complete interface types."}],
    "java": [{"title": "Banking System API", "description": "Implement a multithreaded bank account management system in Java."}],
    "cplusplus": [{"title": "Custom Memory Allocator", "description": "Build a custom allocator in C++ to manage memory efficiently."}],
    "csharp": [{"title": "Inventory Management WPF App", "description": "Create a desktop app with LINQ and Entity Framework."}],
    "go": [{"title": "Concurrent Log Parser", "description": "Use Goroutines and Channels to process large log files concurrently."}],
    "rust": [{"title": "Multithreaded Web Server", "description": "Build a fast, memory-safe web server from scratch in Rust."}],
    "kotlin": [{"title": "Android Habit Tracker", "description": "Use Coroutines and Room database to track daily user habits."}],
    "swift": [{"title": "iOS Weather App", "description": "Fetch weather APIs using Swift Concurrency and SwiftUI."}],
    "php": [{"title": "MVC Blog Engine", "description": "Build a simple Content Management System using raw PHP 8 OOP."}],
    "ruby": [{"title": "Web Scraper Gem", "description": "Create a Ruby Gem that scrapes and parses e-commerce product data."}],
    "scala": [{"title": "Functional Data Processor", "description": "Process JSON datasets using pure functional programming in Scala."}],
    "r": [{"title": "COVID-19 Data Dashboard", "description": "Use R and ggplot2 to visualize public health datasets."}],
    "sql_lang": [{"title": "E-Commerce Database Schema", "description": "Design tables, relationships, and analytical views for a store."}],

    # 2. FRONTEND DEVELOPMENT
    "html5": [{"title": "Accessible Portfolio Form", "description": "Create a semantic HTML5 portfolio with strict ARIA standards."}],
    "css3": [{"title": "CSS Grid Dashboard", "description": "Design a responsive analytics dashboard using only CSS Grid and Flexbox."}],
    "react": [{"title": "Movie Search Application", "description": "Build a React app with hooks fetching from TMDB API."}],
    "nextjs": [{"title": "SEO-Optimized Tech Blog", "description": "Deploy a statically generated blog using Next.js App Router."}],
    "vuejs": [{"title": "Real-time Chat UI", "description": "Build a reactive chat interface using Vue 3 Composition API."}],
    "angular": [{"title": "Enterprise CRM Dashboard", "description": "Create a complex data-table CRM with Angular reactive forms."}],
    "svelte": [{"title": "Crypto Price Tracker", "description": "Build a lightning-fast price tracker using SvelteKit."}],
    "tailwindcss": [{"title": "Landing Page Clone", "description": "Recreate Stripe's landing page using utility-first Tailwind classes."}],
    "material_ui": [{"title": "Admin Settings Panel", "description": "Build a styled settings UI component using MUI."}],
    "redux": [{"title": "E-Commerce Shopping Cart", "description": "Manage cart state and product inventory using Redux Toolkit."}],
    "vite": [{"title": "Custom Vite Plugin", "description": "Create a plugin that compresses images during the Vite build process."}],
    "webpack": [{"title": "Optimized Production Build", "description": "Configure Webpack for tree-shaking, code splitting, and caching."}],
    "web_components": [{"title": "Custom Data Table Element", "description": "Build a reusable `<data-table>` web component using Shadow DOM."}],
    "webassembly": [{"title": "Image Processing Filter", "description": "Write a C/Rust function compiled to Wasm to filter images in browser."}],
    "rxjs": [{"title": "Auto-Complete Search Box", "description": "Use RxJS to debounce and switchMap HTTP requests."}],

    # 3. BACKEND DEVELOPMENT
    "fastapi": [{"title": "Async Machine Learning API", "description": "Serve an ML model asynchronously using FastAPI and Pydantic."}],
    "django": [{"title": "Social Media Backend", "description": "Build models, views, and DRF endpoints for a Twitter clone."}],
    "flask": [{"title": "URL Shortener Service", "description": "Create a lightweight URL shortening service with Flask and Redis."}],
    "expressjs": [{"title": "RESTful Task API", "description": "Build a complete CRUD API with Express and middleware error handling."}],
    "nestjs": [{"title": "Microservice Architecture API", "description": "Set up a NestJS backend utilizing Dependency Injection and Guards."}],
    "spring_boot": [{"title": "Employee Management API", "description": "Develop a Spring Boot REST API with Spring Data JPA."}],
    "aspnet_core": [{"title": "Real-time Bidding Platform", "description": "Build an auction backend utilizing ASP.NET Core and SignalR."}],
    "nodejs": [{"title": "CLI Build Tool", "description": "Write a Node.js script using the 'fs' module to scaffold projects."}],
    "graphql": [{"title": "GraphQL E-Commerce Gateway", "description": "Implement an Apollo GraphQL server merging multiple REST APIs."}],
    "rest_api": [{"title": "API Design Specification", "description": "Design a fully compliant OpenAPI spec for a logistics system."}],
    "grpc": [{"title": "Polyglot Microservices", "description": "Connect a Go backend and a Python microservice using gRPC."}],
    "websockets": [{"title": "Live Collaborative Whiteboard", "description": "Sync drawing coordinates across clients via WebSockets."}],
    "microservices": [{"title": "Event-Driven Order System", "description": "Build separate Order, Payment, and Inventory microservices."}],
    "celery": [{"title": "Background Email Sender", "description": "Offload bulk email sending to a Celery worker queue."}],
    "elixir": [{"title": "Fault-Tolerant Chat Node", "description": "Build a distributed chat system utilizing Phoenix and BEAM."}],

    # 4. DATABASES & STORAGE
    "postgresql": [{"title": "Advanced Query Optimization", "description": "Use EXPLAIN ANALYZE to optimize queries using B-Tree and GIN indexes."}],
    "mysql": [{"title": "High-Availability Cluster Setup", "description": "Configure MySQL primary-replica replication."}],
    "mongodb": [{"title": "IoT Data Aggregation", "description": "Use MongoDB Aggregation Pipelines to analyze time-series sensor data."}],
    "redis": [{"title": "Leaderboard API Cache", "description": "Build a real-time gaming leaderboard using Redis Sorted Sets."}],
    "cassandra": [{"title": "Distributed Event Logger", "description": "Model a Cassandra keyspace for high-write-throughput logging."}],
    "dynamodb": [{"title": "Single-Table Design Forum", "description": "Design a DynamoDB schema to hold Users, Threads, and Replies."}],
    "sqlite": [{"title": "Embedded App Database", "description": "Integrate SQLite into a desktop application for offline sync."}],
    "neo4j": [{"title": "Social Recommendation Engine", "description": "Write Cypher queries to suggest friends-of-friends in Neo4j."}],
    "elasticsearch": [{"title": "Full-Text Search Engine", "description": "Index documents and build a fuzzy-search autocomplete API."}],
    "opensearch": [{"title": "Log Analytics Dashboard", "description": "Ingest and visualize application logs using OpenSearch Dashboards."}],
    "cockroachdb": [{"title": "Multi-Region Financial Ledger", "description": "Deploy a distributed database ensuring serializable consistency."}],
    "clickhouse": [{"title": "Real-time Ad Analytics", "description": "Ingest millions of ad clicks and write high-speed aggregate queries."}],
    "supabase": [{"title": "Serverless SaaS Backend", "description": "Build a SaaS backend using Supabase RLS policies and Edge Functions."}],
    "firebase": [{"title": "Real-time Location Tracker", "description": "Sync map markers across users using Firestore realtime listeners."}],
    "snowflake": [{"title": "Data Warehouse Transformation", "description": "Load JSON data into Snowflake and build analytical views."}],

    # 5. MESSAGING & STREAMING
    "kafka": [{"title": "Clickstream Processor", "description": "Produce and consume high-throughput web analytics events using Kafka."}],
    "rabbitmq": [{"title": "Task Distribution System", "description": "Use RabbitMQ Fanout exchanges to distribute work to multiple workers."}],
    "apache_pulsar": [{"title": "Geo-Replicated Messaging", "description": "Configure an Apache Pulsar cluster across two regions."}],
    "activemq": [{"title": "Enterprise JMS Integration", "description": "Integrate a Java billing system with ActiveMQ topics."}],
    "amazon_sqs": [{"title": "Decoupled Image Processor", "description": "Use AWS SQS and Lambda to decouple image upload from processing."}],

    # 6. DEVOPS, CLOUD & INFRASTRUCTURE
    "docker": [{"title": "Multi-Container Web App", "description": "Dockerize a Node.js app, Redis cache, and Postgres DB with Docker Compose."}],
    "kubernetes": [{"title": "Highly Available Deployment", "description": "Deploy a microservice to K8s with auto-scaling and Ingress routing."}],
    "terraform": [{"title": "Automated Cloud Infrastructure", "description": "Provision an AWS VPC, EC2, and RDS entirely through Terraform IaC."}],
    "aws": [{"title": "Serverless Image Recognition API", "description": "Combine API Gateway, Lambda, and Rekognition on AWS."}],
    "azure": [{"title": "Azure Functions Backend", "description": "Deploy a serverless HTTP triggered function interacting with CosmosDB."}],
    "google_cloud": [{"title": "GCP Data Pipeline", "description": "Automate a data flow utilizing Cloud Storage, Pub/Sub, and BigQuery."}],
    "cloudflare": [{"title": "Edge URL Shortener", "description": "Build a globally distributed URL shortener utilizing Cloudflare Workers & KV."}],
    "ansible": [{"title": "Automated Server Provisioning", "description": "Write Ansible playbooks to securely configure an NGINX web server."}],
    "helm": [{"title": "Custom Helm Chart", "description": "Package a microservice architecture into a deployable Helm chart."}],
    "prometheus": [{"title": "Application Metrics Exporter", "description": "Instrument a Go service to expose custom metrics to Prometheus."}],
    "grafana": [{"title": "System Observability Dashboard", "description": "Connect Grafana to Prometheus to visualize CPU and API latency."}],
    "datadog": [{"title": "Distributed Tracing Setup", "description": "Integrate Datadog APM into a microservice network to trace requests."}],
    "jenkins": [{"title": "Automated CI/CD Pipeline", "description": "Write a Jenkinsfile to build, test, and push a Docker image on commit."}],
    "github_actions": [{"title": "Automated NPM Publisher", "description": "Create an action that runs tests and publishes a package on release."}],
    "gitlab_ci": [{"title": "Multi-Stage Deployment Pipeline", "description": "Configure GitLab CI to deploy to Staging, then Production via manual gate."}],
    "linux": [{"title": "Secure Web Server Config", "description": "Harden a Linux server with UFW, Fail2Ban, and SSH key authentication."}],
    "bash": [{"title": "Automated Backup Script", "description": "Write a bash script that compresses directories and uploads to S3."}],
    "nginx": [{"title": "Load Balancer & Reverse Proxy", "description": "Configure NGINX to distribute traffic across three application nodes."}],
    "open_telemetry": [{"title": "OTel Tracing Integration", "description": "Instrument a Node and Python service to pass distributed trace context."}],
    "hashicorp_vault": [{"title": "Dynamic Database Credentials", "description": "Configure Vault to issue short-lived, dynamic Postgres credentials."}],

    # 7. AI, MACHINE LEARNING & LLM
    "machine_learning": [{"title": "House Price Predictor", "description": "Train a Random Forest regression model on the Ames Housing dataset."}],
    "deep_learning": [{"title": "Image Classifier Neural Network", "description": "Build a Convolutional Neural Network (CNN) to classify images."}],
    "pytorch": [{"title": "Custom Transformer Model", "description": "Implement a scaled-down Transformer architecture from scratch in PyTorch."}],
    "tensorflow": [{"title": "Time-Series Forecasting", "description": "Use Keras LSTMs to predict future stock prices based on historical data."}],
    "openai_api": [{"title": "AI Support Chatbot", "description": "Build an intelligent assistant using OpenAI Function Calling and GPT-4."}],
    "anthropic_api": [{"title": "Long-Document Analyzer", "description": "Use Claude's large context window to extract insights from financial reports."}],
    "gemini_api": [{"title": "Multimodal Image Describer", "description": "Send images and text to Gemini API to generate accessible alt-text."}],
    "prompt_engineering": [{"title": "Chain-of-Thought Evaluator", "description": "Design prompts that force the LLM to explain its reasoning step-by-step."}],
    "langchain": [{"title": "Document Q&A Chain", "description": "Build an app that answers questions based on uploaded PDFs using LangChain."}],
    "langgraph": [{"title": "Stateful Multi-Actor Agent", "description": "Create a cyclical graphing agent that fact-checks its own outputs."}],
    "crewai": [{"title": "Automated Marketing Team", "description": "Set up a Crew of AI agents (Researcher, Writer, Editor) to generate blogs."}],
    "autogen": [{"title": "Code-Writing Agent Network", "description": "Deploy two agents that write, execute, and fix Python code collaboratively."}],
    "model_context_protocol": [{"title": "MCP Local Database Tool", "description": "Build an MCP server exposing local SQL query execution to an LLM."}],
    "rag": [{"title": "Enterprise Knowledge Base RAG", "description": "Build a Retrieval-Augmented Generation pipeline over internal company docs."}],
    "text_embeddings": [{"title": "Semantic Search Engine", "description": "Convert documents to embeddings and use cosine similarity to search them."}],
    "faiss": [{"title": "Millions-Scale Vector Search", "description": "Index 1M vectors using FAISS and perform sub-millisecond similarity lookups."}],
    "chromadb": [{"title": "Local RAG Vector Store", "description": "Integrate ChromaDB to store and retrieve contextual chunks for a chatbot."}],
    "pinecone": [{"title": "Serverless Semantic Product Search", "description": "Push product catalog embeddings to Pinecone for intelligent search."}],
    "qdrant": [{"title": "Filtered Vector Search", "description": "Implement hybrid search combining dense vectors and metadata filters in Qdrant."}],
    "milvus": [{"title": "Scalable Image Retrieval", "description": "Store image feature vectors in Milvus to build a reverse-image search API."}],
    "mlops": [{"title": "Automated Model Retraining", "description": "Set up MLflow and Airflow to track model drift and trigger retraining."}],
    "huggingface": [{"title": "Pretrained Sentiment Analyzer", "description": "Download and utilize a RoBERTa model from the Hugging Face Hub."}],
    "fine_tuning": [{"title": "Domain-Specific LLM (LoRA)", "description": "Fine-tune a Llama 3 model on medical QA datasets using QLoRA."}],
    "vllm": [{"title": "High-Throughput LLM Server", "description": "Deploy a quantized LLM utilizing vLLM's PagedAttention for fast API serving."}],
    "ollama": [{"title": "Local Code Assistant API", "description": "Run a local instance of Ollama to serve a private coding assistant."}],

    # 8. DATA ENGINEERING
    "apache_spark": [{"title": "Big Data Log Analyzer", "description": "Process gigabytes of server logs using PySpark DataFrames on a cluster."}],
    "apache_airflow": [{"title": "Automated Daily ETL DAG", "description": "Schedule a pipeline to extract API data, transform it, and load to a warehouse."}],
    "dbt": [{"title": "Warehouse Data Modeling", "description": "Write dbt SQL models to clean and join raw tables into analytics-ready views."}],
    "apache_flink": [{"title": "Real-time Fraud Detection", "description": "Process a stream of transaction events in Flink to flag anomalies instantly."}],
    "databricks": [{"title": "Lakehouse Analytics Pipeline", "description": "Build a unified batch and streaming pipeline using Databricks Notebooks."}],
    "delta_lake": [{"title": "ACID Data Lake Transformation", "description": "Implement time-travel and schema enforcement on a Spark dataset."}],
    "pandas": [{"title": "Data Cleaning Script", "description": "Handle missing values, outliers, and type casting on a messy CSV dataset."}],
    "numpy": [{"title": "Matrix Operations Library", "description": "Perform high-speed vectorized linear algebra computations without loops."}],
    "etl_pipeline": [{"title": "End-to-End ELT Architecture", "description": "Extract data via Python, load into Snowflake, and transform via dbt."}],
    "polars": [{"title": "High-Performance Data Aggregation", "description": "Rewrite a slow Pandas script in Polars to achieve 10x speedup."}],

    # 9. TESTING & QA
    "pytest": [{"title": "API Test Suite", "description": "Write Pytest fixtures to mock a database and test FastAPI endpoints."}],
    "jest": [{"title": "Component Unit Tests", "description": "Test React component state and snapshot rendering using Jest."}],
    "cypress": [{"title": "End-to-End Checkout Flow", "description": "Automate a browser test completing an e-commerce checkout in Cypress."}],
    "playwright": [{"title": "Cross-Browser Automation", "description": "Write Playwright scripts to ensure a web app works in Chromium, WebKit, and Firefox."}],
    "selenium": [{"title": "Automated Form Submitter", "description": "Use Selenium WebDriver to scrape and interact with dynamic legacy web forms."}],
    "mockito": [{"title": "Mocking Java Dependencies", "description": "Use Mockito to isolate a Java Service layer from its Database Repository."}],
    "junit": [{"title": "Java Business Logic Tests", "description": "Write comprehensive JUnit 5 parameterized tests for algorithmic logic."}],
    "load_testing_k6": [{"title": "API Load Stress Test", "description": "Simulate 10,000 concurrent users hitting a REST API using Grafana k6."}],

    # 10. SECURITY & AUTH
    "oauth2": [{"title": "Social Login Integration", "description": "Implement Google and GitHub OAuth2 login in a web application."}],
    "jwt": [{"title": "Stateless Auth API", "description": "Generate, sign, and verify JWTs to protect backend API routes."}],
    "web_security_owasp": [{"title": "Vulnerability Scanner", "description": "Audit an application and patch SQLi, XSS, and CSRF vulnerabilities."}],
    "zero_trust": [{"title": "Micro-Segmented Architecture", "description": "Design a network layout where internal services must authenticate via mTLS."}],
    "encryption": [{"title": "Secure Password Storage", "description": "Implement Argon2 hashing and AES encryption for sensitive user data."}],
    "iam": [{"title": "Role-Based Access Control", "description": "Build a middleware system enforcing Admin, Editor, and Viewer permissions."}],
    "webauthn": [{"title": "Passkey Authentication Flow", "description": "Implement biometric WebAuthn login using the browser's credentials API."}],

    # 11. CS & SYSTEM DESIGN
    "data_structures_and_algorithms": [{"title": "Custom Hash Map", "description": "Implement a high-performance Hash Map handling collisions from scratch."}],
    "system_design": [{"title": "Design a Ride-Sharing App", "description": "Draw an architecture diagram for an Uber-like system (DB, Cache, Queues)."}],
    "object_oriented_programming": [{"title": "Chess Game Engine", "description": "Model pieces, boards, and game rules using OOP encapsulation."}],
    "functional_programming": [{"title": "Pure Function Pipeline", "description": "Refactor a heavily mutated state machine into pure, composable functions."}],
    "solid_principles": [{"title": "Legacy Code Refactoring", "description": "Take a monolith file and refactor it applying the 5 SOLID principles."}],
    "clean_architecture": [{"title": "Hexagonal Service App", "description": "Build an app separating the domain core from HTTP adapters and DB ports."}],
    "domain_driven_design": [{"title": "E-Commerce Domain Model", "description": "Define Bounded Contexts and Aggregates for a complex retail business."}],
    "design_patterns": [{"title": "Pattern Library Implementation", "description": "Implement Factory, Observer, and Strategy patterns in a single app."}],
    "concurrency_and_multithreading": [{"title": "Thread-Safe Web Crawler", "description": "Build a multithreaded crawler using Mutex locks to prevent race conditions."}],
    "memory_management": [{"title": "C++ Memory Leak Debugger", "description": "Use Valgrind to identify and fix memory leaks in a manual-allocation app."}],
    "networking_fundamentals": [{"title": "Custom TCP Chat Server", "description": "Build a raw TCP socket server and client allowing users to chat."}],
    "operating_systems": [{"title": "Simple Process Scheduler", "description": "Simulate a Round-Robin CPU scheduling algorithm in Python/C."}],
    "distributed_systems": [{"title": "Distributed Key-Value Store", "description": "Build a simple KV store using a consensus algorithm like Raft."}],
    "performance_optimization": [{"title": "Bottleneck Profiling", "description": "Profile a sluggish Python API using cProfile and optimize it by 500%."}],
    "caching_strategies": [{"title": "Multi-Tier Caching System", "description": "Implement a local in-memory cache backed by a distributed Redis cache."}],
}

def get_fallback_projects(skill_name: str) -> List[Dict[str, str]]:
    """Safe fallback for unknown skills to prevent crashes."""
    return get_unknown_projects(skill_name)

def get_projects(skill_key: str) -> List[Dict[str, str]]:
    """Retrieves projects, ensuring a safe fallback if key doesn't exist."""
    projects = PROJECT_LIBRARY.get(skill_key)
    return projects if projects is not None else get_fallback_projects(skill_key)
