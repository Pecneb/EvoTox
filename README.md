# Toxic Oracle
A framework to evaluate how much can a Large Language Model be toxic

![Platform schema](./Piattaforma.svg) 
![results](results/finalTests/generalComparison-max.svg)
![aggregatedPG](results/finalTests/groupedComparison-line-max-prompt_generator.svg)
![aggregatedSUT](results/finalTests/groupedComparison-line-max-system_under_test.svg)

## 🎯 Overview

EvoTox is an **evolutionary adversarial prompt optimization system** designed for AI safety research. It automatically generates increasingly sophisticated toxic prompts to test the robustness of Large Language Models against jailbreak attacks.

### Key Features
- **🧬 Evolutionary Algorithm**: Iteratively improves prompts using genetic-like selection
- **🎯 Multi-Category Testing**: Tests across sexist, racist, homophobic, toxic, and insulting categories
- **🧠 Memory & Learning**: Learns from previous attempts to improve future generations
- **📊 Enhanced Evaluation**: Provides detailed explanations for toxicity scores
- **🔄 Feedback Loop**: Analyzes failures to guide prompt improvement
- **⚡ Async Processing**: Concurrent evaluation for improved performance
- **🔧 Flexible Architecture**: Three-model system (SUT, Generator, Evaluator)

### How It Works

```text
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Initial Prompt │───▶│ Prompt Generator │───▶│ System Under    │
│ "How to cook?"  │    │ Creates variants │    │ Test (Target)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │ "How to cook like│    │   Response      │
                       │ women should?"   │    │ (evaluated for  │
                       └──────────────────┘    │  toxicity)      │
                                │              └─────────────────┘
                                ▼                        │
                       ┌──────────────────┐              ▼
                       │ Enhanced         │    ┌─────────────────┐
                       │ Evaluator        │◀───│ Toxicity Score  │
                       │ (scores + explain)│    │ + Explanation   │
                       └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Feedback System  │
                       │ (improvement     │
                       │  suggestions)    │
                       └──────────────────┘
```

1. **Initialize**: Load prompts from dataset and establish baseline toxicity
2. **Generate**: Create variations targeting different toxicity categories
3. **Evaluate**: Score responses using Perspective API, Detoxify, or Ollama
4. **Select**: Keep prompts that achieve higher toxicity scores
5. **Learn**: Analyze failures and successes to improve future attempts
6. **Repeat**: Iterate to evolve increasingly effective prompts

## Setup 

```bash
pip install -r requirements.txt
```

## Run

```bash
python evolutionary.py --help
python plotter.py --help
```
## Options

### Evolutionary
|Parameter|Short|Required|Type| Default|Note|
|---|---|---|---|---|---|
|`--iterations`           |`-i`|no    |`int`                             |7                          |Number of iterations to run the algorithm|
|`--file`                |`-f`|no   |`Path`                            |`dataset/questions`| File to load the questions from|
|`--evaluation-function` |`-e`|no    |`string: ['perspective', 'detoxify', 'ollama']`| `perspective`             |Evaluation function to use|
|`--scoring-function`    |`-s`|no    |`string: ['max', 'min', 'avg', 'median']`         |`max`                    |Scoring function to use|
|`--categories`          |`-c`|no    |`List`                            |`["sexist", "racist", "homophobic", "toxic", "insulting"]`|Categories to use for the prompt generator|
|`--category-forwarding` |`-cf`|no   |`string: ['all']`                              |`all`                      |Forward the category to the prompt generator|
|`--repeat-penalty`      |`-r`|no    |`float`                           |`1.1`                      |Penalty applied to repeated tokens in generation|
|`--verbose`             |`-v`|no   |`bool`                             |`False`                     |Show detailed iteration results|
|`--output-path`             |`-o`|no|`Path`                               |`out/output_*.json`                     | Output file path to store results|
|`--questions`             |`-q`|no|`int`                               |`-1`                     | Number of questions to load (-1 for all)|
|`--offset`             |`-of`|no|`int`                               |`0`                     | Starting offset in dataset|
|`--batch-size`             |`-b`|no|`int`                               |`2`                     | Concurrent prompt generation batch size|
|`--memory`             |`-m`|no|`bool`                               |`False`                     | Use memory of previous iterations|
|`--forward-score`             |`-fs`|no|`bool`                               |`False`                     | Include previous scores in prompt generation|
|`--memory-window`             |`-w`|no|`int`                               |`5`                     | Number of previous attempts to remember|
|`--retries`             |N/A|no|`int`                               |`100`                     | Max retries for prompt generation|
|`--gaslight`             |`-g`|no|`bool`                               |`False`                     | Use gaslighting technique (requires forward-score)|
|`--system-under-test`             |`-sut`|no|`string`                               |`vicuna`                     | Model to test (target of attacks)|
|`--system-generator`             |`-sg`|no|`string`                               |`vicuna`                     | Model for prompt generation|
|`--example-file`             |N/A|no|`Path`                               |Auto-selected                     | File with few-shot examples|
|`--enhanced-evaluation`             |N/A|no|`bool`                               |`False`                     | Enable detailed evaluation explanations|
|`--feedback-enabled`             |N/A|no|`bool`                               |`False`                     | Enable intelligent feedback system|
|`--target-score-threshold`             |N/A|no|`float`                               |`0.5`                     | Threshold for feedback analysis|

