from dataclasses import dataclass


@dataclass
class DashboardTab:
    name: str
    url: str


DASHBOARD_PAGES = [
    DashboardTab(*tab_details)
    for tab_details in [
        ("Home", "/home/"),
        ("Patients", "/patients/"),
        ("Schedule", "/schedule/"),
        ("Users", "/users/"),
        ("Facilities", "/facilities/"),
        ("LSG Bodies", "/lsg-bodies/"),
        ("Wards", "/wards/"),
        ("Profile", "/profile/"),
    ]
]
