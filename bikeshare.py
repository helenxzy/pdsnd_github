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
    validity = False

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input("\nWhich city would you like to filter by? (Choose from Chicago, New York City, Washington): ").strip().lower())
        if city not in ("chicago", "new york city", "washington"):
            print("\nInvalid entry. Please try again")
            continue
        else:
            print("\nIt looks like you want to see data for: '{}' ".format(city.title()))
            validity_check()
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("\nType in name of month to filter by (January, February, March, April, May, June or 'All' if no preference): ").strip().lower())

        if month not in ("january", "february", "march", "april", "may", "june", "all"):
            print("\nInvalid entry. Please type in month name (or \"all\" to select every month)")
            continue
        else:
            print("\nIt looks like you want to filter by: '{}' ".format(month.title()))
            validity_check()
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("\nType in name of day to filter by (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or 'All' if no preference): ").strip().lower())
        if day not in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday" , "sunday", "all"):
            print("Invalid entry. Please type in a valid day of week (or \"all\" to select every day)")
            continue
        else:
            print("\nIt looks like you want to filter by: '{}' ".format(day.title()))
            validity_check()
            break

    print("\nYou selected '{}' as city, '{}' as month, and '{}' as day. \nFiltering by your parameters....".format(city.title(), month.title(), day.title()))
    print()

    print('-'*40)
    return city, month, day

def validity_check():
    """Asks the user whether the input is correct. If not, give a chance for correction."""

    while True:
        validity = str(input("Is your input correct? Type 'yes' to continue and 'no' to restart: \n").strip().lower())
        if validity not in ("yes", "no"):
            print("\nInvalid entry. Please try again")
            continue
        elif validity == 'yes':
            break
        else:
            get_filters()


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month / day of week / hour from 'Start Time' to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding integer
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    dictionary = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June',
                  '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}

    # TO DO: display the most common month
    popular_month = df['Month'].mode()[0]
    month_in_string = dictionary[str(popular_month)]
    print("Most common month: ", month_in_string)

    # TO DO: display the most common day of week
    popular_day = df['Day'].mode()[0]
    print("Most common day of the week: ", popular_day)

    # TO DO: display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print('Most common start hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("Most commonly used start station: ", start_station)

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("Most commonly used end station: ", end_station)

    # TO DO: display most frequent combination of start station and end station trip
    pair = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).reset_index(name="counts")
    freq_start_pair = pair['Start Station'][0]
    freq_end_pair = pair['End Station'][0]
    print("Most frequent combination:  Start at {}, End at {}".format(freq_start_pair, freq_end_pair))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time in seconds: ", total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time in seconds: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = df["User Type"].value_counts()
    print(user_type_count)

    # TO DO: Display counts of gender
    if "Gender" in df.columns:
        gender_count = df["Gender"].value_counts()
        # count null values
        nan_values = df["Gender"].isna().sum()
        print("\nCounts by Gender: \n{}\n \n*Note: there were '{}' NaN values for gender column".format(gender_count,nan_values))
    else:
        print("\nThe dataset does not have a 'Gender' column.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print("\nEarliest birth year: '{}'. \nMost recent birth year: '{}'. \nMost common birth year: '{}'.".format(earliest, most_recent, most_common))
    else:
        print("\nThe dataset does not have a 'Birth Year' column.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """
    Asks if the user would like to see some lines of data from the filtered dataset.
    Displays 5 (show_rows) lines, then asks if they would like to see 5 more.
    Continues asking until they say stop.
    """
    show_rows = 5
    rows_start = 0
    rows_end = show_rows - 1

    print('\n    Would you like to see some raw data from the current dataset?')
    while True:
        raw_data = input('      (yes or no):  ')
        if raw_data.lower() == 'yes':
            print('\n    Displaying rows {} to {}:'.format(rows_start + 1, rows_end + 1))
            print('\n', df.iloc[rows_start : rows_end + 1])
            rows_start += show_rows
            rows_end += show_rows
            print('-'*40)
            print('\n    Would you like to see the next {} rows?'.format(show_rows))
            continue
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
