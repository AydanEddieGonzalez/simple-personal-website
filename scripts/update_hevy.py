"""
pulls my workout stats from hevy and saves them to hevy.json for the website.

runs on github actions once a day (see .github/workflows/hevy.yml).
the api key comes from the HEVY_API_KEY secret, so it never ends up in the code.
"""

import json
import os
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

API = "https://api.hevyapp.com/v1"
KEY = os.environ["HEVY_API_KEY"]
TZ = ZoneInfo("America/Los_Angeles")
MAX_PAGES = 30  # 10 workouts per page, plenty for a year-long streak


def get(path):
    req = urllib.request.Request(f"{API}/{path}", headers={"api-key": KEY, "accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.load(res)


def parse(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(TZ)


def week_start(dt):
    # weeks start on monday
    return (dt - timedelta(days=dt.weekday())).date()


# grab recent workouts, newest first
workouts = []
for page in range(1, MAX_PAGES + 1):
    data = get(f"workouts?page={page}&pageSize=10")
    workouts += data.get("workouts", [])
    if page >= data.get("page_count", 1):
        break

total = get("workouts/count").get("workout_count", len(workouts))

now = datetime.now(TZ)
this_week = week_start(now)
weeks_trained = {week_start(parse(w["start_time"])) for w in workouts}

# streak = how many weeks in a row i've trained (this week doesn't break it if it just started)
streak = 0
week = this_week if this_week in weeks_trained else this_week - timedelta(weeks=1)
while week in weeks_trained:
    streak += 1
    week -= timedelta(weeks=1)

recent = []
for w in workouts[:3]:
    start, end = parse(w["start_time"]), parse(w["end_time"])
    recent.append({
        "title": w.get("title") or "workout",
        "exercises": len(w.get("exercises", [])),
        "minutes": round((end - start).total_seconds() / 60),
        "date": w["start_time"],
    })

out = {
    "updated": now.isoformat(),
    "workout_count": total,
    "this_week": sum(1 for w in workouts if week_start(parse(w["start_time"])) == this_week),
    "streak_weeks": streak,
    "recent": recent,
}

with open("hevy.json", "w") as f:
    json.dump(out, f, indent=2)

print(f"saved: {total} workouts, {out['this_week']} this week, {streak} wk streak")
