#

import strava_if

if __name__ == "__main__":
    if strava_if.authenticate_to_strava() < 0:
        print("ERROR: Failed to authenticate to Strava. Exit.")
        exit(-1)

    athlete = strava_if.get_athlete()

    # TODO: Change to CMDLINE parameters
    month = 8
    year = 2023

    print("Athlete's name is {} {}, based in {}, {}".format(athlete.firstname, athlete.lastname, athlete.city,
                                                            athlete.country))

    print("Commute monthly report\n")
    print("List of commute activities of athlete {} in month {y:04d}-{m:02d}.\n".format(
        athlete.firstname + " " + athlete.lastname, y=year, m=month))

    print("Activity_name; Activity_date; Moving_time; Elapsed_time; Distance; Type; Sport_type")
    counter = 0
    distance_acc = 0
    for activity in strava_if.get_monthly_activities(month, year):
        if activity.commute:
            distance_acc = distance_acc + activity.distance.num / 1000.0
            counter = counter + 1
            print(
                "{0.name};{0.start_date};{0.moving_time};{0.elapsed_time};{1};{0.type};{0.sport_type}".format(activity,
                                                                                                              activity.distance.num / 1000.0))

    print('\nTotal: {} activities, {} km.'.format(counter, distance_acc))

    # client.close()

    exit(0)
