# app/api/services/analysis_service.py

import app.modules.analysis.featureBuilder as featureBuilder
import app.modules.analysis.recommendationEngine as recommendationEngine
from app.modules.analysis.similarity import compute_similarity

class AnalysisService:
    def __init__(self):
        self.feature_builder = featureBuilder.FeatureBuilder()
        self.recommendation_engine = recommendationEngine.RecommendationEngine()
        pass
    
    def __compute_similarity(self, text1, text2):
        return compute_similarity(text1, text2) 