"""
Stats Module
============

Statistical analysis functions for scientific computing.
"""

import pandas as pd
import numpy as np
from typing import Optional, Union, List, Dict, Any, Tuple
from scipy import stats
from scipy.stats import ttest_ind, ttest_rel, f_oneway, chi2_contingency


class StatisticalAnalyzer:
    """
    A comprehensive statistical analysis utility.
    
    Provides common statistical tests and descriptive statistics.
    """
    
    def __init__(self):
        """Initialize the StatisticalAnalyzer."""
        pass
    
    @staticmethod
    def descriptive_stats(data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate descriptive statistics for a DataFrame.
        
        Args:
            data: Input DataFrame
            
        Returns:
            DataFrame with descriptive statistics
        """
        return data.describe()
    
    @staticmethod
    def ttest_independent(
        group1: Union[pd.Series, List[float]],
        group2: Union[pd.Series, List[float]],
        equal_var: bool = True
    ) -> Dict[str, float]:
        """
        Perform independent samples t-test.
        
        Args:
            group1: First group of observations
            group2: Second group of observations
            equal_var: Whether to assume equal population variances
            
        Returns:
            Dictionary with t-statistic and p-value
        """
        t_stat, p_value = ttest_ind(group1, group2, equal_var=equal_var)
        return {"t_statistic": t_stat, "p_value": p_value}
    
    @staticmethod
    def ttest_paired(
        group1: Union[pd.Series, List[float]],
        group2: Union[pd.Series, List[float]]
    ) -> Dict[str, float]:
        """
        Perform paired samples t-test.
        
        Args:
            group1: First group of observations
            group2: Second group of observations
            
        Returns:
            Dictionary with t-statistic and p-value
        """
        t_stat, p_value = ttest_rel(group1, group2)
        return {"t_statistic": t_stat, "p_value": p_value}
    
    @staticmethod
    def anova_one_way(*groups: Union[pd.Series, List[float]]) -> Dict[str, float]:
        """
        Perform one-way ANOVA.
        
        Args:
            *groups: Two or more groups of observations
            
        Returns:
            Dictionary with F-statistic and p-value
        """
        f_stat, p_value = f_oneway(*groups)
        return {"f_statistic": f_stat, "p_value": p_value}
    
    @staticmethod
    def chi_square_test(
        observed: Union[pd.DataFrame, np.ndarray],
        expected: Optional[Union[pd.DataFrame, np.ndarray]] = None
    ) -> Dict[str, float]:
        """
        Perform chi-square test of independence.
        
        Args:
            observed: Observed frequencies
            expected: Expected frequencies (optional)
            
        Returns:
            Dictionary with chi-square statistic, p-value, degrees of freedom
        """
        result = chi2_contingency(observed)
        return {
            "chi_square": result[0],
            "p_value": result[1],
            "dof": result[2],
            "expected": result[3]
        }
    
    @staticmethod
    def correlation(
        data: pd.DataFrame,
        method: str = "pearson"
    ) -> pd.DataFrame:
        """
        Calculate correlation matrix.
        
        Args:
            data: Input DataFrame
            method: Correlation method ("pearson", "spearman", "kendall")
            
        Returns:
            Correlation matrix
        """
        return data.corr(method=method)
    
    @staticmethod
    def pearson_correlation(
        x: Union[pd.Series, List[float]],
        y: Union[pd.Series, List[float]]
    ) -> Dict[str, float]:
        """
        Calculate Pearson correlation coefficient.
        
        Args:
            x: First variable
            y: Second variable
            
        Returns:
            Dictionary with correlation coefficient and p-value
        """
        corr, p_value = stats.pearsonr(x, y)
        return {"correlation": corr, "p_value": p_value}
    
    @staticmethod
    def spearman_correlation(
        x: Union[pd.Series, List[float]],
        y: Union[pd.Series, List[float]]
    ) -> Dict[str, float]:
        """
        Calculate Spearman rank correlation coefficient.
        
        Args:
            x: First variable
            y: Second variable
            
        Returns:
            Dictionary with correlation coefficient and p-value
        """
        corr, p_value = stats.spearmanr(x, y)
        return {"correlation": corr, "p_value": p_value}
    
    @staticmethod
    def normality_test(
        data: Union[pd.Series, List[float]],
        method: str = "shapiro"
    ) -> Dict[str, float]:
        """
        Test for normality of a distribution.
        
        Args:
            data: Sample data
            method: Test method ("shapiro", "knormal", "anderson")
            
        Returns:
            Dictionary with test statistic and p-value
        """
        if method == "shapiro":
            stat, p_value = stats.shapiro(data)
            return {"statistic": stat, "p_value": p_value}
        elif method == "knormal":
            stat, p_value = stats.kstest(data, 'norm')
            return {"statistic": stat, "p_value": p_value}
        else:
            raise ValueError(f"Unknown method: {method}")
    
    @staticmethod
    def confidence_interval(
        data: Union[pd.Series, List[float]],
        confidence: float = 0.95
    ) -> Tuple[float, float]:
        """
        Calculate confidence interval for the mean.
        
        Args:
            data: Sample data
            confidence: Confidence level (default 0.95)
            
        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        n = len(data)
        mean = np.mean(data)
        sem = stats.sem(data)
        margin = sem * stats.t.ppf((1 + confidence) / 2., n - 1)
        return (mean - margin, mean + margin)


def perform_ttest(
    group1: Union[pd.Series, List[float]],
    group2: Union[pd.Series, List[float]],
    paired: bool = False,
    equal_var: bool = True
) -> Dict[str, float]:
    """
    Convenience function to perform t-test.
    
    Args:
        group1: First group of observations
        group2: Second group of observations
        paired: Whether to perform paired t-test
        equal_var: Whether to assume equal variances (for independent t-test)
        
    Returns:
        Dictionary with test results
    """
    analyzer = StatisticalAnalyzer()
    if paired:
        return analyzer.ttest_paired(group1, group2)
    else:
        return analyzer.ttest_independent(group1, group2, equal_var)


def perform_anova(*groups: Union[pd.Series, List[float]]) -> Dict[str, float]:
    """
    Convenience function to perform one-way ANOVA.
    
    Args:
        *groups: Two or more groups of observations
        
    Returns:
        Dictionary with test results
    """
    analyzer = StatisticalAnalyzer()
    return analyzer.anova_one_way(*groups)