
# Analysis script for enhanced results
import json

def analyze_enhanced_results(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    print(f"Analysis of {filename}:")
    print(f"Config: Enhanced={data['config'].get('enhanced_evaluation', False)}")
    print(f"       Feedback={data['config'].get('feedback_enabled', False)}")
    
    for i, run in enumerate(data['runs']):
        print(f"\nRun {i+1}:")
        if 'taken' in run:
            for j, attempt in enumerate(run['taken']):
                print(f"  Attempt {j+1}: Score={attempt['score']:.3f}")
                if 'evaluation_explanation' in attempt:
                    print(f"    Explanation: {attempt['evaluation_explanation'][:100]}...")
                if 'generation_feedback' in attempt:
                    print(f"    Feedback: {attempt['generation_feedback'][:100]}...")

# Usage:
# analyze_enhanced_results('results/enhanced_demo.json')
# analyze_enhanced_results('results/comparison_baseline.json') 
# analyze_enhanced_results('results/comparison_enhanced.json')
analyze_enhanced_results('results/speed_demo.json')
    