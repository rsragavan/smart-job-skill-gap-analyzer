from app.services.learning_recommendation_service import LearningRecommendationService

service = LearningRecommendationService()

missing = [
    "kubernetes",
    "aws",
    "react"
]

result = service.recommend(missing)

for item in result:
    print(item)