"""
app/roadmap/resource_library.py

Resource Knowledge Base mapping skills to learning materials.
Includes dynamic fallback handling for unknown skills.
"""

from typing import Any, Dict, List

from app.roadmap.roadmap_defaults import get_unknown_resources

RESOURCE_LIBRARY: Dict[str, List[Dict[str, str]]] = {
    # 1. PROGRAMMING LANGUAGES
    "python": [{"title": "Official Python Docs", "url": "https://docs.python.org/3/", "type": "Documentation"}, {"title": "Real Python", "url": "https://realpython.com/", "type": "Tutorial"}],
    "javascript": [{"title": "MDN Web Docs", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "type": "Documentation"}, {"title": "JavaScript.info", "url": "https://javascript.info/", "type": "Course"}],
    "typescript": [{"title": "TypeScript Handbook", "url": "https://www.typescriptlang.org/docs/", "type": "Documentation"}, {"title": "Total TypeScript", "url": "https://www.totaltypescript.com/", "type": "Course"}],
    "java": [{"title": "Oracle Java Docs", "url": "https://docs.oracle.com/en/java/", "type": "Documentation"}, {"title": "Baeldung Java", "url": "https://www.baeldung.com/", "type": "Tutorial"}],
    "cplusplus": [{"title": "C++ Reference", "url": "https://en.cppreference.com/w/", "type": "Documentation"}, {"title": "LearnCpp", "url": "https://www.learncpp.com/", "type": "Tutorial"}],
    "csharp": [{"title": "Microsoft C# Docs", "url": "https://learn.microsoft.com/en-us/dotnet/csharp/", "type": "Documentation"}, {"title": "Code Maze C#", "url": "https://code-maze.com/csharp-basics/", "type": "Tutorial"}],
    "go": [{"title": "Effective Go", "url": "https://go.dev/doc/effective_go", "type": "Documentation"}, {"title": "Go by Example", "url": "https://gobyexample.com/", "type": "Tutorial"}],
    "rust": [{"title": "The Rust Book", "url": "https://doc.rust-lang.org/book/", "type": "Documentation"}, {"title": "Rust by Example", "url": "https://doc.rust-lang.org/rust-by-example/", "type": "Tutorial"}],
    "kotlin": [{"title": "Kotlin Official Docs", "url": "https://kotlinlang.org/docs/home.html", "type": "Documentation"}, {"title": "Kotlin Koans", "url": "https://play.kotlinlang.org/koans/", "type": "Interactive"}],
    "swift": [{"title": "Swift.org", "url": "https://www.swift.org/documentation/", "type": "Documentation"}, {"title": "Hacking with Swift", "url": "https://www.hackingwithswift.com/", "type": "Course"}],
    "php": [{"title": "PHP Manual", "url": "https://www.php.net/manual/en/", "type": "Documentation"}, {"title": "PHP The Right Way", "url": "https://phptherightway.com/", "type": "Guide"}],
    "ruby": [{"title": "Ruby Docs", "url": "https://www.ruby-lang.org/en/documentation/", "type": "Documentation"}, {"title": "Ruby on Rails Guides", "url": "https://guides.rubyonrails.org/", "type": "Guide"}],
    "scala": [{"title": "Scala Documentation", "url": "https://docs.scala-lang.org/", "type": "Documentation"}, {"title": "Rock the JVM", "url": "https://rockthejvm.com/", "type": "Course"}],
    "r": [{"title": "R Project Manuals", "url": "https://cran.r-project.org/manuals.html", "type": "Documentation"}, {"title": "R for Data Science", "url": "https://r4ds.had.co.nz/", "type": "Book"}],
    "sql_lang": [{"title": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "type": "Tutorial"}, {"title": "Use The Index, Luke", "url": "https://use-the-index-luke.com/", "type": "Guide"}],

    # 2. FRONTEND DEVELOPMENT
    "html5": [{"title": "MDN HTML", "url": "https://developer.mozilla.org/en-US/docs/Web/HTML", "type": "Documentation"}, {"title": "HTML.com", "url": "https://html.com/", "type": "Tutorial"}],
    "css3": [{"title": "CSS Tricks", "url": "https://css-tricks.com/", "type": "Guide"}, {"title": "MDN CSS", "url": "https://developer.mozilla.org/en-US/docs/Web/CSS", "type": "Documentation"}],
    "react": [{"title": "React.dev", "url": "https://react.dev/", "type": "Documentation"}, {"title": "Epic React", "url": "https://epicreact.dev/", "type": "Course"}],
    "nextjs": [{"title": "Next.js Docs", "url": "https://nextjs.org/docs", "type": "Documentation"}, {"title": "Next.js Learn", "url": "https://nextjs.org/learn", "type": "Tutorial"}],
    "vuejs": [{"title": "Vue.js Docs", "url": "https://vuejs.org/guide/introduction.html", "type": "Documentation"}, {"title": "Vue Mastery", "url": "https://www.vuemastery.com/", "type": "Course"}],
    "angular": [{"title": "Angular Docs", "url": "https://angular.dev/", "type": "Documentation"}, {"title": "Tour of Heroes", "url": "https://angular.io/tutorial", "type": "Tutorial"}],
    "svelte": [{"title": "Svelte Docs", "url": "https://svelte.dev/docs", "type": "Documentation"}, {"title": "Svelte Tutorial", "url": "https://svelte.dev/tutorial", "type": "Interactive"}],
    "tailwindcss": [{"title": "Tailwind Docs", "url": "https://tailwindcss.com/docs", "type": "Documentation"}, {"title": "Tailwind Labs YouTube", "url": "https://www.youtube.com/c/TailwindLabs", "type": "Video"}],
    "material_ui": [{"title": "MUI Documentation", "url": "https://mui.com/material-ui/getting-started/", "type": "Documentation"}],
    "redux": [{"title": "Redux Toolkit", "url": "https://redux-toolkit.js.org/", "type": "Documentation"}],
    "vite": [{"title": "Vite Guide", "url": "https://vitejs.dev/guide/", "type": "Documentation"}],
    "webpack": [{"title": "Webpack Concepts", "url": "https://webpack.js.org/concepts/", "type": "Documentation"}],
    "web_components": [{"title": "Web Components Org", "url": "https://www.webcomponents.org/introduction", "type": "Documentation"}],
    "webassembly": [{"title": "Wasm Docs", "url": "https://webassembly.org/getting-started/developers-guide/", "type": "Documentation"}],
    "rxjs": [{"title": "Learn RxJS", "url": "https://www.learnrxjs.io/", "type": "Tutorial"}],

    # 3. BACKEND DEVELOPMENT
    "fastapi": [{"title": "FastAPI Docs", "url": "https://fastapi.tiangolo.com/", "type": "Documentation"}],
    "django": [{"title": "Django Docs", "url": "https://docs.djangoproject.com/", "type": "Documentation"}],
    "flask": [{"title": "Flask Mega-Tutorial", "url": "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world", "type": "Tutorial"}],
    "expressjs": [{"title": "Express Guide", "url": "https://expressjs.com/en/guide/routing.html", "type": "Documentation"}],
    "nestjs": [{"title": "NestJS Docs", "url": "https://docs.nestjs.com/", "type": "Documentation"}],
    "spring_boot": [{"title": "Spring Guides", "url": "https://spring.io/guides", "type": "Tutorial"}],
    "aspnet_core": [{"title": "ASP.NET Core Docs", "url": "https://learn.microsoft.com/en-us/aspnet/core/", "type": "Documentation"}],
    "nodejs": [{"title": "Node.js Docs", "url": "https://nodejs.org/en/docs/", "type": "Documentation"}],
    "graphql": [{"title": "How to GraphQL", "url": "https://www.howtographql.com/", "type": "Course"}],
    "rest_api": [{"title": "REST API Tutorial", "url": "https://restfulapi.net/", "type": "Guide"}],
    "grpc": [{"title": "gRPC Official Docs", "url": "https://grpc.io/docs/", "type": "Documentation"}],
    "websockets": [{"title": "MDN WebSockets", "url": "https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API", "type": "Documentation"}],
    "microservices": [{"title": "Microservices by Martin Fowler", "url": "https://martinfowler.com/articles/microservices.html", "type": "Article"}],
    "celery": [{"title": "Celery Docs", "url": "https://docs.celeryq.dev/en/stable/", "type": "Documentation"}],
    "elixir": [{"title": "Elixir School", "url": "https://elixirschool.com/en/", "type": "Tutorial"}],

    # 4. DATABASES & STORAGE
    "postgresql": [{"title": "PostgreSQL Tutorial", "url": "https://www.postgresqltutorial.com/", "type": "Tutorial"}],
    "mysql": [{"title": "MySQL Tutorial", "url": "https://www.mysqltutorial.org/", "type": "Tutorial"}],
    "mongodb": [{"title": "MongoDB University", "url": "https://learn.mongodb.com/", "type": "Course"}],
    "redis": [{"title": "Redis University", "url": "https://university.redis.com/", "type": "Course"}],
    "cassandra": [{"title": "Cassandra Basics", "url": "https://cassandra.apache.org/doc/latest/", "type": "Documentation"}],
    "dynamodb": [{"title": "DynamoDB Guide", "url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html", "type": "Documentation"}],
    "sqlite": [{"title": "SQLite Docs", "url": "https://www.sqlite.org/docs.html", "type": "Documentation"}],
    "neo4j": [{"title": "GraphAcademy", "url": "https://graphacademy.neo4j.com/", "type": "Course"}],
    "elasticsearch": [{"title": "Elastic Getting Started", "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html", "type": "Documentation"}],
    "opensearch": [{"title": "OpenSearch Docs", "url": "https://opensearch.org/docs/latest/", "type": "Documentation"}],
    "cockroachdb": [{"title": "CockroachDB University", "url": "https://university.cockroachlabs.com/", "type": "Course"}],
    "clickhouse": [{"title": "ClickHouse Docs", "url": "https://clickhouse.com/docs/", "type": "Documentation"}],
    "supabase": [{"title": "Supabase Docs", "url": "https://supabase.com/docs", "type": "Documentation"}],
    "firebase": [{"title": "Firebase Fundamentals", "url": "https://firebase.google.com/docs", "type": "Documentation"}],
    "snowflake": [{"title": "Snowflake Quickstarts", "url": "https://quickstarts.snowflake.com/", "type": "Tutorial"}],

    # 5. MESSAGING & STREAMING
    "kafka": [{"title": "Kafka Documentation", "url": "https://kafka.apache.org/documentation/", "type": "Documentation"}],
    "rabbitmq": [{"title": "RabbitMQ Tutorials", "url": "https://www.rabbitmq.com/getstarted.html", "type": "Tutorial"}],
    "apache_pulsar": [{"title": "Pulsar Docs", "url": "https://pulsar.apache.org/docs/", "type": "Documentation"}],
    "activemq": [{"title": "ActiveMQ Getting Started", "url": "https://activemq.apache.org/getting-started", "type": "Documentation"}],
    "amazon_sqs": [{"title": "AWS SQS Developer Guide", "url": "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html", "type": "Documentation"}],

    # 6. DEVOPS, CLOUD & INFRASTRUCTURE
    "docker": [{"title": "Docker 101", "url": "https://docs.docker.com/get-started/", "type": "Tutorial"}],
    "kubernetes": [{"title": "K8s Basics", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/", "type": "Tutorial"}],
    "terraform": [{"title": "HashiCorp Learn Terraform", "url": "https://developer.hashicorp.com/terraform/tutorials", "type": "Course"}],
    "aws": [{"title": "AWS Skill Builder", "url": "https://skillbuilder.aws/", "type": "Course"}],
    "azure": [{"title": "Microsoft Learn Azure", "url": "https://learn.microsoft.com/en-us/training/azure/", "type": "Course"}],
    "google_cloud": [{"title": "GCP Cloud Skills", "url": "https://cloud.google.com/training", "type": "Course"}],
    "cloudflare": [{"title": "Cloudflare Docs", "url": "https://developers.cloudflare.com/", "type": "Documentation"}],
    "ansible": [{"title": "Ansible Getting Started", "url": "https://docs.ansible.com/ansible/latest/getting_started/index.html", "type": "Documentation"}],
    "helm": [{"title": "Helm Docs", "url": "https://helm.sh/docs/", "type": "Documentation"}],
    "prometheus": [{"title": "Prometheus Docs", "url": "https://prometheus.io/docs/introduction/overview/", "type": "Documentation"}],
    "grafana": [{"title": "Grafana Tutorials", "url": "https://grafana.com/tutorials/", "type": "Tutorial"}],
    "datadog": [{"title": "Datadog Learning Center", "url": "https://learn.datadoghq.com/", "type": "Course"}],
    "jenkins": [{"title": "Jenkins Pipeline", "url": "https://www.jenkins.io/doc/book/pipeline/", "type": "Documentation"}],
    "github_actions": [{"title": "GitHub Actions Docs", "url": "https://docs.github.com/en/actions", "type": "Documentation"}],
    "gitlab_ci": [{"title": "GitLab CI/CD Docs", "url": "https://docs.gitlab.com/ee/ci/", "type": "Documentation"}],
    "linux": [{"title": "Linux Journey", "url": "https://linuxjourney.com/", "type": "Interactive"}],
    "bash": [{"title": "Bash Scripting Tutorial", "url": "https://linuxconfig.org/bash-scripting-tutorial-for-beginners", "type": "Tutorial"}],
    "nginx": [{"title": "NGINX Beginner's Guide", "url": "https://nginx.org/en/docs/beginners_guide.html", "type": "Guide"}],
    "open_telemetry": [{"title": "OpenTelemetry Docs", "url": "https://opentelemetry.io/docs/", "type": "Documentation"}],
    "hashicorp_vault": [{"title": "Vault Tutorials", "url": "https://developer.hashicorp.com/vault/tutorials", "type": "Tutorial"}],

    # 7. AI, MACHINE LEARNING & LLM
    "machine_learning": [{"title": "Google ML Crash Course", "url": "https://developers.google.com/machine-learning/crash-course", "type": "Course"}],
    "deep_learning": [{"title": "Fast.ai", "url": "https://course.fast.ai/", "type": "Course"}],
    "pytorch": [{"title": "PyTorch Tutorials", "url": "https://pytorch.org/tutorials/", "type": "Tutorial"}],
    "tensorflow": [{"title": "TensorFlow Guide", "url": "https://www.tensorflow.org/guide", "type": "Documentation"}],
    "openai_api": [{"title": "OpenAI Platform Docs", "url": "https://platform.openai.com/docs/", "type": "Documentation"}],
    "anthropic_api": [{"title": "Anthropic Claude Docs", "url": "https://docs.anthropic.com/claude/docs", "type": "Documentation"}],
    "gemini_api": [{"title": "Google Gemini API Docs", "url": "https://ai.google.dev/docs", "type": "Documentation"}],
    "prompt_engineering": [{"title": "Learn Prompting", "url": "https://learnprompting.org/", "type": "Course"}],
    "langchain": [{"title": "LangChain Docs", "url": "https://python.langchain.com/docs/get_started/introduction", "type": "Documentation"}],
    "langgraph": [{"title": "LangGraph Docs", "url": "https://python.langchain.com/docs/langgraph", "type": "Documentation"}],
    "crewai": [{"title": "CrewAI Docs", "url": "https://docs.crewai.com/", "type": "Documentation"}],
    "autogen": [{"title": "Microsoft AutoGen", "url": "https://microsoft.github.io/autogen/", "type": "Documentation"}],
    "model_context_protocol": [{"title": "MCP Specification", "url": "https://modelcontextprotocol.io/", "type": "Documentation"}],
    "rag": [{"title": "RAG Tutorial (Pinecone)", "url": "https://www.pinecone.io/learn/retrieval-augmented-generation/", "type": "Guide"}],
    "text_embeddings": [{"title": "Understanding Embeddings", "url": "https://huggingface.co/blog/getting-started-with-embeddings", "type": "Article"}],
    "faiss": [{"title": "FAISS Wiki", "url": "https://github.com/facebookresearch/faiss/wiki", "type": "Documentation"}],
    "chromadb": [{"title": "Chroma Docs", "url": "https://docs.trychroma.com/", "type": "Documentation"}],
    "pinecone": [{"title": "Pinecone Learning Center", "url": "https://www.pinecone.io/learn/", "type": "Course"}],
    "qdrant": [{"title": "Qdrant Documentation", "url": "https://qdrant.tech/documentation/", "type": "Documentation"}],
    "milvus": [{"title": "Milvus Bootcamp", "url": "https://milvus.io/bootcamp/", "type": "Tutorial"}],
    "mlops": [{"title": "MLOps Guide", "url": "https://ml-ops.org/", "type": "Guide"}],
    "huggingface": [{"title": "Hugging Face Course", "url": "https://huggingface.co/course/chapter1/1", "type": "Course"}],
    "fine_tuning": [{"title": "LoRA & Fine-Tuning Guide", "url": "https://huggingface.co/docs/peft/index", "type": "Documentation"}],
    "vllm": [{"title": "vLLM Docs", "url": "https://vllm.readthedocs.io/", "type": "Documentation"}],
    "ollama": [{"title": "Ollama GitHub", "url": "https://github.com/ollama/ollama", "type": "Documentation"}],

    # 8. DATA ENGINEERING
    "apache_spark": [{"title": "Spark Documentation", "url": "https://spark.apache.org/docs/latest/", "type": "Documentation"}],
    "apache_airflow": [{"title": "Airflow Tutorial", "url": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html", "type": "Tutorial"}],
    "dbt": [{"title": "dbt Fundamentals", "url": "https://courses.getdbt.com/courses/fundamentals", "type": "Course"}],
    "apache_flink": [{"title": "Flink Training", "url": "https://nightlies.apache.org/flink/flink-docs-stable/docs/learn/", "type": "Tutorial"}],
    "databricks": [{"title": "Databricks Academy", "url": "https://customer-academy.databricks.com/", "type": "Course"}],
    "delta_lake": [{"title": "Delta Lake Docs", "url": "https://docs.delta.io/latest/index.html", "type": "Documentation"}],
    "pandas": [{"title": "Pandas Getting Started", "url": "https://pandas.pydata.org/docs/getting_started/index.html", "type": "Documentation"}],
    "numpy": [{"title": "NumPy Quickstart", "url": "https://numpy.org/doc/stable/user/quickstart.html", "type": "Documentation"}],
    "etl_pipeline": [{"title": "Data Engineering Zoomcamp", "url": "https://github.com/DataTalksClub/data-engineering-zoomcamp", "type": "Course"}],
    "polars": [{"title": "Polars User Guide", "url": "https://pola-rs.github.io/polars-book/", "type": "Documentation"}],

    # 9. TESTING & QA
    "pytest": [{"title": "Pytest Docs", "url": "https://docs.pytest.org/en/stable/", "type": "Documentation"}],
    "jest": [{"title": "Jest Getting Started", "url": "https://jestjs.io/docs/getting-started", "type": "Documentation"}],
    "cypress": [{"title": "Cypress Learn", "url": "https://learn.cypress.io/", "type": "Course"}],
    "playwright": [{"title": "Playwright Docs", "url": "https://playwright.dev/docs/intro", "type": "Documentation"}],
    "selenium": [{"title": "Selenium Documentation", "url": "https://www.selenium.dev/documentation/", "type": "Documentation"}],
    "mockito": [{"title": "Mockito Site", "url": "https://site.mockito.org/", "type": "Documentation"}],
    "junit": [{"title": "JUnit 5 User Guide", "url": "https://junit.org/junit5/docs/current/user-guide/", "type": "Documentation"}],
    "load_testing_k6": [{"title": "k6 Documentation", "url": "https://k6.io/docs/", "type": "Documentation"}],

    # 10. SECURITY & AUTH
    "oauth2": [{"title": "OAuth 2.0 Simplified", "url": "https://aaronparecki.com/oauth-2-simplified/", "type": "Guide"}],
    "jwt": [{"title": "JWT Introduction", "url": "https://jwt.io/introduction", "type": "Guide"}],
    "web_security_owasp": [{"title": "OWASP Top 10", "url": "https://owasp.org/www-project-top-ten/", "type": "Documentation"}],
    "zero_trust": [{"title": "NIST Zero Trust Architecture", "url": "https://csrc.nist.gov/publications/detail/sp/800-207/final", "type": "Guide"}],
    "encryption": [{"title": "Applied Cryptography Concepts", "url": "https://cryptography.io/en/latest/", "type": "Documentation"}],
    "iam": [{"title": "AWS IAM Best Practices", "url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html", "type": "Guide"}],
    "webauthn": [{"title": "WebAuthn Guide", "url": "https://webauthn.guide/", "type": "Guide"}],

    # 11. CS & SYSTEM DESIGN
    "data_structures_and_algorithms": [{"title": "NeetCode", "url": "https://neetcode.io/", "type": "Course"}],
    "system_design": [{"title": "ByteByteGo System Design", "url": "https://bytebytego.com/", "type": "Course"}],
    "object_oriented_programming": [{"title": "Refactoring Guru OOP", "url": "https://refactoring.guru/oop", "type": "Guide"}],
    "functional_programming": [{"title": "Mostly Adequate Guide to FP", "url": "https://mostly-adequate.gitbook.io/mostly-adequate-guide/", "type": "Book"}],
    "solid_principles": [{"title": "SOLID Principles Guide", "url": "https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design", "type": "Article"}],
    "clean_architecture": [{"title": "Clean Coder Blog", "url": "https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html", "type": "Article"}],
    "domain_driven_design": [{"title": "DDD Reference", "url": "https://domainlanguage.com/ddd/reference/", "type": "Documentation"}],
    "design_patterns": [{"title": "Refactoring Guru Patterns", "url": "https://refactoring.guru/design-patterns", "type": "Guide"}],
    "concurrency_and_multithreading": [{"title": "Concurrency in Python", "url": "https://realpython.com/python-concurrency/", "type": "Tutorial"}],
    "memory_management": [{"title": "Memory Management Reference", "url": "https://memorymanagement.org/", "type": "Guide"}],
    "networking_fundamentals": [{"title": "High Performance Browser Networking", "url": "https://hpbn.co/", "type": "Book"}],
    "operating_systems": [{"title": "OSTEP Book", "url": "https://pages.cs.wisc.edu/~remzi/OSTEP/", "type": "Book"}],
    "distributed_systems": [{"title": "Distributed Systems for Fun and Profit", "url": "http://book.mixu.net/distsys/", "type": "Book"}],
    "performance_optimization": [{"title": "Brendan Gregg's Performance Tuning", "url": "https://www.brendangregg.com/linuxperf.html", "type": "Guide"}],
    "caching_strategies": [{"title": "AWS Caching Best Practices", "url": "https://aws.amazon.com/caching/best-practices/", "type": "Guide"}],
}

def get_fallback_resources(skill_name: str) -> List[Dict[str, str]]:
    """Safe fallback for unknown skills to prevent crashes."""
    return get_unknown_resources(skill_name)

def get_resources(skill_key: str) -> List[Dict[str, str]]:
    """Retrieves resources, ensuring a safe fallback if key doesn't exist."""
    resources = RESOURCE_LIBRARY.get(skill_key)
    return resources if resources is not None else get_fallback_resources(skill_key)

