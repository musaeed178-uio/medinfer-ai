# AI-Based Medical Diagnosis Expert System

An AI-powered expert system that assists users in identifying possible diseases based on symptoms. Built with Prolog for knowledge representation and reasoning, and Python for the graphical user interface.

## Features

### Core Features
- Disease prediction from **25+ diseases**
- Symptom selection from **50+ symptoms**
- Rule-based inference using Prolog
- Weighted confidence scoring with severity weights
- Detailed explanation of diagnosis results
- Forward and backward chaining support

### Advanced Features
- **Patient Profile Management** - Save patient information (name, age, gender, blood type)
- **Diagnosis History** - Track all past diagnoses with timestamps
- **Statistics Dashboard** - Visual charts showing disease distribution and symptom frequency
- **Disease Encyclopedia** - Browse all diseases with descriptions, categories, and recommendations
- **Emergency Flags** - Critical conditions are highlighted for immediate attention
- **Symptom Search & Filter** - Search symptoms by name or filter by body system category
- **Dark/Light Theme** - Toggle between light and dark modes
- **Export Reports** - Export diagnosis results and history to text files
- **Disease Categories** - Diseases organized by type (viral, bacterial, respiratory, etc.)
- **Body System Organization** - Symptoms grouped by body system for easier selection

## Prerequisites

- Python 3.8+
- [SWI-Prolog](https://www.swi-prolog.org/) (must be installed and in system PATH)

## Installation

1. Install SWI-Prolog from https://www.swi-prolog.org/
2. Ensure SWI-Prolog is added to your system PATH
3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python gui.py
```

1. Set up your patient profile (optional)
2. Select symptoms from the organized checklist
3. Click **Diagnose** to see possible diseases
4. View confidence scores, categories, and explanations
5. Export reports or view history and statistics

## Project Structure

```
Medical_Expert_System/
├── gui.py              # Enhanced Tkinter GUI with tabs, themes, charts
├── controller.py       # Python-Prolog bridge (PySwip) with search/filter
├── medical_kb.pl       # Prolog knowledge base (25 diseases, 50+ symptoms)
├── patient_profile.py  # Patient profile and history management
├── report_exporter.py  # Report export to TXT format
├── requirements.txt    # Python dependencies
├── data/               # Auto-created: stores patient data and history
├── assets/             # Images and resources
└── screenshots/        # Application screenshots
```

## Knowledge Base

### Diseases (25+)
| Category | Diseases |
|----------|----------|
| Viral | Flu, Cold, COVID-19, Dengue, Chickenpox, Measles, Hepatitis A |
| Bacterial | Typhoid, Tuberculosis, UTI |
| Respiratory | Asthma, Pneumonia, Bronchitis |
| Neurological | Migraine, Insomnia |
| Metabolic | Diabetes |
| Cardiovascular | Hypertension |
| Other | Malaria, Anemia, Allergy, Sinusitis, Gastroenteritis, Heat Stroke, Depression, Arthritis |

### Symptoms (50+)
Organized by body system: General, Respiratory, Neurological, Gastrointestinal, Musculoskeletal, Skin, Cardiovascular, Urinary, Psychological, ENT

## Reasoning

- **Backward Chaining**: Prolog's default goal-driven reasoning
- **Forward Chaining**: Data-driven inference from symptoms to diseases
- **Weighted Confidence**: Severity-weighted symptom matching for more accurate scoring
- **Emergency Detection**: Flags life-threatening conditions automatically

## Technologies

- Python 3
- SWI-Prolog
- PySwip (Python-Prolog bridge)
- Tkinter (GUI)
- JSON (data persistence)

## Disclaimer

This system is for **educational and demonstration purposes only**. It is NOT a substitute for professional medical diagnosis. Always consult a qualified healthcare provider for medical advice.
