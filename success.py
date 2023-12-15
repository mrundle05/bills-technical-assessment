import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('TEN2018SeasonData.csv')
# look at TIMETOPRESSURE, TIMETOTHROW, 2MINUTE, DISTANCE, FIELDPOSITION, INTERCEPTION, INCOMPLETIONTYPE, PASSDEPTH, PASSDIRECTION, PASSER, PASSRECEIVERTARGET, PASSRESULT, PASSRUSHPLAYERS, PLAYENDFIELDPOSITION, QBPRESSURE, QBSCRAMBLE, TOUCHDOWN, PLAYCLOCK

# Filter rows where pff_PASSER is 'TEN 08 (QB)'
ten_08_data = data[data['pff_PASSER'] == 'TEN 08 (QB)']

# Select specific columns for analysis
selected_columns = [
    'pff_QUARTER', 'pff_DOWN', 'pff_TIMETOPRESSURE', 'pff_TIMETOTHROW', 'pff_2MINUTE', 'pff_DISTANCE',
    'pff_FIELDPOSITION', 'pff_INTERCEPTION', 'pff_INCOMPLETIONTYPE', 'pff_PASSDEPTH', 'pff_PASSDIRECTION',
    'pff_PASSER', 'pff_PASSRECEIVERTARGET', 'pff_PASSRESULT', 'pff_PASSRUSHPLAYERS', 'pff_PLAYENDFIELDPOSITION',
    'pff_QBPRESSURE', 'pff_QBSCRAMBLE', 'pff_TOUCHDOWN', 'pff_PLAYCLOCK'
]

# Filter rows where pff_PASSER is 'TEN 08 (QB)'
ten_08_data = data[data['pff_PASSER'] == 'TEN 08 (QB)']

# Group data by quarter and calculate the completion rate
quarterly_completion_rate = ten_08_data.groupby('pff_QUARTER')['pff_PASSRESULT'].value_counts(normalize=True).unstack().fillna(0)
completion_percentage = quarterly_completion_rate['COMPLETE'] /(quarterly_completion_rate['COMPLETE'] + quarterly_completion_rate['INCOMPLETE'] + quarterly_completion_rate['BATTED PASS'] + quarterly_completion_rate['INTERCEPTION'])*100

# Plot the bar chart for completion percentage per quarter
plt.bar(completion_percentage.index.astype(str), completion_percentage.values, color='blue')
plt.xlabel('Quarter')
plt.ylabel('Completion Percentage')
plt.title('Completion Percentage per Quarter')
plt.ylim(0, 100)  # Set the y-axis limit to percentage scale
plt.savefig('completionPerQuarter.png')
plt.clf()

# Group data by down and count the number of passes completed
down_completion_rate = ten_08_data.groupby('pff_DOWN')['pff_PASSRESULT'].value_counts(normalize=True).unstack().fillna(0)
completion_percentage = down_completion_rate['COMPLETE'] /(down_completion_rate['COMPLETE'] + down_completion_rate['INCOMPLETE'] + down_completion_rate['BATTED PASS'] + down_completion_rate['INTERCEPTION'])*100
completion_percentage = completion_percentage[completion_percentage.index != 0]

# Plot the bar chart for completion percentage per down
plt.bar(completion_percentage.index.astype(str), completion_percentage.values, color='blue', label='Completion Percentage')
plt.xlabel('Down')
plt.ylim(0, 100)
plt.ylabel('Completion Percentage')
plt.title('Completion Percentage per Down')

# Save the plot as an image file
plt.savefig('completionPerDown.png')
plt.clf()
# Filter rows where pff_PASSER is 'TEN 08 (QB)'
ten_08_data = data[data['pff_PASSER'] == 'TEN 08 (QB)'].copy()  # Create a copy to avoid the warning

# Extract minutes and seconds from pff_CLOCK and convert to total seconds
ten_08_data['pff_CLOCK'] = ten_08_data['pff_CLOCK'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))

