class LearningRecommendationService:

    ROADMAPS = {
        "java": {
            "priority": "High",
            "learning_time": "3-4 Weeks",
            "roadmap": "Java Basics → OOP → Collections → Spring Boot"
        },
        "spring": {
            "priority": "High",
            "learning_time": "2-3 Weeks",
            "roadmap": "Spring Core → Spring Boot → REST API"
        },
        "spring boot": {
            "priority": "High",
            "learning_time": "2-3 Weeks",
            "roadmap": "Spring Boot → JPA → Security"
        },
        "aws": {
            "priority": "Medium",
            "learning_time": "4 Weeks",
            "roadmap": "EC2 → S3 → IAM → RDS"
        },
        "docker": {
            "priority": "High",
            "learning_time": "1 Week",
            "roadmap": "Images → Containers → Docker Compose"
        },
        "kubernetes": {
            "priority": "High",
            "learning_time": "2-3 Weeks",
            "roadmap": "Pods → Deployments → Services → Helm"
        },
        "flask": {
            "priority": "Medium",
            "learning_time": "1 Week",
            "roadmap": "Flask Basics → Routing → REST API"
        },
        "react": {
            "priority": "High",
            "learning_time": "3 Weeks",
            "roadmap": "JSX → Components → Hooks → API Integration"
        },
        "c": {
            "priority": "Low",
            "learning_time": "2 Weeks",
            "roadmap": "Variables → Functions → Pointers"
        }
    }

    def recommend(self, missing_skills):

        recommendations = []

        for skill in missing_skills:

            if skill in self.ROADMAPS:

                recommendations.append({
                    "skill": skill,
                    "priority": self.ROADMAPS[skill]["priority"],
                    "learning_time": self.ROADMAPS[skill]["learning_time"],
                    "roadmap": self.ROADMAPS[skill]["roadmap"]
                })

        return recommendations