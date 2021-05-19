import time
import pandas as pd


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input(
        '\n\nPlease enter the name of the city for which you would like to see bikeshare data.\n'
        'Chicago, New York City, and Washington are available.\n')
    city = city.lower()

    # city input validation
    while city not in ['chicago', 'new york city', 'washington']:
        print('\nThe city name you entered isn\'t valid. Please enter the full city name.'
              '\nData is available for Chicago, New York City, and Washington.')
        city = input(
            '\n\nPlease enter the name of the city for which you would like to see bikeshare data.\n')
        city = city.lower()

    # get user input for month (all, january, february, ... , june)

    month = input(
        '\nPlease enter the full name of the month for which you would like to see bikeshare data.'
        '\nData is available between January and June.'
        '\nIf you do not want to filter by month, please enter "all".\n')
    month = month.lower()

    # month input validation
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        print('\nYour input isn\'t a valid month name. Please enter the full month name.'
              '\nData is available between January and June.\n'
              'If you do not want to filter by month, please enter "all".')
        month = input(
            '\n\nPlease enter the full name of the month for which you would like to see bikeshare data.\n')
        month = month.lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input(
        '\nPlease enter the day of the week for which you would like to see bikeshare data.\n'
        'If you do not want to filter by day of the week, please enter "all".\n')
    day = day.lower()

    # day of the week input validation
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        print('\nYour input isn\'t a valid day weekday.'
              ' Please enter the full weekday name in singular form (e.g. Saturday).')
        print('If you do not want to filter by day of the week, please enter "all".\n')
        day = input(
            '\nPlease enter the day of the week for which you would like to see bikeshare data.\n')
        day = day.lower()

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
    month_dic = {'january': 1,
                 'february': 2,
                 'march': 3,
                 'april': 4,
                 'may': 5,
                 'june': 6}

    day_dic = {'monday': 0,
               'tuesday': 1,
               'wednesday': 2,
               'thursday': 3,
               'friday': 4,
               'saturday': 5,
               'sunday': 6}

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.dayofweek
    df['Hour'] = df['Start Time'].dt.hour
    df['Stations Combination'] = 'from ' + df['Start Station'] + ' to ' + df['End Station']

    if month != 'all':
        filtr_month = (df['Month'] == month_dic[month])
        df = df.loc[filtr_month]

    if day != 'all':
        filtr_day = (df['Day'] == day_dic[day])
        df = df.loc[filtr_day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    month_dic = {1: 'January',
                 2: 'February',
                 3: 'March',
                 4: 'April',
                 5: 'May',
                 6: 'June'}

    day_dic = {0: 'Monday',
               1: 'Tuesday',
               2: 'Wednesday',
               3: 'Thursday',
               4: 'Friday',
               5: 'Saturday',
               6: 'Sunday'}

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most popular month is', month_dic[df['Month'].mode()[0]])

    # display the most common day of week
    print('The most popular weekday is', day_dic[df['Day'].mode()[0]])

    # display the most common start hour
    print('The most common start hour is', df['Hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    print('The most common start station is', df['Start Station'].mode()[0])

    # display most commonly used end station

    print('The most common end station is', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('The most common start and end stations combination is',
          df['Stations Combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time was:', df['Travel Time'].sum())

    # display mean travel time
    print('The mean travel time was:', df['Travel Time'].mean().round('1s'))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The counts of user types are the following:\n')
    print(df['User Type'].value_counts().to_string())

    # Display counts of gender
    # Gender data is not available for Washington
    if 'Gender' in df.columns:
        print('\nThe user gender distribution is the following:\n')
        print(df['Gender'].value_counts().to_string())

    # Display earliest, most recent, and most common year of birth
    # Year of birth data is not available for Washington
    if 'Birth Year' in df.columns:
        print('\nThe earliest birth year is:', int(df['Birth Year'].min()))
        print('The most recent birth year is:', int(df['Birth Year'].max()))
        print('The most common birth year is:', int(df['Birth Year'].mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def individual_data(df):
    # Asks user if they would like to see five individual records at a time.
    ind_data = input('Would you like to see five individual records? Enter yes or no.\n')
    disp_start_row = 0

    while ind_data.lower() == 'yes':
        print(df.iloc[disp_start_row:disp_start_row+5])
        disp_start_row += 5
        ind_data = input(
            'Would you like to see five more individual records? Enter yes or no.\n').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        individual_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
