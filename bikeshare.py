import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("Enter the name of the city:")
    city=input()
    while(city not in ['chicago','new york city', 'washington']):
        city = input("invalid input, retry..")

    # TO DO: get user input for month (all, january, february, ... , june)

    print("Enter the month:")
    month=input()
    while(month not in ['all','january','february','march','april','may','june','july','august','september','october','november','december']):
        month = input("invalid input, retry..")


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print("Enter the day:")
    day=input()
    while(day not in ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']):
        day = input("invalid input, retry..")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.DataFrame()
    # load data in the file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the start time column to dates..
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month from the date of start time and also day of week.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        months = ['january','february','march','april','may','june','july','august','september','october','november','december']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()] #no need to do like month, because we have day column.
    

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start = time.time()

    if df.empty:
        print('No data available for the selected filters.')
        print('-'*40)
        return

    # Extract hour from Start Time
    df['hour'] = df['Start Time'].dt.hour

    # Find the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
             'July', 'August', 'September', 'October', 'November', 'December']
    common_month = months[df['month'].mode()[0] - 1]
    print('Most popular month:', common_month)

    # Find the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most popular day of the week:', common_day)

    # Find the most common hour
    common_hour = df['hour'].mode()[0]
    print('Most popular hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if df.empty:
        print('No data available for the selected filters.')
        print('-'*40)
        return

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is:', start_station)

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is:', end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Start End Station'] = df['Start Station'] + ' to ' + df['End Station']
    start_end_station = df['Start End Station'].mode()[0]
    print('The most frequent combination of start station and end station trip is:', start_end_station)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if df.empty:
        print('No data available for the selected filters.')
        print('-'*40)
        return

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if df.empty:
        print('No data available for the selected filters.')
        print('-'*40)
        return

    # Display counts of user types
    try:
        user_types = df['User Type'].value_counts()
        print('Counts of user types:')
        print(user_types)
        print()
    except KeyError:
        print('No user type data available for this city.\n')

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print('Counts of gender:')
        print(gender_counts)
        print()
    except (KeyError, AttributeError):
        print('No gender data available for this city.\n')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print('Birth Year Statistics:')
        print(f'Earliest year of birth: {earliest_year}')
        print(f'Most recent year of birth: {recent_year}')
        print(f'Most common year of birth: {common_year}')
    except (KeyError, AttributeError, ValueError):
        print('No birth year data available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    print("Do you want to see 5 rows of the data? (yes or no)")
    userinput = input().lower()
    i=0
    while(userinput == 'yes' or userinput == 'y'):
        print(df.iloc[i:i+5])
        i+=5
        if(i>=len(df)):
            break
        userinput = input("Do you want to see 5 more rows? (yes or no)").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df.head())
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
