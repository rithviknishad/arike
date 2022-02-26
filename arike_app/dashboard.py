from dataclasses import dataclass
from typing import List, Optional


@dataclass
class __DashboardTab:
    name: str
    url: str
    selected: bool


DASHBOARD_PAGES: List[__DashboardTab] = []


def register_dashboard_tab(name: str, url: str):
    DASHBOARD_PAGES.append(__DashboardTab(name, url, False))


class MyTabs:
    Home = "Home", "/home"
    Users = "Users", "/users"


for tab in [x for x in dir(MyTabs) if not x.startswith("__")]:
    register_dashboard_tab(*getattr(MyTabs, tab))
