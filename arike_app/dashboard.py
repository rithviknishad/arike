from dataclasses import dataclass


@dataclass
class DashboardTab:
    name: str
    url: str


DASHBOARD_PAGES = [
    DashboardTab(*tab_details)
    for tab_details in [
        ("Home", "/home"),
        ("Users", "/users"),
        ("Facility", "/facilities"),
        ("Patients", "/patients"),
        ("LSG Body", "/lsg-bodies"),
        ("Ward", "/wards"),
        ("Profile", "/profile"),
    ]
]
