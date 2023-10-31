# OKR Evaluation for Researchers, Teams, and Organization

This project is designed to evaluate the Objectives and Key Results (OKR) for researchers, teams, and the entire organization. The process involves cleaning the initial manuscript, calculating the OKR, and handling special cases for later manual validation. The results are then transformed into text files, making them ready for processing with large language models.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Special Cases Handling](#special-cases-handling)
- [Caution: Naming and Structure of TXT Files](#caution-naming-and-structure-of-txt-files)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/OuHaoyun/okr-evaluation.git
   cd okr-evaluation
   ```
2. Set up the environment:

   ```bash
   chmod +x setup_env.sh
   ./setup_env.sh
   ```
3. Activate the environment:

   ```bash
   conda activate okr-evaluation
   ```

## Usage

1. Place your data in the appropriate directory as specified in `constants.py`.
2. Run the main script:

   ```bash
   python main.py
   ```
3. The results will be saved in the directories specified in `constants.py`.

## Project Structure

- `main.py`: The main script that orchestrates the entire OKR evaluation process.
- `constants.py`: Contains constants such as data paths and other configuration details.
- `utils.py`: Contains utility functions for reading files, data cleaning, OKR calculations, and more.
- `requirements.txt`: Lists the dependencies required for the project.
- `setup.sh`: Bash script to set up the environment and install the required dependencies.

## Special Cases Handling

For special cases that cannot be automatically processed, they are saved in the `df_special` DataFrame and exported to an intermediate Excel file. This allows for manual validation and ensures that no data is lost or misinterpreted during the automated processing.

## ⚠️ Caution: Naming and Structure of TXT Files

When working with the generated TXT files from the Excel or DataFrame outputs, it's crucial to be meticulous about their naming conventions and internal structure. The name, content, and structure of these TXT files directly influence the retrieval efficiency of the LLM-based chatbot application. Any inconsistencies or deviations from the expected format can lead to suboptimal performance or even errors in the chatbot's responses. Ensure that any modifications or extensions to the code maintain the integrity of these TXT outputs to guarantee seamless integration with the chatbot system.
