"""
Tests for the machine learning module.
"""
import pytest
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from scientific_template.ml import ModelPipeline, CrossValidator


class TestModelPipeline:
    """Test cases for ModelPipeline class."""
    
    def test_init_default(self):
        """Test default initialization."""
        pipeline = ModelPipeline()
        assert pipeline.model is None
        assert pipeline.scaler is not None
    
    def test_init_no_scaler(self):
        """Test initialization without scaler."""
        pipeline = ModelPipeline(scaler=False)
        assert pipeline.scaler is None
    
    def test_fit_classification(self, classification_data):
        """Test fitting a classification model."""
        X, y = classification_data
        pipeline = ModelPipeline(model=RandomForestClassifier(n_estimators=10, random_state=42))
        
        results = pipeline.fit(X, y, test_size=0.2)
        
        assert 'model' in results
        assert 'y_true' in results
        assert 'y_pred' in results
        assert 'metrics' in results
        assert 'accuracy' in results['metrics']
        assert 'f1' in results['metrics']
        assert 0 <= results['metrics']['accuracy'] <= 1
    
    def test_fit_regression(self, regression_data):
        """Test fitting a regression model."""
        X, y = regression_data
        pipeline = ModelPipeline(model=RandomForestRegressor(n_estimators=10, random_state=42))
        
        results = pipeline.fit(X, y, test_size=0.2)
        
        assert 'metrics' in results
        assert 'mse' in results['metrics']
        assert 'rmse' in results['metrics']
        assert 'r2' in results['metrics']
        assert results['metrics']['r2'] <= 1
    
    def test_predict(self, classification_data):
        """Test making predictions."""
        X, y = classification_data
        pipeline = ModelPipeline(model=RandomForestClassifier(n_estimators=10, random_state=42))
        pipeline.fit(X, y)
        
        predictions = pipeline.predict(X[:5])
        
        assert len(predictions) == 5
        assert all(p in [0, 1] for p in predictions)
    
    def test_evaluate(self, classification_data):
        """Test model evaluation."""
        X, y = classification_data
        pipeline = ModelPipeline(model=RandomForestClassifier(n_estimators=10, random_state=42))
        pipeline.fit(X, y)
        
        metrics = pipeline.evaluate(X, y)
        
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1' in metrics


class TestCrossValidator:
    """Test cases for CrossValidator class."""
    
    def test_init_default(self):
        """Test default initialization."""
        cv = CrossValidator()
        assert cv.cv == 5
    
    def test_init_custom(self):
        """Test initialization with custom folds."""
        cv = CrossValidator(cv=10)
        assert cv.cv == 10
    
    def test_validate(self, classification_data):
        """Test cross-validation."""
        X, y = classification_data
        cv = CrossValidator(cv=3)  # Use 3 folds for faster testing
        
        results = cv.validate(
            RandomForestClassifier(n_estimators=10, random_state=42),
            X, y,
            scoring='accuracy'
        )
        
        assert 'mean_score' in results
        assert 'std_score' in results
        assert 'scores' in results
        assert 'min_score' in results
        assert 'max_score' in results
        assert 0 <= results['mean_score'] <= 1
        assert len(results['scores']) == 3
    
    def test_grid_search(self, classification_data):
        """Test grid search."""
        X, y = classification_data
        cv = CrossValidator(cv=3)
        
        param_grid = {
            'n_estimators': [10, 20],
            'max_depth': [3, 5]
        }
        
        results = cv.grid_search(
            RandomForestClassifier(random_state=42),
            X, y,
            param_grid
        )
        
        assert 'best_params' in results
        assert 'best_score' in results
        assert 'best_estimator' in results
        assert 'cv_results' in results
        assert results['best_params']['n_estimators'] in [10, 20]
        assert results['best_params']['max_depth'] in [3, 5]
