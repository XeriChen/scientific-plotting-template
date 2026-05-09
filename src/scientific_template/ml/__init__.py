"""
ML Module
=========

Machine learning utilities for scientific computing.
"""

import pandas as pd
import numpy as np
from typing import Optional, Union, List, Dict, Any, Tuple
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, mean_squared_error, r2_score


class ModelPipeline:
    """
    A comprehensive machine learning pipeline utility.
    
    Provides streamlined model training, evaluation, and prediction.
    """
    
    def __init__(self, model=None, scaler: bool = True):
        """
        Initialize the ModelPipeline.
        
        Args:
            model: Scikit-learn compatible model (optional)
            scaler: Whether to apply feature scaling
        """
        self.model = model
        self.scaler = StandardScaler() if scaler else None
        self.label_encoder = LabelEncoder()
        self.is_classification = None
    
    def fit(
        self,
        X: Union[pd.DataFrame, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        test_size: float = 0.2,
        random_state: int = 42
    ) -> Dict[str, Any]:
        """
        Fit the model on training data.
        
        Args:
            X: Feature matrix
            y: Target variable
            test_size: Proportion of data for testing
            random_state: Random seed for reproducibility
            
        Returns:
            Dictionary with training results and metrics
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Scale features if enabled
        if self.scaler:
            X_train = self.scaler.fit_transform(X_train)
            X_test = self.scaler.transform(X_test)
        
        # Encode target if categorical
        if isinstance(y, pd.Series) and y.dtype == 'object':
            y_train = self.label_encoder.fit_transform(y_train)
            y_test = self.label_encoder.transform(y_test)
            self.is_classification = True
        elif hasattr(y, 'dtype') and np.issubdtype(y.dtype, np.integer):
            self.is_classification = True
        else:
            self.is_classification = False
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        
        results = {
            "model": self.model,
            "y_true": y_test,
            "y_pred": y_pred
        }
        
        if self.is_classification:
            results["metrics"] = {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred, average='weighted', zero_division=0),
                "recall": recall_score(y_test, y_pred, average='weighted', zero_division=0),
                "f1": f1_score(y_test, y_pred, average='weighted', zero_division=0)
            }
        else:
            results["metrics"] = {
                "mse": mean_squared_error(y_test, y_pred),
                "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
                "r2": r2_score(y_test, y_pred)
            }
        
        return results
    
    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Make predictions with the trained model.
        
        Args:
            X: Feature matrix
            
        Returns:
            Predictions
        """
        if self.scaler:
            X = self.scaler.transform(X)
        return self.model.predict(X)
    
    def evaluate(
        self,
        X: Union[pd.DataFrame, np.ndarray],
        y: Union[pd.Series, np.ndarray]
    ) -> Dict[str, float]:
        """
        Evaluate the model on given data.
        
        Args:
            X: Feature matrix
            y: Target variable
            
        Returns:
            Dictionary with evaluation metrics
        """
        if self.scaler:
            X = self.scaler.transform(X)
        
        y_pred = self.model.predict(X)
        
        if self.is_classification:
            if isinstance(y, pd.Series) and y.dtype == 'object':
                y = self.label_encoder.transform(y)
            
            return {
                "accuracy": accuracy_score(y, y_pred),
                "precision": precision_score(y, y_pred, average='weighted', zero_division=0),
                "recall": recall_score(y, y_pred, average='weighted', zero_division=0),
                "f1": f1_score(y, y_pred, average='weighted', zero_division=0)
            }
        else:
            return {
                "mse": mean_squared_error(y, y_pred),
                "rmse": np.sqrt(mean_squared_error(y, y_pred)),
                "r2": r2_score(y, y_pred)
            }


class CrossValidator:
    """
    Cross-validation utility for model evaluation.
    """
    
    def __init__(self, cv: int = 5):
        """
        Initialize the CrossValidator.
        
        Args:
            cv: Number of cross-validation folds
        """
        self.cv = cv
    
    def validate(
        self,
        model,
        X: Union[pd.DataFrame, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        scoring: Optional[str] = None,
        shuffle: bool = True,
        random_state: int = 42
    ) -> Dict[str, float]:
        """
        Perform cross-validation.
        
        Args:
            model: Scikit-learn compatible model
            X: Feature matrix
            y: Target variable
            scoring: Scoring metric
            shuffle: Whether to shuffle data before splitting
            random_state: Random seed
            
        Returns:
            Dictionary with cross-validation results
        """
        scores = cross_val_score(
            model, X, y,
            cv=self.cv,
            scoring=scoring,
            n_jobs=-1
        )
        
        return {
            "mean_score": scores.mean(),
            "std_score": scores.std(),
            "scores": scores.tolist(),
            "min_score": scores.min(),
            "max_score": scores.max()
        }
    
    def grid_search(
        self,
        model,
        X: Union[pd.DataFrame, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        param_grid: Dict[str, List[Any]],
        scoring: Optional[str] = None,
        cv: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Perform grid search for hyperparameter tuning.
        
        Args:
            model: Scikit-learn compatible model
            X: Feature matrix
            y: Target variable
            param_grid: Parameter grid for grid search
            scoring: Scoring metric
            cv: Number of CV folds (uses self.cv if None)
            
        Returns:
            Dictionary with best parameters and score
        """
        grid_search = GridSearchCV(
            model,
            param_grid,
            cv=cv or self.cv,
            scoring=scoring,
            n_jobs=-1
        )
        
        grid_search.fit(X, y)
        
        return {
            "best_params": grid_search.best_params_,
            "best_score": grid_search.best_score_,
            "best_estimator": grid_search.best_estimator_,
            "cv_results": grid_search.cv_results_
        }