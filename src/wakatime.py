from typing import TypedDict, List, Optional
import requests

class WakaTimeProject(TypedDict):
    key: str
    total: int

class WakaTimeCategory(TypedDict):
    key: str
    total: int

class WakaTimeStats(TypedDict):
    user_id: str
    from_: str  # Note: using from_ since 'from' is a Python keyword
    to: str
    projects: List[WakaTimeProject]
    languages: List[WakaTimeCategory]
    editors: List[WakaTimeCategory]
    operating_systems: List[WakaTimeCategory]
    machines: List[WakaTimeCategory]
    labels: List[WakaTimeCategory]
    branches: Optional[List[WakaTimeCategory]]
    entities: Optional[List[WakaTimeCategory]]
    categories: List[WakaTimeCategory]
    total_sum: int  # Added by your function

def get_wakatime_stats(num_days: int = 7) -> List[WakaTimeStats]:
    from datetime import datetime, timedelta
    today = datetime.today()
    data = []
    for i in range(1, num_days+1):
        from_date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        to_date = (today - timedelta(days=i-1)).strftime('%Y-%m-%d')
        response = requests.get(
            "https://waka.hackclub.com/api/summary",
            params={"user": "U062UG485EE", "from": from_date, "to": to_date},
            headers={"Authorization": "Bearer 2ce9e698-8a16-46f0-b49a-ac121bcfd608"}
        )
        day_data = response.json()
        day_data["total_sum"] = sum([project["total"] for project in day_data["categories"]])
        data.append(day_data)
    return data
