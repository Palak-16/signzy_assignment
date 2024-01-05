import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = '/content/Assignment - Hiring Interns.xlsx'
data = pd.read_excel(file_path, sheet_name=1)

# Basic Data Cleaning: Filling missing values for analysis
data_cleaned = data.fillna('Unknown')

# Enhanced categorization of economic segments
def categorize_economic_segment(row):
    premium_manufacturers = ['ROYAL ENFIELD', 'HARLEY DAVIDSON', 'BMW']
    premium_models = ['BMW 1000RR', 'HARLEY STREET 750']

    if row['vehicleManufacturerName'] in premium_manufacturers or row['model'] in premium_models:
        return 'Premium'
    elif row['vehicleCubicCapacity'] == 'Unknown' or (isinstance(row['vehicleCubicCapacity'], int) and row['vehicleCubicCapacity'] < 150):
        return 'Budget'
    else:
        return 'Mid-Range'

data_cleaned['EconomicSegment'] = data_cleaned.apply(categorize_economic_segment, axis=1)

# Define more nuanced User Personas with different formula based on grossVehicleWeight
def define_user_persona(row):
    if row['EconomicSegment'] == 'Premium':
        if row['class'] == 'M-Cycle/Scooter':
            return 'Premium Scooter Rider'
        elif row['type'] == 'PETROL':
            return 'Premium Petrol Vehicle Owner'
        else:
            return 'Premium Vehicle Owner'
    elif row['EconomicSegment'] == 'Mid-Range':
        weight = row['grossVehicleWeight']
        if weight == 'Unknown':
            return 'Mid-Range Vehicle Owner (Unknown Weight)'
        try:
            weight = float(str(weight).replace(',', ''))
            if weight < 500:
                return 'Mid-Range Vehicle Owner (Lightweight)'
            elif weight < 1000:
                return 'Mid-Range Vehicle Owner (Medium Weight)'
            else:
                return 'Mid-Range Vehicle Owner (Heavyweight)'
        except ValueError:
            return 'Mid-Range Vehicle Owner (Invalid Weight)'
    else:
        if row['class'] == 'M-Cycle/Scooter':
            return 'Scooter Rider'
        elif row['type'] == 'PETROL':
            return 'Petrol Vehicle User'
        else:
            return 'General Vehicle Owner'

data_cleaned['UserPersona'] = data_cleaned.apply(define_user_persona, axis=1)

# Determine Buying Tendency of Insurance based on Economic Segment
def buying_tendency(row):
    if row['EconomicSegment'] == 'Premium':
        return 'High'
    elif row['EconomicSegment'] == 'Mid-Range':
        return 'Medium'
    else:
        return 'Low'

data_cleaned['InsuranceBuyingTendency'] = data_cleaned.apply(buying_tendency, axis=1)

# Assess Buying Capability of Insurance based on User Persona
def buying_capability(row):
    if row['EconomicSegment'] == 'Premium':
        if row['UserPersona'] == 'Premium Scooter Rider':
            return 'High'
        elif row['UserPersona'] == 'Premium Petrol Vehicle Owner':
            return 'Medium'
        else:
            return 'High'
    elif row['EconomicSegment'] == 'Mid-Range':
        return 'Medium'
    else:
        return 'Low'

data_cleaned['InsuranceBuyingCapability'] = data_cleaned.apply(buying_capability, axis=1)

# Visualization of User Personas
plt.figure(figsize=(14, 6))
sns.countplot(x='UserPersona', data=data_cleaned, order=data_cleaned['UserPersona'].value_counts().index)
plt.title('Distribution of User Personas')
plt.xticks(rotation=90)
plt.xlabel('User Persona')
plt.ylabel('Count')
plt.show()

# Visualization of Insurance Buying Tendency
plt.figure(figsize=(6, 4))
sns.countplot(x='InsuranceBuyingTendency', data=data_cleaned, order=['Low', 'Medium', 'High'])
plt.title('Insurance Buying Tendency')
plt.xlabel('Buying Tendency')
plt.ylabel('Count')
plt.show()

# Visualization of Insurance Buying Capability
plt.figure(figsize=(6, 4))
sns.countplot(x='InsuranceBuyingCapability', data=data_cleaned, order=['Low', 'Medium', 'High'])
plt.title('Insurance Buying Capability')
plt.xlabel('Buying Capability')
plt.ylabel('Count')
plt.show()
