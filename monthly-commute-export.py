#
from argparse import ArgumentParser
import strava_if

if __name__ == "__main__":

    #
    # Parse command line parameters
    #
    parser = ArgumentParser()

    # Month: 1-12
    parser.add_argument("-m", "--month", action="append", type=int)

    # Year: 1900-9999
    parser.add_argument("-y", "--year", action="append", type=int)

    # Mode: 'C' for Commute flag based search, 'T' for Tag ('#xxx') based search
    parser.add_argument("-M", "--mode", action="append", type=str)

    # Tag: Value of the tag
    parser.add_argument("-T", "--tag", action="append", type=str)

    args = parser.parse_args()

    year = args.year[0]
    month = args.month[0]
    if args.mode[0] == 'C':
        com_or_tag = True
    elif args.mode[0] == 'T':
        com_or_tag = False
        tag_value = args.tag[0]
    else:
        print("ERROR: Wrong user input. Exit.")
        exit(-2)

    #
    # Connect and authenticate to your Strava account
    #
    if strava_if.authenticate_to_strava() < 0:
        print("ERROR: Failed to authenticate to Strava. Exit.")
        exit(-1)

    #
    # Print general report info
    #
    athlete = strava_if.get_athlete()

    print("Athlete: {} - {} {}, based in {}, {}".format(athlete.id, athlete.firstname, athlete.lastname, athlete.city,
                                                            athlete.country))

    print("Commute monthly report")
    print("  Athlete {}\n  Month {y:04d}-{m:02d}.\n".format(
        athlete.firstname + " " + athlete.lastname, y=year, m=month))

    # Search and print relevant activities (CSV format)
    print("Athlete_ID; Activity_name; Activity_date; Moving_time; Elapsed_time; Distance; Type; Sport_type")
    counter = 0
    distance_acc = 0
    for activity in strava_if.get_monthly_activities(month, year):
        if (com_or_tag and activity.commute) or (not com_or_tag and (tag_value in activity.name)):
            distance_acc = distance_acc + activity.distance.num / 1000.0
            counter = counter + 1
            print("""{0.id};{1.name};{1.start_date};{1.moving_time};{1.elapsed_time};{2};{1.type};{1.sport_type}""".format(athlete, activity, activity.distance.num / 1000.0))

    print('\nTotal: {} activities, {} km.'.format(counter, distance_acc))

    # client.close()

    exit(0)
