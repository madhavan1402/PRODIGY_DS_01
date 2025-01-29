import pandas as pd
import matplotlib.pyplot as plt
0
# File paths
file_population = 'API_SP.POP.TOTL_DS2_en_csv_v2_900.csv'
file_metadata = 'Metadata_Country_API_SP.POP.TOTL_DS2_en_csv_v2_900.csv'
file_indicators = 'Metadata_Indicator_API_SP.POP.TOTL_DS2_en_csv_v2_900.csv'  # Update with the actual file name of the indicator dataset

# Load datasets
population_data = pd.read_csv(file_population, skiprows=4)
metadata = pd.read_csv(file_metadata)
indicators = pd.read_csv(file_indicators)

# Merge population data with metadata
merged_data = pd.merge(population_data, metadata, left_on='Country Code', right_on='Country Code', how='inner')

# Clean and rename columns for clarity
merged_data = merged_data.rename(columns={'2020': 'Population_2020', 'Region': 'Region', 'IncomeGroup': 'Income Group'})
merged_data = merged_data[['Country Name', 'Population_2020', 'Region', 'Income Group']]
merged_data['Population_2020'] = pd.to_numeric(merged_data['Population_2020'], errors='coerce')
merged_data = merged_data.dropna(subset=['Population_2020', 'Region', 'Income Group'])

# Merge with indicator dataset to attach descriptions (if applicable)
indicator_description = indicators[indicators['INDICATOR_CODE'] == 'SP.POP.TOTL']['INDICATOR_NAME'].values[0]

# Group by region and sum population
region_population = merged_data.groupby('Region')['Population_2020'].sum().sort_values(ascending=False)

# Visualization
plt.figure(figsize=(10, 6))
region_population.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title(f'Regional Population Distribution (2020)\n{indicator_description}', fontsize=14)
plt.xlabel('Region', fontsize=12)
plt.ylabel('Total Population', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save and display the plot
plt.savefig('regional_population_distribution.png')
plt.show()
