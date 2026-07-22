export interface RoadmapItemData {
    skill: string;
    difficulty: "Beginner" | "Intermediate" | "Advanced";
    weeks: number;
    weeklyTopics: string[];
    officialDocs: string;
    freeCourse: string;
    practiceProject: string;
}

// Curated roadmap data for missing skills
const skillRoadmapDatabase: Record<string, RoadmapItemData> = {
    // Frontend Skills
    React: {
        skill: "React",
        difficulty: "Intermediate",
        weeks: 4,
        weeklyTopics: [
            "Week 1: Components, JSX, Props, State",
            "Week 2: Hooks (useState, useEffect, useContext)",
            "Week 3: Forms, Lists, Keys, Event Handling",
            "Week 4: Routing, API Integration, Best Practices",
        ],
        officialDocs: "https://react.dev",
        freeCourse: "https://www.freecodecamp.org/learn/front-end-development-libraries/react/",
        practiceProject: "Build a Todo App with Task Filtering & API Integration",
    },
    "Vue.js": {
        skill: "Vue.js",
        difficulty: "Intermediate",
        weeks: 4,
        weeklyTopics: [
            "Week 1: Templates, Directives, Data Binding",
            "Week 2: Components, Props, Emits, Lifecycle",
            "Week 3: Computed Properties, Watchers, Methods",
            "Week 4: Routing, State Management with Pinia",
        ],
        officialDocs: "https://vuejs.org",
        freeCourse: "https://www.freecodecamp.org/learn/front-end-development-libraries/vue/",
        practiceProject: "Build a Notes App with Local Storage & Filtering",
    },
    Angular: {
        skill: "Angular",
        difficulty: "Advanced",
        weeks: 6,
        weeklyTopics: [
            "Week 1: Components, Services, Dependency Injection",
            "Week 2: Templates, Directives, Data Binding",
            "Week 3: Routing, Guards, Lazy Loading",
            "Week 4: Forms (Template & Reactive)",
            "Week 5: HTTP Client, Interceptors, Error Handling",
            "Week 6: Testing, Deployment, Best Practices",
        ],
        officialDocs: "https://angular.io",
        freeCourse: "https://www.freecodecamp.org/learn/front-end-development-libraries/angular/",
        practiceProject: "Build a Full-Featured Dashboard with Real-time Data",
    },
    TypeScript: {
        skill: "TypeScript",
        difficulty: "Intermediate",
        weeks: 3,
        weeklyTopics: [
            "Week 1: Types, Interfaces, Generics, Type Guards",
            "Week 2: Classes, Decorators, Advanced Types",
            "Week 3: Modules, Namespaces, Declaration Files",
        ],
        officialDocs: "https://www.typescriptlang.org",
        freeCourse: "https://www.freecodecamp.org/learn/front-end-development-libraries/typescript/",
        practiceProject: "Refactor a JavaScript Project to TypeScript",
    },
    CSS: {
        skill: "CSS",
        difficulty: "Beginner",
        weeks: 2,
        weeklyTopics: [
            "Week 1: Selectors, Box Model, Flexbox",
            "Week 2: Grid, Responsive Design, Animations",
        ],
        officialDocs: "https://developer.mozilla.org/en-US/docs/Web/CSS",
        freeCourse: "https://www.freecodecamp.org/learn/responsive-web-design/",
        practiceProject: "Create a Responsive Portfolio Website",
    },
    HTML: {
        skill: "HTML",
        difficulty: "Beginner",
        weeks: 1,
        weeklyTopics: [
            "Week 1: Semantic HTML, Forms, Accessibility, SEO",
        ],
        officialDocs: "https://developer.mozilla.org/en-US/docs/Web/HTML",
        freeCourse: "https://www.freecodecamp.org/learn/responsive-web-design/basic-html-and-html5/",
        practiceProject: "Build a Semantic Multi-page Website",
    },

    // Backend Skills
    "Node.js": {
        skill: "Node.js",
        difficulty: "Intermediate",
        weeks: 4,
        weeklyTopics: [
            "Week 1: Event Loop, Modules, File System, Streams",
            "Week 2: Express.js Basics, Routing, Middleware",
            "Week 3: Database Integration, Error Handling",
            "Week 4: Authentication, API Security, Deployment",
        ],
        officialDocs: "https://nodejs.org/en/docs/",
        freeCourse: "https://www.freecodecamp.org/learn/back-end-development-and-apis/",
        practiceProject: "Build a RESTful API with Authentication & Database",
    },
    Python: {
        skill: "Python",
        difficulty: "Beginner",
        weeks: 4,
        weeklyTopics: [
            "Week 1: Data Types, Control Flow, Functions",
            "Week 2: Object-Oriented Programming, Modules",
            "Week 3: File I/O, Exception Handling, Decorators",
            "Week 4: List Comprehensions, Iterators, Generators",
        ],
        officialDocs: "https://docs.python.org/3/",
        freeCourse: "https://www.freecodecamp.org/learn/scientific-computing-with-python/",
        practiceProject: "Build a Web Scraper & Data Analysis Tool",
    },
    Django: {
        skill: "Django",
        difficulty: "Intermediate",
        weeks: 5,
        weeklyTopics: [
            "Week 1: Project Setup, Apps, Models, Migrations",
            "Week 2: ORM Queries, Admin Interface, Relationships",
            "Week 3: Views, URL Routing, Templates",
            "Week 4: Forms, Validation, User Authentication",
            "Week 5: Class-Based Views, REST API, Deployment",
        ],
        officialDocs: "https://docs.djangoproject.com/",
        freeCourse: "https://www.freecodecamp.org/learn/back-end-development-and-apis/",
        practiceProject: "Build a Blog Platform with Comments & User Roles",
    },
    FastAPI: {
        skill: "FastAPI",
        difficulty: "Intermediate",
        weeks: 3,
        weeklyTopics: [
            "Week 1: Application Setup, Path/Query Parameters, Request Bodies",
            "Week 2: Response Models, Status Codes, Dependencies",
            "Week 3: Authentication, Database Integration, Testing",
        ],
        officialDocs: "https://fastapi.tiangolo.com/",
        freeCourse: "https://www.freecodecamp.org/learn/back-end-development-and-apis/",
        practiceProject: "Build a High-Performance REST API with JWT Auth",
    },
    "Express.js": {
        skill: "Express.js",
        difficulty: "Intermediate",
        weeks: 3,
        weeklyTopics: [
            "Week 1: Routing, Middleware, Request/Response Handling",
            "Week 2: Error Handling, Static Files, Templating",
            "Week 3: Authentication, Session Management, Deployment",
        ],
        officialDocs: "https://expressjs.com/",
        freeCourse: "https://www.freecodecamp.org/learn/back-end-development-and-apis/",
        practiceProject: "Build a REST API with Rate Limiting & Caching",
    },

    // Database Skills
    PostgreSQL: {
        skill: "PostgreSQL",
        difficulty: "Intermediate",
        weeks: 3,
        weeklyTopics: [
            "Week 1: Tables, Data Types, Queries, Joins",
            "Week 2: Indexes, Transactions, Constraints",
            "Week 3: Views, Procedures, Performance Tuning",
        ],
        officialDocs: "https://www.postgresql.org/docs/",
        freeCourse: "https://www.freecodecamp.org/learn/relational-database/",
        practiceProject: "Design & Optimize a Relational Database Schema",
    },
    MongoDB: {
        skill: "MongoDB",
        difficulty: "Intermediate",
        weeks: 3,
        weeklyTopics: [
            "Week 1: Collections, Documents, CRUD Operations",
            "Week 2: Aggregation, Indexing, Schema Validation",
            "Week 3: Replication, Sharding, Transactions",
        ],
        officialDocs: "https://docs.mongodb.com/",
        freeCourse: "https://university.mongodb.com/",
        practiceProject: "Build a Document Database with Complex Queries",
    },
    SQL: {
        skill: "SQL",
        difficulty: "Beginner",
        weeks: 2,
        weeklyTopics: [
            "Week 1: SELECT, WHERE, JOINs, GROUP BY",
            "Week 2: Subqueries, Window Functions, Optimization",
        ],
        officialDocs: "https://en.wikipedia.org/wiki/SQL",
        freeCourse: "https://www.freecodecamp.org/learn/relational-database/",
        practiceProject: "Solve Complex SQL Queries & Create Reports",
    },
    Redis: {
        skill: "Redis",
        difficulty: "Intermediate",
        weeks: 2,
        weeklyTopics: [
            "Week 1: Data Structures, Commands, Persistence",
            "Week 2: Pub/Sub, Transactions, Cluster Mode",
        ],
        officialDocs: "https://redis.io/documentation",
        freeCourse: "https://www.freecodecamp.org/learn/back-end-development-and-apis/",
        practiceProject: "Build a Caching Layer for a Web Application",
    },

    // DevOps/Cloud Skills
    Docker: {
        skill: "Docker",
        difficulty: "Intermediate",
        weeks: 3,
        weeklyTopics: [
            "Week 1: Images, Containers, Dockerfile, Registry",
            "Week 2: Networking, Volumes, Environment Variables",
            "Week 3: Docker Compose, Multi-stage Builds, Optimization",
        ],
        officialDocs: "https://docs.docker.com/",
        freeCourse: "https://www.freecodecamp.org/learn/devops/",
        practiceProject: "Containerize a Full-Stack Application",
    },
    Kubernetes: {
        skill: "Kubernetes",
        difficulty: "Advanced",
        weeks: 5,
        weeklyTopics: [
            "Week 1: Pods, Deployments, Services",
            "Week 2: ConfigMaps, Secrets, Volumes",
            "Week 3: Networking, Ingress, Service Mesh",
            "Week 4: StatefulSets, DaemonSets, Jobs",
            "Week 5: Monitoring, Logging, Scaling",
        ],
        officialDocs: "https://kubernetes.io/docs/",
        freeCourse: "https://www.freecodecamp.org/learn/devops/",
        practiceProject: "Deploy a Microservices Architecture to Kubernetes",
    },
    AWS: {
        skill: "AWS",
        difficulty: "Intermediate",
        weeks: 6,
        weeklyTopics: [
            "Week 1: EC2, S3, IAM, VPC",
            "Week 2: RDS, Lambda, DynamoDB",
            "Week 3: CloudFront, Route 53, ELB",
            "Week 4: CloudFormation, CloudWatch, SNS/SQS",
            "Week 5: API Gateway, Cognito, Secrets Manager",
            "Week 6: Best Practices, Cost Optimization, Migration",
        ],
        officialDocs: "https://docs.aws.amazon.com/",
        freeCourse: "https://www.freecodecamp.org/learn/aws-certified-cloud-practitioner/",
        practiceProject: "Design & Deploy a Scalable Application on AWS",
    },
    Azure: {
        skill: "Azure",
        difficulty: "Intermediate",
        weeks: 5,
        weeklyTopics: [
            "Week 1: Virtual Machines, App Service, Databases",
            "Week 2: Storage, Networking, Security",
            "Week 3: Container Instances, Kubernetes Service",
            "Week 4: Functions, Logic Apps, API Management",
            "Week 5: Monitoring, DevOps, Best Practices",
        ],
        officialDocs: "https://docs.microsoft.com/en-us/azure/",
        freeCourse: "https://www.freecodecamp.org/learn/azure/",
        practiceProject: "Deploy a Cloud-Native Application on Azure",
    },
    GCP: {
        skill: "GCP",
        difficulty: "Intermediate",
        weeks: 5,
        weeklyTopics: [
            "Week 1: Compute Engine, Cloud Storage, Cloud SQL",
            "Week 2: Cloud Functions, Firestore, Pub/Sub",
            "Week 3: App Engine, Cloud Run, GKE",
            "Week 4: Networking, Security, IAM",
            "Week 5: Monitoring, Logging, Cost Optimization",
        ],
        officialDocs: "https://cloud.google.com/docs",
        freeCourse: "https://www.freecodecamp.org/learn/google-cloud-associate-cloud-engineer/",
        practiceProject: "Build a Serverless Application on GCP",
    },

    // Version Control
    Git: {
        skill: "Git",
        difficulty: "Beginner",
        weeks: 1,
        weeklyTopics: [
            "Week 1: Commits, Branches, Merging, Rebasing, Remote Repositories",
        ],
        officialDocs: "https://git-scm.com/doc",
        freeCourse: "https://git-scm.com/book/en/v2",
        practiceProject: "Manage a Project Repository with Branching Strategy",
    },

    // Testing
    Jest: {
        skill: "Jest",
        difficulty: "Intermediate",
        weeks: 2,
        weeklyTopics: [
            "Week 1: Test Structure, Assertions, Mocking",
            "Week 2: Async Testing, Snapshots, Coverage",
        ],
        officialDocs: "https://jestjs.io/",
        freeCourse: "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/",
        practiceProject: "Write Comprehensive Unit Tests for a Library",
    },
    Pytest: {
        skill: "Pytest",
        difficulty: "Intermediate",
        weeks: 2,
        weeklyTopics: [
            "Week 1: Fixtures, Markers, Parametrization",
            "Week 2: Mocking, Coverage, Advanced Features",
        ],
        officialDocs: "https://docs.pytest.org/",
        freeCourse: "https://www.freecodecamp.org/learn/scientific-computing-with-python/",
        practiceProject: "Test a Python Application with High Coverage",
    },

    // Other Common Skills
    JavaScript: {
        skill: "JavaScript",
        difficulty: "Beginner",
        weeks: 4,
        weeklyTopics: [
            "Week 1: Variables, Data Types, Operators, Control Flow",
            "Week 2: Functions, Scope, Closures, this Keyword",
            "Week 3: Objects, Arrays, Prototypes, Inheritance",
            "Week 4: Async/Await, Promises, Event Loop, DOM APIs",
        ],
        officialDocs: "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
        freeCourse: "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/",
        practiceProject: "Build an Interactive Web Application",
    },
    "REST API": {
        skill: "REST API",
        difficulty: "Intermediate",
        weeks: 2,
        weeklyTopics: [
            "Week 1: HTTP Methods, Status Codes, Resource Design",
            "Week 2: Authentication, Error Handling, Versioning",
        ],
        officialDocs: "https://restfulapi.net/",
        freeCourse: "https://www.freecodecamp.org/learn/back-end-development-and-apis/",
        practiceProject: "Design & Implement a Well-Structured REST API",
    },
    GraphQL: {
        skill: "GraphQL",
        difficulty: "Intermediate",
        weeks: 3,
        weeklyTopics: [
            "Week 1: Schema, Queries, Mutations, Subscriptions",
            "Week 2: Resolvers, Middleware, Error Handling",
            "Week 3: Performance Optimization, Testing, Deployment",
        ],
        officialDocs: "https://graphql.org/learn/",
        freeCourse: "https://www.freecodecamp.org/learn/back-end-development-and-apis/",
        practiceProject: "Build a GraphQL API with Complex Queries",
    },
    "Machine Learning": {
        skill: "Machine Learning",
        difficulty: "Advanced",
        weeks: 8,
        weeklyTopics: [
            "Week 1: Fundamentals, Linear Algebra, Calculus Review",
            "Week 2: Supervised Learning, Regression, Classification",
            "Week 3: Decision Trees, Ensemble Methods, SVM",
            "Week 4: Unsupervised Learning, Clustering, Dimensionality Reduction",
            "Week 5: Neural Networks, Backpropagation, Activation Functions",
            "Week 6: Deep Learning, CNNs, RNNs, Transformers",
            "Week 7: NLP Basics, Text Processing, Word Embeddings",
            "Week 8: Model Evaluation, Hyperparameter Tuning, Deployment",
        ],
        officialDocs: "https://scikit-learn.org/",
        freeCourse: "https://www.freecodecamp.org/learn/machine-learning-for-everyone/",
        practiceProject: "Build an End-to-End ML Pipeline & Deploy a Model",
    },
    "Data Science": {
        skill: "Data Science",
        difficulty: "Advanced",
        weeks: 6,
        weeklyTopics: [
            "Week 1: Data Collection, Cleaning, Exploration",
            "Week 2: Statistical Analysis, Hypothesis Testing",
            "Week 3: Visualization, Storytelling with Data",
            "Week 4: Feature Engineering, Selection",
            "Week 5: Statistical Models, Regression, Classification",
            "Week 6: Communication, Business Impact, Ethics",
        ],
        officialDocs: "https://pandas.pydata.org/docs/",
        freeCourse: "https://www.freecodecamp.org/learn/data-analysis-with-python/",
        practiceProject: "Analyze a Dataset & Present Actionable Insights",
    },
};

export function getSkillRoadmap(skill: string): RoadmapItemData | null {
    return skillRoadmapDatabase[skill] || null;
}

export function generateRoadmapFromMissingSkills(
    missingSkills: string[]
): RoadmapItemData[] {
    return missingSkills
        .map((skill) => getSkillRoadmap(skill))
        .filter((item): item is RoadmapItemData => item !== null);
}

