# Common Mistakes Dashboard

**Common Mistakes Dashboard** is an interactive data visualization project designed to analyze common student mistakes in self-paced math courses. The project processes raw CSV data from multiple courses (e.g., Prealgebra 1, Prealgebra 2, Algebra A), cleans it, and provides an interactive Streamlit dashboard for exploring the data.

## Features

- **Data Ingestion & Preprocessing**
  - Load raw CSV files from `data/raw/` for different courses.
  - Clean and process the data (e.g., compute combined wrong percentages from the top three wrong answers).
  - Save cleaned data to `data/processed/` for use by the dashboard.

- **Interactive Dashboard**
  - Choose which course to visualize using a course picker.
  - Filter data by minimum number of responses.
  - Toggle optional columns (e.g., `%failed`, `%giveup`, `%trigger_goto`, `failed_sum`) independently.
  - Visualize data with interactive charts (e.g., a bubble/scatter chart showing combined wrong % vs. number of responses).

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/common-mistakes.git
    cd common-mistakes
    ```

2. **Set up a virtual environment:**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use: env\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Install the package in editable mode:**
    ```bash
    pip install -e .
    ```
    
## Usage

### Preprocessing Data

Run the following command to process all raw CSV files and save the cleaned versions to `data/processed/`:

```bash
python -m src.data.process_all
```

### Running the Dashboard

Start the Streamlit app with:

```bash
streamlit run streamlit_app.py
```     

### Running Tests

Run the following command to execute all tests:

```bash
pytest
```

### License

This project is licensed under the MIT License. 






