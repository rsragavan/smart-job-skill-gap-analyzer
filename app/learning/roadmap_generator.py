class RoadmapGenerator:

    ROADMAP = {

        "python": {
            "difficulty": "Beginner",
            "days": 20,
            "topics": [
                "Python Basics",
                "Functions",
                "OOP",
                "File Handling"
            ],
            "resource": "https://docs.python.org/3/tutorial/"
        },

        "java": {
            "difficulty": "Beginner",
            "days": 25,
            "topics": [
                "Java Basics",
                "OOP",
                "Collections",
                "Exception Handling"
            ],
            "resource": "https://dev.java/learn/"
        },

        "spring": {
            "difficulty": "Intermediate",
            "days": 25,
            "topics": [
                "Spring Core",
                "Dependency Injection",
                "Spring MVC"
            ],
            "resource": "https://spring.io/guides"
        },

        "spring boot": {
            "difficulty": "Intermediate",
            "days": 20,
            "topics": [
                "REST API",
                "Spring Data JPA",
                "Security"
            ],
            "resource": "https://spring.io/projects/spring-boot"
        },

        "mysql": {
            "difficulty": "Beginner",
            "days": 10,
            "topics": [
                "CRUD",
                "Joins",
                "Indexes"
            ],
            "resource": "https://dev.mysql.com/doc/"
        },

        "postgresql": {
            "difficulty": "Intermediate",
            "days": 10,
            "topics": [
                "SQL",
                "Indexes",
                "JSON",
                "Joins"
            ],
            "resource": "https://www.postgresql.org/docs/"
        },

        "docker": {
            "difficulty": "Intermediate",
            "days": 15,
            "topics": [
                "Images",
                "Containers",
                "Dockerfile",
                "Docker Compose"
            ],
            "resource": "https://docs.docker.com/"
        },

        "git": {
            "difficulty": "Beginner",
            "days": 5,
            "topics": [
                "Commit",
                "Branch",
                "Merge"
            ],
            "resource": "https://git-scm.com/doc"
        },

        "linux": {
            "difficulty": "Intermediate",
            "days": 20,
            "topics": [
                "Linux Commands",
                "Shell",
                "Permissions",
                "Processes"
            ],
            "resource": "https://linuxjourney.com/"
        },

        "aws": {
            "difficulty": "Advanced",
            "days": 30,
            "topics": [
                "EC2",
                "S3",
                "IAM",
                "VPC"
            ],
            "resource": "https://docs.aws.amazon.com/"
        },

        "kubernetes": {
            "difficulty": "Advanced",
            "days": 30,
            "topics": [
                "Pods",
                "Deployments",
                "Services",
                "Ingress"
            ],
            "resource": "https://kubernetes.io/docs/"
        },

        "django": {
            "difficulty": "Intermediate",
            "days": 20,
            "topics": [
                "Models",
                "Views",
                "Templates",
                "REST API"
            ],
            "resource": "https://docs.djangoproject.com/"
        },

        "fastapi": {
            "difficulty": "Intermediate",
            "days": 15,
            "topics": [
                "Routing",
                "Pydantic",
                "Dependency Injection",
                "Swagger"
            ],
            "resource": "https://fastapi.tiangolo.com/"
        },

        "flask": {
            "difficulty": "Beginner",
            "days": 10,
            "topics": [
                "Routing",
                "Templates",
                "Blueprints"
            ],
            "resource": "https://flask.palletsprojects.com/"
        },

        "react": {
            "difficulty": "Intermediate",
            "days": 20,
            "topics": [
                "Components",
                "Hooks",
                "State",
                "Routing"
            ],
            "resource": "https://react.dev/learn"
        },

        "javascript": {
            "difficulty": "Beginner",
            "days": 20,
            "topics": [
                "Variables",
                "Functions",
                "DOM",
                "ES6"
            ],
            "resource": "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
        },

        "html": {
            "difficulty": "Beginner",
            "days": 5,
            "topics": [
                "Elements",
                "Forms",
                "Tables"
            ],
            "resource": "https://developer.mozilla.org/en-US/docs/Web/HTML"
        },

        "css": {
            "difficulty": "Beginner",
            "days": 5,
            "topics": [
                "Selectors",
                "Flexbox",
                "Grid"
            ],
            "resource": "https://developer.mozilla.org/en-US/docs/Web/CSS"
        },

        "sql": {
            "difficulty": "Beginner",
            "days": 15,
            "topics": [
                "SELECT",
                "JOIN",
                "GROUP BY",
                "Indexes"
            ],
            "resource": "https://www.w3schools.com/sql/"
        },

        "c": {
            "difficulty": "Beginner",
            "days": 20,
            "topics": [
                "Variables",
                "Pointers",
                "Functions",
                "Arrays"
            ],
            "resource": "https://www.programiz.com/c-programming"
        }

    }

    def generate(self, missing_skills):

        roadmap = []

        for priority, skill in enumerate(missing_skills, start=1):

            info = self.ROADMAP.get(
                skill.lower(),
                {
                    "difficulty": "Intermediate",
                    "days": 15,
                    "topics": [
                        "Learn Fundamentals",
                        "Practice Projects"
                    ],
                    "resource": "https://www.google.com/search?q=" + skill
                }
            )

            roadmap.append(
                {
                    "skill": skill,
                    "difficulty": info["difficulty"],
                    "estimated_days": info["days"],
                    "priority": priority,
                    "topics": info["topics"],
                    "learning_resource": info["resource"]
                }
            )

        return roadmap