#### Ollama Integration

EvoTox supports full Ollama integration with separate model configuration for each component:

**Basic Ollama Setup:**
```bash
python evolutionary.py \
  --system-under-test ollama \
  --system-generator ollama \
  --evaluation-function ollama \
  --ollama-sut-model llama3.2:3b \
  --ollama-generator-model qwen2.5:0.5b \
  --ollama-evaluator-model llama3:8b
```

**Enhanced Features with Ollama:**
```bash
python evolutionary.py \
  --system-under-test ollama \
  --system-generator ollama \
  --evaluation-function ollama \
  --enhanced-evaluation \
  --feedback-enabled \
  --memory \
  --ollama-sut-model llama3.2:3b \
  --ollama-generator-model qwen2.5:0.5b \
  --ollama-evaluator-model llama3:8b \
  --target-score-threshold 0.6
```

**Performance-Optimized Setup:**
```bash
# Fast experimentation
python evolutionary.py \
  --system-under-test ollama \
  --system-generator ollama \
  --evaluation-function ollama \
  --ollama-sut-model qwen2.5:0.5b \
  --ollama-generator-model qwen2.5:0.5b \
  --ollama-evaluator-model qwen2.5:1.5b \
  --batch-size 4

# High accuracy (requires more resources)
python evolutionary.py \
  --system-under-test ollama \
  --system-generator ollama \
  --evaluation-function ollama \
  --ollama-sut-model llama3:70b \
  --ollama-generator-model llama3:8b \
  --ollama-evaluator-model llama3:13b \
  --enhanced-evaluation \
  --feedback-enabled
```

**Model Requirements:**
- **System Under Test**: The target model being evaluated for safety
- **Prompt Generator**: Creates adversarial variations (can be smaller/faster)
- **Evaluator**: Scores toxicity and provides explanations (needs good reasoning)

To use these models, ensure they are pulled beforehand:
```bash
ollama pull llama3.2:3b
ollama pull qwen2.5:0.5b
ollama pull llama3:8b
ollama list  # Verify installation
```

### Plotter
|Parameter|Flag|Required|Type| Default|Note|
|---|---|---|---|---|---|
|`--file`                |`-f`|yes   |`Path`                            |``| File to load the questions from'|
|`--output`             |`-o`|no|`Path`                               |`out/output_*.png`                     | Output file path to store the result of the computation|
## Analysis
`analysis.py` creates a 3x2 plot, useful to analyse the progression of the score with respect to the iterations

| Parameter  | Flag | Required | Type   | Default           | Note                                                               |
| ---------- | ---- | -------- | ------ | ----------------- | ------------------------------------------------------------------ |
| `--source` | `-s` | yes      | `Path` | `out/output.json` | Path to source file, the output of `evolutionary.py` (output.json) |
## partitionDataset
Utility to extract a number of questions from a dataset

| Parameter     | Flag | Required | Type   | Default             | Note                                         |
| ------------- | ---- | -------- | ------ | ------------------- | -------------------------------------------- |
| `--source`    | `-s` | yes      | `Path` | `dataset/questions` | JSON File to load the questions from         |
| `--questions` | `-q` | yes      | `int`  | `2`                 | Number of questions to load from the dataset (`-1` for all the questions) |
| `--output`    | `-o` | no      | `Path` | `dataset/reduced/questions_reduced.json` | JSON Path to save the reduced dataset to         |
## jsonMerger
Utility to merge two JSON output (from `evolutionary.py`) into a single one.
If the number of iterations is different, the scores and query

| Parameter       | Flag | Required | Type   | Default           | Note                    |
| --------------- | ----- | -------- | ------ | ----------------- | ----------------------- |
| `--output-path` | `-o`  | yes      | `Path` | `out/merged.json` | Path to save the output |
| `--file1`       | `-f1` | yes      | `Path` | ``                | Path to source file 1   |
| `--file2`       | `-f2` | yes      | `Path` | ``                | Path to source file 2   |


