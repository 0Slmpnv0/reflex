
# Data Visualization Toolkit

## Overview
Python toolkit for generating interactive visualizations from JSON data with date filtering capabilities. Provides 7 specialized functions for different analytical scenarios, all leveraging Plotly's `plotly_dark` theme for consistent styling. Processes nested JSON structures and handles temporal/numerical/categorical data relationships.

## Installation
```bash
pip install pandas plotly
```

## Usage
### Data Format Requirements
Input JSON must contain:
```json
{
  "date": ["YYYY-MM-DD", ...],
  "report": [
    {"metric1": value, "metric2": value, ...},
    ...
  ]
}
```

### Common Parameters
- `user_data`: JSON string matching above format
- `date_limit`: Tuple (start_date, end_date) in YYYY-MM-DD
- All functions raise `ValueError` for invalid date ranges

## Functions Overview

### 1. prepare_data()
**Purpose**: Core data transformer  
- Converts nested JSON to flat DataFrame
- Handles date conversion and structural validation

### 2. number_tag()
**Visualization**: Horizontal bar chart  
- Compares numerical averages across categories
- **Parameters**:
  - `number_param_name`: Metric to average
  - `tag_param_name`: Grouping category

### 3. number_date()
**Visualization**: Time-series line chart  
- Temporal aggregation (daily/weekly/monthly)
- **Parameters**:
  - `scale`: Aggregation period
  - Validation for minimum date ranges

### 4. tag_date()
**Visualization**: Stacked bar chart  
- Tag frequency analysis over time
- **Parameters**:
  - `scale`: Weekly/monthly grouping
  - Automatic top tag selection

### 5. checkbox_date()
**Visualization**: Pie chart  
- Boolean distribution analysis
- Time-filtered ratio visualization

### 6. number_checkbox()
**Visualization**: Grouped bar chart  
- Cross-category numerical comparisons
- Boolean segmentation analysis

### 7. tag_checkbox()
**Visualization**: Horizontal histogram  
- Boolean fulfillment rates by category
- Percentage-based ranking

## Example Usage
```python
# Sample data preparation
import json
data = {
    "date": ["2023-01-01", "2023-01-02"],
    "report": [
        {"sales": 150, "active": True, "category": "A"},
        {"sales": 200, "active": False, "category": "B"}
    ]
}
json_data = json.dumps(data)

# Generate visualization
html_plot = number_tag(
    user_data=json_data,
    number_param_name="sales",
    tag_param_name="category"
)
```

## Technical Notes
1. **Date Handling**:
   - Automatic datetime conversion
   - Inclusive range filtering
   - Month analysis requires ≥31 day ranges

2. **Visual Defaults**:
   - Consistent dark theme (`plotly_dark`)
   - High-resolution PNG output (scale=5)
   - Automatic sorting for analytical clarity

3. **Error Protection**:
   - Pre-validation of date sequences
   - Type checking for scale parameters
   - Empty plot handling for missing data

4. **Performance**:
   - In-place DataFrame modifications
   - GroupBy optimizations
   - Memory-efficient JSON parsing


P.S.
Yes, you guessed this right. The readme is totally AI generated, but I swear I read it! Guess, I would do it even worse, so thats the rigth decision