# Group data by time and calculate the completion rate
completion_rate_by_time = ten_08_data.groupby(ten_08_data['pff_CLOCK'] < 120)['pff_PASSRESULT'].value_counts(normalize=True).unstack().fillna(0)
completion_percentage = completion_rate_by_time['COMPLETE'] /(completion_rate_by_time['COMPLETE'] + completion_rate_by_time['INCOMPLETE'] + completion_rate_by_time['BATTED PASS'] + completion_rate_by_time['INTERCEPTION'])*100

# Plot the bar chart for completion percentage under 2 minutes and not under 2 minutes
labels = ['Under 2 Minutes', 'Not Under 2 Minutes']
plt.bar(labels, completion_percentage.values, color='blue', label='Completion Percentage')
plt.xlabel('Time Condition')
plt.ylabel('Completion Percentage')
plt.ylim(0, 100)
plt.title('Completion Percentage Under 2 Minutes vs Not Under 2 Minutes')

# Save the plot as an image file
plt.savefig('completion2minutes.png')
plt.clf()

# Categorize pass depth into ranges
ten_08_data['PassDepthCategory'] = pd.cut(ten_08_data['pff_PASSDEPTH'], bins=[0, 5, 15, float('inf')], labels=['0-5 yards', '5-15 yards', 'More than 15 yards'])

# Group data by pass depth category and calculate the completion rate
completion_rate_by_depth = ten_08_data.groupby('PassDepthCategory')['pff_PASSRESULT'].value_counts(normalize=True).unstack().fillna(0)
completion_percentage = completion_rate_by_depth['COMPLETE'] / (completion_rate_by_depth['COMPLETE'] + completion_rate_by_depth['INCOMPLETE'] + completion_rate_by_depth['BATTED PASS'] + completion_rate_by_depth['INTERCEPTION']) * 100

# Plot the bar chart for completion percentage by pass depth category
labels = completion_rate_by_depth.index.astype(str)
plt.bar(labels, completion_percentage.values, color='blue', label='Completion Percentage')
plt.xlabel('Pass Depth Category')
plt.ylabel('Completion Percentage')
plt.ylim(0, 100)
plt.title('Completion Percentage by Pass Depth Category')

# Save the plot as an image file
plt.savefig('completionPassDepth.png')
plt.clf()

# Create time-to-throw intervals
bins = [0, 1.5, 3.0, float('inf')]
labels = ['0-1.5', '1.5-3.0', '3.0+']
ten_08_data['TimeToThrowInterval'] = pd.cut(ten_08_data['pff_TIMETOTHROW'], bins=bins, labels=labels, right=False)

# Group data by time-to-throw interval and quarter, then calculate completion rate
grouped_data = ten_08_data.groupby(['TimeToThrowInterval'])['pff_PASSRESULT'].value_counts(normalize=True).unstack().fillna(0)
completion_percentage = grouped_data['COMPLETE'] / (grouped_data['COMPLETE'] + grouped_data['INCOMPLETE'] + grouped_data['BATTED PASS'] + grouped_data['INTERCEPTION']) * 100


plt.bar(labels, completion_percentage.values, color='blue', label='Completion Percentage')
plt.xlabel('Time to Throw Interval')
plt.ylabel('Completion Percentage')
plt.title('Completion Percentage per Time-to-Throw Interval')
plt.ylim(0, 100)
plt.savefig('completiontimetothrow.png')
plt.clf()

# Filter rows where pff_PASSER is 'TEN 08 (QB)' and the play resulted in a touchdown
touchdowns = data[(data['pff_PASSER'] == 'TEN 08 (QB)') & (data['pff_TOUCHDOWN'].str[:3] == 'TEN') & (data['pff_PASSRESULT'] == 'COMPLETE')]

# Get the total number of touchdowns
total_touchdowns = touchdowns.shape[0]

print(f'Total Touchdowns Thrown by TEN 08 (QB): {total_touchdowns}')
# Filter rows where pff_PASSER is 'TEN 08 (QB)' and the play resulted in an interception
interceptions = data[(data['pff_PASSER'] == 'TEN 08 (QB)') & (data['pff_PASSRESULT'] == 'INTERCEPTION')]

# Get the total number of interceptions
total_interceptions = interceptions.shape[0]

print(f'Total Intercpptions Thrown by TEN 08 (QB): {total_interceptions}')