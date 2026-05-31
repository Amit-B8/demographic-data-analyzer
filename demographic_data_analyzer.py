import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("adult.data.csv")

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = pd.Series(df['race']).value_counts()

    # What is the average age of men?
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)
    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round((df[df['education'] == 'Bachelors'].shape[0] / df.shape[0]) * 100, 1)

    # This will check what percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # Checks what percentage of people without advanced education make more than 50K?
    # with `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    # ~ means not in Pandas so this is opposite of above
    lower_education = df[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]

    # percentage with salary > 50K
    # Take the higher education group and find who makes > 50K
    rich_in_higher_ed = higher_education[higher_education['salary'] == '>50K']
    # Divide the number of rich people by the total number of people in that group
    rich_fraction = rich_in_higher_ed.shape[0] / higher_education.shape[0]
    # Multiply by 100 and round to one decimal
    higher_education_rich = round(rich_fraction * 100, 1)
    # Take the lower education group and find who makes >50K
    rich_in_lower_ed = lower_education[lower_education['salary'] == '>50K']
    # Divide the number of rich people by the total number of people in that group
    rich_fraction_lower = rich_in_lower_ed.shape[0] / lower_education.shape[0]
    # Multiply by 100 and round to one decimal
    lower_education_rich = round(rich_fraction_lower * 100, 1)

    # What is the minimum number of hours a person works per week which is the hours-per-week feature
    min_work_hours = df['hours-per-week'].min()

    # Checks what percentage of the people who work the minimum number of hours per week have a salary of > 50K 
    num_min_workers = df[df['hours-per-week'] == min_work_hours].shape[0]
    rich_percentage = round((df[(df['hours-per-week'] == min_work_hours) & (df['salary'] == '>50K')].shape[0] / num_min_workers) * 100, 1) if num_min_workers > 0 else 0

    # checks what country has the highest percentage of people that earn >50K
    # Now you just extract the winner
    df['is_rich'] = df['salary'] == '>50K'
    stats = df.groupby('native-country')['is_rich'].mean() * 100
    highest_earning_country = stats.idxmax()
    highest_earning_country_percentage = round(stats.max(), 1)

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = (df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
                     ['occupation']
                     .value_counts()
                     .idxmax())

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