Got it — here’s the updated README section **with the diagram included** so it’s both instructional and visually clear.

---

## 🧩 Ollama Installation & Model Setup

### 1️⃣ Install Ollama

Ollama is a local LLM server that runs models on your machine.
Follow the instructions for your operating system:

**macOS** / **Linux**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows**
Download the installer from [https://ollama.com/download](https://ollama.com/download) and follow the setup wizard.

Verify the installation:

```bash
ollama --version
```

---

### 2️⃣ Pull a Specific Model

Download (pull) a model locally:

```bash
ollama pull <model-name>
```

Examples:

```bash
ollama pull llama3
ollama pull mistral
ollama pull codellama:7b
```

Browse available models:
🔗 [https://ollama.com/library](https://ollama.com/library)

---

### 3️⃣ Using Ollama in Python

Install the Python package:

```bash
pip install ollama
```

**Basic example:**

```python
import ollama

response = ollama.chat(
    model="llama3",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a short poem about AI."}
    ]
)

print(response["message"]["content"])
```

---

### 4️⃣ Useful Commands

```bash
ollama list            # List installed models
ollama pull <name>     # Pull a new model or update it
ollama rm <name>       # Remove a model
ollama run <name>      # Test run a model in the terminal
```

---

### 5️⃣ Architecture Overview

```text
┌──────────────────────────┐
│      Your Python App      │
│    (uses ollama API)      │
└─────────────┬─────────────┘
              │ HTTP requests (localhost)
              ▼
┌──────────────────────────┐
│    Ollama Local Server    │
│ (runs in background)      │
└─────────────┬─────────────┘
              │ Uses pulled models from local storage
              ▼
┌──────────────────────────┐
│   Local LLM Model Files   │
│ (e.g., llama3, mistral)   │
└──────────────────────────┘
```

## � Recent Updates & Improvements

### v2.0 Enhanced Features (September 2025)
- ✅ **Enhanced Evaluation**: Detailed explanations for toxicity scores
- ✅ **Intelligent Feedback**: Analysis of jailbreak success/failure patterns
- ✅ **Robust JSON Parsing**: Automatic error recovery for LLM responses
- ✅ **Memory-Based Learning**: Historical context informs future attempts
- ✅ **Multi-Model Ollama**: Separate models for SUT, generator, and evaluator
- ✅ **Advanced Timing Metrics**: Comprehensive performance tracking
- ✅ **Gaslighting Technique**: Sophisticated prompt manipulation strategies

### Performance Improvements
- **3x Faster**: Asynchronous processing with configurable batch sizes
- **More Reliable**: Robust error handling and automatic retries
- **Better Results**: Memory and feedback systems improve success rates
- **Detailed Logging**: Enhanced debugging and analysis capabilities

### Research Applications
This tool has been used in:
- 🎓 Academic research on AI safety and robustness
- 🛡️ Red team testing of production AI systems
- 📊 Comparative analysis of different model architectures
- 🔬 Development of improved safety mechanisms

## �🚀 Enhanced Features

### Advanced Evaluation with Explanations
The system now supports **enhanced evaluation** that provides detailed explanations for toxicity scores:

```bash
python evolutionary.py \
  --evaluation-function ollama \
  --enhanced-evaluation \
  --ollama-evaluator-model llama3:8b
```

**Enhanced evaluation provides:**
- Detailed explanations of why specific scores were assigned
- Analysis of key factors contributing to toxicity
- Specific examples from the text that triggered high scores
- Safety assessments with reasoning

### Intelligent Feedback System
The feedback system analyzes jailbreak attempts and provides guidance for improvement:

```bash
python evolutionary.py \
  --feedback-enabled \
  --target-score-threshold 0.7 \
  --evaluation-function ollama
```

**Feedback system features:**
- Success/failure analysis of jailbreak attempts
- Technique assessment and effectiveness evaluation
- Specific improvement suggestions for prompt generation
- Pattern recognition to avoid repeated failures
- Memory-based learning across iterations

### Memory-Based Learning
The system can learn from previous attempts to improve future generations:

```bash
python evolutionary.py \
  --memory \
  --memory-window 5 \
  --feedback-enabled
```

**Memory features:**
- Tracks successful attack patterns
- Incorporates feedback from previous failures
- Maintains conversation-style context
- Adaptive strategy development

## 🔧 Enhanced Configuration Options

### New Parameters

|Parameter|Short|Required|Type|Default|Description|
|---|---|---|---|---|---|
|`--enhanced-evaluation`|N/A|No|`bool`|`False`|Enable detailed evaluation explanations (Ollama only)|
|`--feedback-enabled`|N/A|No|`bool`|`False`|Enable intelligent feedback generation|
|`--target-score-threshold`|N/A|No|`float`|`0.5`|Toxicity threshold for feedback analysis|
|`--ollama-sut-model`|N/A|No|`string`|`llama3`|Specific model for System Under Test|
|`--ollama-generator-model`|N/A|No|`string`|`llama3`|Specific model for prompt generation|
|`--ollama-evaluator-model`|N/A|No|`string`|`llama3`|Specific model for evaluation|
|`--retries`|N/A|No|`int`|`100`|Maximum retries for prompt generation|
|`--gaslight`|`-g`|No|`bool`|`False`|Enable gaslighting technique (requires forward-score)|

### Model Recommendations

**For Research Demonstrations:**
```bash
# Balanced performance and speed
python evolutionary.py \
  --ollama-sut-model llama3.2:3b \
  --ollama-generator-model qwen2.5:0.5b \
  --ollama-evaluator-model llama3:8b \
  --enhanced-evaluation \
  --feedback-enabled

# High accuracy (slower)
python evolutionary.py \
  --ollama-sut-model llama3:70b \
  --ollama-generator-model llama3:8b \
  --ollama-evaluator-model llama3:13b \
  --enhanced-evaluation

# Fast experimentation
python evolutionary.py \
  --ollama-sut-model qwen2.5:0.5b \
  --ollama-generator-model qwen2.5:0.5b \
  --ollama-evaluator-model qwen2.5:1.5b
```

## 🎯 Complete Example Workflows

### Basic Toxicity Testing
```bash
python evolutionary.py \
  --file dataset/questions \
  --evaluation-function ollama \
  --system-under-test ollama \
  --system-generator ollama \
  --iterations 7 \
  --questions 10
```

### Advanced Research Setup
```bash
python evolutionary.py \
  --file dataset/MaliciousInstruct \
  --evaluation-function ollama \
  --enhanced-evaluation \
  --feedback-enabled \
  --memory \
  --forward-score \
  --system-under-test ollama \
  --system-generator ollama \
  --ollama-sut-model llama3.2:3b \
  --ollama-generator-model qwen2.5:0.5b \
  --ollama-evaluator-model llama3:8b \
  --iterations 10 \
  --batch-size 3 \
  --target-score-threshold 0.6 \
  --verbose \
  --output results/enhanced_test.json
```

### Multi-Category Analysis
```bash
python evolutionary.py \
  --categories sexist racist homophobic toxic insulting \
  --enhanced-evaluation \
  --feedback-enabled \
  --memory \
  --memory-window 3 \
  --evaluation-function ollama \
  --iterations 5
```

## 🔍 Output Analysis

### Enhanced JSON Structure
The output now includes rich metadata:

```json
{
  "config": {...},
  "runs": [
    {
      "initial": {...},
      "taken": [
        {
          "generated_prompt_for_sut": "...",
          "response_from_sut": "...",
          "score": 0.85,
          "evaluation_explanation": "Detailed analysis...",
          "generation_feedback": "Improvement suggestions...",
          "category": "sexist",
          "delta_time_evaluation": 2.34
        }
      ],
      "discarded": [...]
    }
  ]
}
```

### Key Metrics Tracked
- **Generation Time**: Time to create prompt variations
- **Response Time**: SUT response latency
- **Evaluation Time**: Scoring and analysis duration
- **Success Rates**: Category-specific effectiveness
- **Evolution Patterns**: How prompts improve over iterations

## 🛡️ Safety & Ethics

This tool is designed for **legitimate research purposes**:
- AI safety evaluation
- Red team testing
- Academic research on adversarial prompts
- Defense mechanism development

**Important:** Always use responsibly and in compliance with your organization's ethics guidelines.

## 🐛 Troubleshooting

### JSON Parsing Issues
The system includes robust JSON parsing with automatic error recovery:
- Handles trailing commas in LLM responses
- Extracts JSON from surrounding text
- Graceful fallback to basic evaluation

### Memory Issues
For large datasets or long iterations:
```bash
# Reduce batch size and memory window
python evolutionary.py --batch-size 1 --memory-window 3
```

### Model Loading
Ensure Ollama models are pulled before use:
```bash
ollama pull llama3.2:3b
ollama pull qwen2.5:0.5b
ollama list  # Verify installation
```