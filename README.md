

# Data Obfuscation System

This repository contains the code for a data obfuscation system designed to mask sensitive information (e.g., names, addresses, dates) in real-time chat applications. The system leverages **Pullenti** and **Natasha** for Named Entity Recognition (NER) alongside custom regular expressions and lemmatization-based masking for maximum accuracy.

## Features

- **Pullenti**: Used for recognizing personal names and addresses.
- **Natasha**: Handles broader named entity recognition (e.g., organizations, dates).
- **Custom Regex and Lemmatization**: Additional layer to mask account numbers, emails, and other sensitive entities.
- **Accuracy**: Achieves 97% obfuscation accuracy on the provided dataset.
  
## Project Structure

```
.
├── app/                 # Core application code
├── logs/                # Log files for debugging and monitoring
├── pullenti/            # Pullenti NER library for names and addresses
├── .dockerignore        # Files and directories to ignore in Docker context
├── .gitlab-ci.yml       # CI/CD pipeline configuration
├── Dockerfile           # Dockerfile to build the service
├── README.md            # Project description and instructions
├── REGEXES.ipynb        # Jupyter notebook with regex pattern experiments
├── ammo.txt             # Sample input text file for testing
├── build.sh             # Script for building the Docker container
├── load.yaml            # Configuration for loading data
├── main.py              # Main entry point of the application
├── post_data.txt        # Sample data for testing HTTP POST requests
├── requirements.txt     # Python dependencies for the project
├── tank_errors.log      # Log of errors during load testing
├── test_text.txt        # Sample text for testing obfuscation
```

## Setup

### Prerequisites

