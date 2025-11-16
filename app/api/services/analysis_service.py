# app/api/services/analysis_service.py

import app.modules.analysis.featureBuilder as featureBuilder
import app.modules.analysis.recommendationEngine as recommendationEngine
from app.modules.analysis.similarity import compute_similarity
from app.data.idealFeatureStore import ideal_feature_store

class AnalysisService:
    def __init__(self, resume_data, desired_role):
        self.feature_builder = featureBuilder.FeatureBuilder(resume_data, desired_role)
        self.recommendation_engine = recommendationEngine.RecommendationEngine(ideal_feature_store)
        pass
    
    def __compute_similarity(self, text1, text2):
        return compute_similarity(text1, text2) 
    
    def analyse_resume(self):
        feature_vector = self.feature_builder.build_features()
        print("Feature Vector:", feature_vector)
        self.recommendation_engine.set_actual_features(feature_vector)
        recommendations = self.recommendation_engine.generate_recommendations()
        print("Recommendations:", recommendations)
        return recommendations