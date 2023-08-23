# This is a sample Python script.

import calendar
import pickle
import time

from stravalib.client import Client


# Operate on several files
# SUCCESS: Returns None
# FAIL: Raises exception
def authenticate_to_strava():
    global STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, client

    client = Client()

    try:
        STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET = open("client_secret.app").read().strip().split(",")
        print("Client ID {} and secret read from file".format(STRAVA_CLIENT_ID))
    except IOError:
        print("Strava.com Client ID & Secret file (client_secret.app) not found. Input the values to initialize your app instance.")
        STRAVA_CLIENT_ID = input("Input STRAVA_CLIENT_ID and press Enter:")
        STRAVA_CLIENT_SECRET = input("Input STRAVA_CLIENT_SECRET and press Enter:")

        try:
            with open("client_secret.app", "w") as f:
                f.write("{},{}".format(STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET))

        except IOError:
            print("ERROR: authenticate_to_strava: IOError exception while opening/storing client_secret.app file");
            return -1

    try:
        with open("access_tokens.app", "rb") as f:
            access_tokens = pickle.load(f)
        f.close()
    except IOError:
        print("WARNING: access_tokens not found - generating new ones")
        print("Copy the following URI to your web browser and confirm application access to your Strava profile:\n")

        url = client.authorization_url(client_id=STRAVA_CLIENT_ID,
                                       redirect_uri="http://127.0.0.1:9999/authorization",
                                       scope=["read_all", "profile:read_all", "activity:read_all"])
        print(url)

        print(
            "\nInput the value of the parameter 'code' from URL in the address line of your browser (code=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx).\n")

        try:
            CODE = input("Input CODE and press Enter:")

            access_tokens = client.exchange_code_for_token(client_id=STRAVA_CLIENT_ID,
                                                           client_secret=STRAVA_CLIENT_SECRET, code=CODE)
            with open("access_tokens.app", "wb") as f:
                pickle.dump(access_tokens, f)
            f.close()

        except IOError:
            print("ERROR: authenticate_to_strava: Can't store access token on local file system. (IOError)");
            return -2

    print("INFO: Latest access tokens read from file: {}".format(access_tokens))

    if time.time() > access_tokens["expires_at"]:
        print("INFO: Tokens has expired, will refresh")
        refresh_response = client.refresh_access_token(client_id=STRAVA_CLIENT_ID,
                                                       client_secret=STRAVA_CLIENT_SECRET,
                                                       refresh_token=access_tokens["refresh_token"])
        access_tokens = refresh_response
        with open("access_tokens.app", "wb") as f:
            pickle.dump(refresh_response, f)
        f.close()

        print("INFO: Refreshed tokens saved to file")

        client.access_token = refresh_response["access_token"]
        client.refresh_token = refresh_response["refresh_token"]
        client.token_expires_at = refresh_response["expires_at"]

    else:
        print("INFO: Token still valid, expires at {}".format(
            time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(access_tokens["expires_at"]))))

        client.access_token = access_tokens["access_token"]
        client.refresh_token = access_tokens["refresh_token"]
        client.token_expires_at = access_tokens["expires_at"]

    return 0


def get_athlete():
    return client.get_athlete()


def get_monthly_activities(month, year):
    date_after = "{y:04d}-{m:02d}-{d:02d}{trail}".format(y=year, m=month, d=1, trail="T00:00:00Z")
    date_before = "{y:04d}-{m:02d}-{d:02d}{trail}".format(y=year, m=month, d=calendar.monthrange(year, month)[1],
                                                          trail="T23:59:59Z")

    #    print(date_after)
    #    print(date_before)

    return client.get_activities(after=date_after, before=date_before, limit=1000)


if __name__ == "__main__":
    print("ERROR: Library only. Exit.")
    exit(-1)
