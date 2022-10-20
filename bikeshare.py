import time
import pandas as pd
import numpy as np

city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input("To view the available bikeshare data, type:\n Chicago\n or New York City\n or Washington\n  ").lower()
    while city not in city_data.keys():
        print("that\'s invalid input")
        city = input("To view the available bikeshare data, type:\n Chicago\n or New York City\n or Washington\n  ").lower()

    months = [ "january","february", "march","april","may","june","all"] # six months only and the string "all"
    month = input("To filter {}\'s data by a particular month, please type the month or all for not filtering by month:\n -january\n -february\n -March\n -April\n -May\n -june\n -All\n  ".format(city)).lower()
    while month not in months:
        print("that\'s invalid input")
        month = input("To filter {}\'s data by a particular month, please type the month or all for not filtering by month:\n -january\n -february\n -March\n -April\n -May\n -june\n -All\n  ".format(city)).lower()

    days = ["mon","tues","wed","thur","fri","sat", "sun","all"]
    day = input("To filter data by a particular day, kindly type the abbreviated day name such as (Sat, Sun, Mon, Tues, Wed, thur, Fri) or all for not filtering by day:\n  ").lower()
    while day not in days:
        print("that\'s invalid input")
        day = input("To filter data by a particular day, kindly type the abbreviated day name such as (Sat, Sun, Mon, Tues, Wed, thur, Fri) or all for not filtering by day:\n  ").lower()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    # load data file into a dataframe
    df = pd.read_csv(city_data[city])
    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    # extract month and day of week from the Start Time column to create a month column and a day of week column
    df["month"] = df["Start Time"].dt.month
    df["day of week"] = df["Start Time"] .dt.day_name()
    df["hour"] = df["Start Time"].dt.hour

    # filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ["january","february", "march","april","may","june"]
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df["day of week"].str.startswith(day.title())]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df["month"].mode()[0]
    print("The most common month: " , most_common_month)

    # display the most common day of week
    most_common_day = df["day of week"].mode()[0]
    print("The most common day of week: " , most_common_day)

    # display the most common start hour
    most_common_start_hour = df["hour"].mode()[0]
    print("The most popular hour: " , most_common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df["Start Station"].mode()[0]
    print("The most commonly used start station: " , most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df["End Station"].mode()[0]
    print("The most commonly used end station: " , most_common_end_station)

    # display most frequent combination of start station and end station trip
    df["Combination"] = df["Start Station"] + " to " + df["End Station"]
    most_frequent_combination = df["Combination"].mode()[0]
    print("The most common trip from start station to end station: " , most_frequent_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("Total Duration: " , total_travel_time)


    # display mean travel time
    average_travel_time = df["Trip Duration"].mean()
    print("Average Duration: " , average_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df["User Type"].value_counts()
    print(user_type)


    # Display counts of gender
    print('\nCalculating Counts of Gender...\n')
    try:
        gender_counts = df["Gender"].value_counts()
        print(gender_counts)
    except (KeyError):
        print("No Gender Data to Share.")
    finally:
        print("Done!")


    # Display earliest, most recent, and most common year of birth
    print('\nCalculating earliest, most recent, and most popular year of birth...\n')
    try:
        the_youngest = df["Birth Year"].max()
        the_oldest = df["Birth Year"].min()
        the_common_year = df["Birth Year"].mode()[0]
        print("The oldest year of birth: ", the_oldest)
        print("The youngest year of birth: ", the_youngest)
        print("The most popular year of birth: ", the_common_year)
    except (KeyError):
        print("No Birth Year Data to Share.")
    finally:
        print("Done!")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(city):
    print("\nRaw Data is available to check....   \n")
    display_raw = input("May you want to have a look on the raw data? Type Yes or No. \n").lower()

    while display_raw == "yes":
        try:
            for chunk in pd.read_csv(city_data[city], chunksize = 5):
                print(chunk)
                display_raw = input("May you want to have a look on the raw data? Type Yes or No. \n").lower()
                if display_raw != "yes":
                    print("Thank You!")
                    break
            break
        except (KeyboardInterrupt):
            print("Thank You.")

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day)
        df = load_data(city, month , day)
        print(df.head())
        #print(df.columns)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
