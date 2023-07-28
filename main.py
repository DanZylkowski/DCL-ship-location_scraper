import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

if __name__ == "__main__":
    print("Hello World")


    def get_gps_coords():
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/75.0.3770.80 Safari/537.36"
            }

        fantasy_url = "https://www.cruisemapper.com/ships/Disney-Fantasy-649"
        wish_url = "https://www.cruisemapper.com/ships/Disney-Wish-2127"
        dream_url = "https://www.cruisemapper.com/ships/Disney-Dream-548"
        wonder_url = "https://www.cruisemapper.com/ships/Disney-Wonder-692"
        magic_url = "https://www.cruisemapper.com/ships/Disney-Magic-684"

        url_list = [fantasy_url, wish_url, dream_url, wonder_url, magic_url]
        ship_list = ["Fantasy", "Wish", "Dream", "Wonder", "Magic"]
        current_coords_list = []
        for ship, url in zip(ship_list, url_list):
            page = requests.get(url, headers=headers)

            soup = BeautifulSoup(page.content, "html.parser")

            coordinates_text = soup.find("div",
                                         class_="col-md-4 currentItineraryInfo"
                                         )

            longitude_start = (
                    coordinates_text.text.find("coordinates") + len(
                "coordinates"
                ) + 1
            )
            longitude_end = longitude_start + 8
            lattitude_start = coordinates_text.text.find("/") + len("/") + 1
            lattitude_end = lattitude_start + 8

            longitude_coords = coordinates_text.text[
                               longitude_start:longitude_end].strip()
            lattitude_coords = coordinates_text.text[
                               lattitude_start:lattitude_end].strip()

            en_route_to_start = (
                    coordinates_text.text.find("en route to") + len(
                "en route to"
                ) + 1
            )
            en_route_to_finish = coordinates_text.text.find("The AIS") - 2
            en_route_to = coordinates_text.text[
                          en_route_to_start:en_route_to_finish]

            coordinates_description_start = coordinates_text.text.find(
                "cruising"
                )
            coordinates_description_finish = en_route_to_finish
            coordinates_description = coordinates_text.text[
                                      coordinates_description_start:coordinates_description_finish
                                      ]

            current_coords_list.append(
                [
                    ship,
                    longitude_coords,
                    lattitude_coords,
                    en_route_to,
                    datetime.now(),
                    coordinates_description,
                    ]
                )
        print(current_coords_list)
        df = pd.DataFrame(
            current_coords_list,
            columns=[
                "Ship_name",
                "latitude",
                "longitude",
                "next_port",
                "datetime",
                "coordinates_description",
                ],
            )
        df.to_csv("DCL cruise ship gps coords.csv", mode="a", index=False,
                  header=False
                  )
        # df.to_csv("DCL cruise ship gps coords.csv", index=False)
        print("New gps coordinates retrieved and saved at {}".format(
            datetime.now()
            )
              )
        return df

    get_gps_coords()

