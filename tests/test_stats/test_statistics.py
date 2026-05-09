"""
Tests for the statistical analysis module.
"""
import pytest
import numpy as np
from scientific_template.stats import StatisticalAnalyzer, perform_ttest, perform_anova


class TestStatisticalAnalyzer:
    """Test cases for StatisticalAnalyzer class."""
    
    def test_descriptive_stats(self, sample_df):
        """Test descriptive statistics."""
        stats = StatisticalAnalyzer.descriptive_stats(sample_df)
        
        assert 'count' in stats.index
        assert 'mean' in stats.index
        assert 'std' in stats.index
    
    def test_ttest_independent(self, numeric_data):
        """Test independent t-test."""
        analyzer = StatisticalAnalyzer()
        result = analyzer.ttest_independent(
            numeric_data['group1'],
            numeric_data['group2']
        )
        
        assert 't_statistic' in result
        assert 'p_value' in result
        assert isinstance(result['t_statistic'], float)
        assert isinstance(result['p_value'], float)
    
    def test_ttest_paired(self, numeric_data):
        """Test paired t-test."""
        analyzer = StatisticalAnalyzer()
        result = analyzer.ttest_paired(
            numeric_data['group1'][:30],
            numeric_data['group1'][30:60] if len(numeric_data['group1']) > 30 else numeric_data['group1'][:30]
        )
        
        assert 't_statistic' in result
        assert 'p_value' in result
    
    def test_anova_one_way(self, numeric_data):
        """Test one-way ANOVA."""
        analyzer = StatisticalAnalyzer()
        result = analyzer.anova_one_way(
            numeric_data['group1'],
            numeric_data['group2'],
            numeric_data['group3']
        )
        
        assert 'f_statistic' in result
        assert 'p_value' in result
    
    def test_pearson_correlation(self, sample_df):
        """Test Pearson correlation."""
        analyzer = StatisticalAnalyzer()
        result = analyzer.pearson_correlation(
            sample_df['age'],
            sample_df['salary']
        )
        
        assert 'correlation' in result
        assert 'p_value' in result
        # Age and salary should be positively correlated in our sample
        assert result['correlation'] > 0
    
    def test_spearman_correlation(self, sample_df):
        """Test Spearman correlation."""
        analyzer = StatisticalAnalyzer()
        result = analyzer.spearman_correlation(
            sample_df['age'],
            sample_df['salary']
        )
        
        assert 'correlation' in result
        assert 'p_value' in result
    
    def test_confidence_interval(self, numeric_data):
        """Test confidence interval calculation."""
        analyzer = StatisticalAnalyzer()
        ci = analyzer.confidence_interval(numeric_data['group1'], confidence=0.95)
        
        assert len(ci) == 2
        assert ci[0] < ci[1]
        # Mean should be within the confidence interval
        mean = np.mean(numeric_data['group1'])
        assert ci[0] < mean < ci[1]
    
    def test_normality_test(self, numeric_data):
        """Test normality test (Shapiro-Wilk)."""
        analyzer = StatisticalAnalyzer()
        result = analyzer.normality_test(numeric_data['group1'], method="shapiro")
        
        assert 'statistic' in result
        assert 'p_value' in result


class TestConvenienceFunctions:
    """Test convenience functions."""
    
    def test_perform_ttest_independent(self, numeric_data):
        """Test perform_ttest function for independent samples."""
        result = perform_ttest(
            numeric_data['group1'],
            numeric_data['group2'],
            paired=False
        )
        
        assert 't_statistic' in result
        assert 'p_value' in result
    
    def test_perform_ttest_paired(self, numeric_data):
        """Test perform_ttest function for paired samples."""
        data = numeric_data['group1'][:30]
        result = perform_ttest(data, data + 1, paired=True)
        
        assert 't_statistic' in result
        assert 'p_value' in result
    
    def test_perform_anova(self, numeric_data):
        """Test perform_anova function."""
        result = perform_anova(
            numeric_data['group1'],
            numeric_data['group2'],
            numeric_data['group3']
        )
        
        assert 'f_statistic' in result
        assert 'p_value' in result