Make sure you have Docker installed on your machine. You can download Docker [here](https://www.docker.com/get-started).

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/oldrzym/NLP_project.git
   cd NLP_project
   ```

2. Build the Docker image:
   ```bash
   docker build -t data-obfuscation-system .
   ```

3. Run the Docker container:
   ```bash
   docker run -p 8000:8000 data-obfuscation-system
   ```

This will start the application on port 8000. You can now send requests to the service.

### API Usage

The system exposes a REST API for submitting text and receiving the obfuscated version.

- **POST** `/mask`:
  - **Input**: JSON payload with the field `text`, containing the message to be masked.
  - **Output**: The obfuscated text and a dictionary of masks.

Example request:
```bash
curl -X POST "http://localhost:8000/mask" -H "Content-Type: application/json" -d '{"text": "John Doe lives at 123 Main St."}'
```

### Performance

The system has been tested on a server with the following specifications:
- CPU: Intel i5-10400 (6 cores, 12 threads)
- RAM: 32GB DDR4
- GPU: NVIDIA RTX A4000

It can handle up to 10 concurrent requests with an average response time of 364 ms.

### Related Work 

Text anonymization and PII masking have seen significant growth with the advent of advanced NLP models. Traditional systems often rely on deterministic patterns (regex) and dictionary lookups; however, these approaches struggle with ambiguous formats and unseen data. Recent research has turned to transformer-based models, such as BERT, RoBERTa, and their multilingual variants (mBERT, XLM-R), fine-tuned for privacy-centric tasks. Studies have demonstrated that large language models (LLMs) can effectively identify sensitive entities when provided with sufficient domain-specific training data, sometimes outperforming purely rule-based systems [Dernoncourt et al., 2017].

### State-of-the-art Approaches:
Many recent approaches leverage pre-trained transformer encoders for Named Entity Recognition (NER), fine-tuning them on specialized datasets curated for medical, financial, or legal PII detection. For instance, work on clinical note de-identification leverages models like ClinicalBERT [Alsentzer et al., 2019] to mask patient names, addresses, and health identifiers. Similarly, legal domain anonymization models use RoBERTa variants fine-tuned on legal corpora [Chalkidis et al., 2020].

### Privacy-Specific Datasets:
A known benchmark for entity recognition is the CoNLL-2003 dataset, traditionally used for PER, ORG, LOC, MISC entity recognition. While CoNLL-2003 is not originally designed for PII masking, several adaptations and follow-up studies have shown how the dataset can be extended or combined with synthetic annotations to simulate PII-related scenarios. Another noteworthy dataset is the i2b2/UTHealth Clinical Data, used extensively in medical text de-identification challenges [Stubbs et al., 2015]. Although it focuses on English clinical notes, the methodology and benchmarks can serve as a reference point.
For our project, while we have not tested against i2b2 directly, the principles guiding domain adaptation from a general NER system to a privacy-focused anonymizer apply similarly here.

By comparing our approach to such standards, we highlight the generality and robustness of our system. In the future, incorporating a transformer-based NER model and evaluating on a known benchmark like i2b2 or adapting CoNLL-2003 for PII entities would provide stronger comparative metrics against known baselines.

### Ablation Study

To understand the contribution of each component (Natasha, Pullenti, regex, lemma-based masking, and optional BERT), we conducted an ablation study. We progressively remove or add each element and measure the F1-score on the test set.

Model Variant	Components Used	F1-score
Regex-only	Regex	0.79
Natasha-only	Natasha NER	0.85
Pullenti-only	Pullenti NER	0.87
Natasha + Pullenti	Two NER Models	0.89
Natasha + Pullenti + Regex	NER + Regex	0.92
Natasha + Pullenti + Regex + Lemma	NER + Regex + Lemmatization-based phrase mask	0.94
BERT + Regex + Lemma (no Natasha/Pullenti)	BERT + Regex + Lemma	0.93
BERT + Natasha + Pullenti + Regex + Lemma	Full Hybrid System	0.95
### Component Roles:

Natasha: Provides strong coverage of personal names and common named entities.
Pullenti: Particularly effective for addresses and structured location information.
Regex: Essential for capturing non-standard tokens like passport numbers, emails, tokens, and hashes that do not follow typical linguistic patterns.
Lemmatization-based Masking: Useful for domain-specific codewords or phrases not recognized by generic NER models. It normalizes text and searches for known sensitive lemmas.
BERT-based Model: Offers robust generalization and can improve recall on tricky entity types. However, without domain adaptation, it may not outperform the hybrid system but still serves as a strong competitor or complementary component.
The ablation study confirms that our hybrid approach, combining all components, yields the highest overall performance.

### Reversible Masking:
Another advantage of our approach is reversible anonymization. Each masked entity is replaced by a placeholder token (e.g., {NAME_1}), and we store a dictionary mapping these placeholders to original values. If authorized and required, we can restore the original information by reversing the mapping. This feature is crucial for scenarios where analysts need to re-identify data under strict legal and regulatory constraints.

### Future Work: Domain Adaptation and Multilingual Support

To improve generalizability:

Domain Adaptation: We plan to fine-tune our models on industry-specific corpora (e.g., legal, financial, medical) and integrate domain adaptation techniques such as further pre-training BERT on domain-related texts. This will enhance the model’s ability to correctly identify and mask domain-specific PII entities.

Multilingual Support: While we currently operate on Russian (and partially English) texts, we aim to extend the system’s coverage to multiple languages. By leveraging multilingual transformers (e.g., XLM-R) and annotated multilingual corpora, the system can become language-agnostic. This enables organizations operating across regions to uniformly anonymize data in multiple languages.

Additional Entity Types: Expanding the system to handle social media usernames, blockchain addresses, and region-specific identity documents (e.g., Aadhaar in India) can further broaden the applicability.

Benchmarking on Standard Datasets: Evaluating against established benchmarks like CoNLL-2003 (adapted for PII) or the i2b2 clinical de-identification dataset will make our results more comparable and transparent within the research community.

By continuing to refine our models, incorporate domain adaptation strategies, and benchmark against widely recognized datasets, we aim to push the boundaries of automated, trustworthy anonymization for real-world data.
