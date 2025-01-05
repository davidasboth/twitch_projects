from __future__ import annotations

from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class AddressObject:
    uprn: str
    address: str

    @staticmethod
    def from_address(address_dict: dict) -> AddressObject:
        """
        Convert a "raw" address dictionary to an AddressObject type
        """
        return AddressObject(uprn=address_dict["uprn"], address=address_dict["label"])


class BinDayFetcher:
    def __init__(self, postcode_lookup_url: str):
        self.postcode_lookup_url = postcode_lookup_url

    def get_addresses(self, postcode: str) -> list[AddressObject]:
        """
        Get a list of addresses at a given postcode
        """
        postcode_lookup_response = requests.post(
            self.postcode_lookup_url, data={"postcode": postcode.strip()}
        )
        postcode_lookup_response.raise_for_status()

        addresses = postcode_lookup_response.json()

        return [AddressObject.from_address(address) for address in addresses]

    def get_bin_day_by_address(self, address: AddressObject) -> str:
        """
        Return the bin day for a specific address (provided as an AddressObject type)
        """
        bin_search_url = f"https://www.cherwell.gov.uk/homepage/129/bin-collection-search?uprn={address.uprn}&address={address.address}"

        bin_response = requests.get(bin_search_url)
        bin_response.raise_for_status()

        bin_soup = BeautifulSoup(bin_response.text, "html.parser")
        day_tags = bin_soup.select(".bin-collection-results__collection-day strong")

        if len(day_tags) == 0:
            print(f"No bin day found for {address}")
            return None

        bin_day = day_tags[0].text

        return bin_day

    def get_bin_day_by_postcode(self, postcode: str) -> str:
        """
        In goes a postcode, out comes the bin day.

        Combines methods to get addresses by postcode and method to get bin day for a single address.
        """
        addresses = self.get_addresses(postcode)

        # catch no addresses returned
        if len(addresses) == 0:
            return None

        bin_day = self.get_bin_day_by_address(addresses[0])
        return bin_day
