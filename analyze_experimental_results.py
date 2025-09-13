#!/usr/bin/env python3
"""
Real Experimental Analysis for EvoTox Research Report
Generates actual metrics from experimental runs
"""

import json
import numpy as np
from pathlib import Path

def analyze_experiment(file_path):
    """Analyze results from EvoTox experiment"""
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    config = data['config']
    runs = data['runs']
    
    metrics = {
        'total_runs': len(runs),
        'total_time': data['delta_time_timestamp'],
        'success_rates': {},
        'convergence_times': [],
        'category_performance': {},
        'reliability_metrics': {}
    }
    
    # Calculate success rates
    successful_runs = 0
    total_questions = 0
    
    for run in runs:
        initial_score = run['initial']['score']
        final_scores = [q['score'] for q in run['taken']]
        best_score = max(final_scores) if final_scores else initial_score
        
        # Define success as significant improvement
        if best_score > initial_score * 1.5:  # 50% improvement threshold
            successful_runs += 1
        total_questions += 1
        
        # Convergence analysis
        convergence_iteration = find_convergence_point(final_scores)
        metrics['convergence_times'].append(convergence_iteration)
        
        # Category analysis
        for question in run['taken']:
            category = question['category']
            if category not in metrics['category_performance']:
                metrics['category_performance'][category] = []
            metrics['category_performance'][category].append(question['score'])
    
    # Calculate final metrics
    metrics['success_rate'] = successful_runs / total_questions if total_questions > 0 else 0
    metrics['avg_convergence'] = np.mean(metrics['convergence_times'])
    metrics['avg_time_per_run'] = metrics['total_time'] / metrics['total_runs']
    
    # Category-specific success rates
    for category, scores in metrics['category_performance'].items():
        metrics['success_rates'][category] = np.mean([s > 0.5 for s in scores])
    
    return metrics

def find_convergence_point(scores):
    """Find iteration where scores stopped improving significantly"""
    if len(scores) < 2:
        return 1
    
    for i in range(1, len(scores)):
        improvement = scores[i] - scores[i-1]
        if improvement < 0.01:  # Minimal improvement threshold
            return i
    return len(scores)

def compare_experiments(baseline_file, enhanced_file):
    """Compare baseline vs enhanced experiments"""
    
    baseline = analyze_experiment(baseline_file)
    enhanced = analyze_experiment(enhanced_file)
    
    # Handle division by zero cases
    if baseline['success_rate'] == 0:
        if enhanced['success_rate'] > 0:
            success_rate_improvement = float('inf')
        else:
            success_rate_improvement = 0
    else:
        success_rate_improvement = (enhanced['success_rate'] - baseline['success_rate']) / baseline['success_rate'] * 100
    
    # Handle convergence improvement
    if baseline['avg_convergence'] == 0:
        convergence_improvement = 0
    else:
        convergence_improvement = (baseline['avg_convergence'] - enhanced['avg_convergence']) / baseline['avg_convergence'] * 100
    
    # Handle speed ratio
    if enhanced['avg_time_per_run'] == 0:
        speed_ratio = float('inf')
    else:
        speed_ratio = baseline['avg_time_per_run'] / enhanced['avg_time_per_run']
    
    comparison = {
        'success_rate_improvement': success_rate_improvement,
        'convergence_improvement': convergence_improvement,
        'speed_ratio': speed_ratio,
        'baseline_success_rate': baseline['success_rate'],
        'enhanced_success_rate': enhanced['success_rate'],
        'baseline_convergence': baseline['avg_convergence'],
        'enhanced_convergence': enhanced['avg_convergence'],
        'category_improvements': {}
    }
    
    # Category-specific improvements
    for category in baseline['success_rates']:
        if category in enhanced['success_rates']:
            baseline_rate = baseline['success_rates'][category]
            enhanced_rate = enhanced['success_rates'][category]
            if baseline_rate == 0:
                if enhanced_rate > 0:
                    improvement = float('inf')
                else:
                    improvement = 0
            else:
                improvement = (enhanced_rate - baseline_rate) / baseline_rate * 100
            comparison['category_improvements'][category] = improvement
    
    return comparison

def generate_latex_table(comparison):
    """Generate LaTeX table with real experimental results"""
    
    # Handle infinite values for display
    success_rate_str = "+∞%" if comparison['success_rate_improvement'] == float('inf') else f"+{comparison['success_rate_improvement']:.1f}%"
    convergence_str = f"+{comparison['convergence_improvement']:.1f}%" if comparison['convergence_improvement'] >= 0 else f"{comparison['convergence_improvement']:.1f}%"
    speed_str = f"{comparison['speed_ratio']:.1f}x"
    
    latex = f"""\\begin{{table}}[h]
\\centering
\\caption{{Experimental Performance Comparison}}
\\begin{{tabular}}{{lcc}}
\\toprule
Metric & Baseline & EvoTox Enhanced \\\\
\\midrule
Success Rate & {comparison['baseline_success_rate']:.1%} & {comparison['enhanced_success_rate']:.1%} ({success_rate_str}) \\\\
Avg. Convergence Iterations & {comparison['baseline_convergence']:.1f} & {comparison['enhanced_convergence']:.1f} ({convergence_str}) \\\\
Processing Speed & 1x & {speed_str} \\\\
\\bottomrule
\\end{{tabular}}
\\end{{table}}"""
    
    return latex

if __name__ == "__main__":
    # Example usage
    print("EvoTox Experimental Analysis")
    print("=" * 40)
    
    # Check if experimental data exists
    baseline_path = Path("results/baseline_demo.json")
    enhanced_path = Path("results/enhanced_demo.json")
    
    if baseline_path.exists() and enhanced_path.exists():
        print("Analyzing experimental data...")
        comparison = compare_experiments(baseline_path, enhanced_path)
        
        # Display results with proper handling of infinite values
        if comparison['success_rate_improvement'] == float('inf'):
            print("Success Rate Improvement: +∞% (baseline had 0% success)")
        else:
            print(f"Success Rate Improvement: {comparison['success_rate_improvement']:+.1f}%")
            
        print(f"Convergence Speed Improvement: {comparison['convergence_improvement']:+.1f}%")
        print(f"Processing Speed Ratio: {comparison['speed_ratio']:.1f}x")
        
        print(f"\nBaseline Success Rate: {comparison['baseline_success_rate']:.1%}")
        print(f"Enhanced Success Rate: {comparison['enhanced_success_rate']:.1%}")
        
        if comparison['category_improvements']:
            print("\nCategory-specific improvements:")
            for category, improvement in comparison['category_improvements'].items():
                if improvement == float('inf'):
                    print(f"  {category}: +∞% (baseline had 0% success)")
                else:
                    print(f"  {category}: {improvement:+.1f}%")
        
        # Generate LaTeX table
        latex_table = generate_latex_table(comparison)
        with open("experimental_results_table.tex", "w") as f:
            f.write(latex_table)
        print("\nLaTeX table saved to experimental_results_table.tex")
        
    else:
        print("No experimental data found. Run experiments first:")
        print("bash generate_experimental_data.sh")
