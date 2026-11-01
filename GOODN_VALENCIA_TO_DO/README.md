# Valencia — Last Location Display

This app is intentionally simple:

- It connects to the database
- Reads the most recent valid GPS packet
- Pulls the last known latitude/longitude
- Returns it as JSON from `/api/location`
- The page loads the result and displays it on screen

This is not a full map app by itself. It is just the backend/data layer that fetches the latest location and exposes it for a frontend view to wrap around.

## What it does

The key logic is in `app.py`:

- Query: `SELECT ... FROM tracker_packets ... ORDER BY received_at DESC ... LIMIT 1`
- It looks for the newest valid `latitude` and `longitude`
- If there is no GPS data, it returns:
  - `success: false`
  - `message: "No GPS location available"`
- If there is data, it returns:
  - `success: true`
  - `location: { ... }`

So the app is basically:

`last saved location -> API -> screen`

That is all.

## How Valencia should use it

Valencia, you do not need to rebuild the logic.

You just need to:

1. Keep this project running
2. Use the `/api/location` endpoint
3. Put that result inside your app view or map screen
4. Display the coordinates as the current bracelet location

Example idea:

- Use the API in a mobile app screen
- Get the latest coordinates
- Put them into a map view
- Show the last known location on the map

That is the whole job.

## API endpoint

Open this in the browser or call it from your frontend:

- `GET /api/location`

Example response:

```json
{
  "success": true,
  "location": {
    "imei": "123456789012345",
    "latitude": 10.123456,
    "longitude": -84.123456,
    "speed": 0,
    "battery": 92,
    "received_at": "2026-11-01T12:00:00"
  }
}
```

## Important note

This code does not build a full GPS UI itself.
It only reads the last location from the database and exposes it.

So for Valencia:

- do not overthink it
- do not add extra tracking logic
- just wrap this endpoint inside an app/map view and display the result

That is the final step.

## Run locally

From the folder:

```bash
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://localhost:5000/
```

The page loads the frontend, and the location data is fetched from the API.

## Final message

This is a last-location reader.

It is already doing the job:

- reads the newest saved bracelet location
- sends it to the frontend
- makes it easy to show on a screen or map

Valencia only needs to wrap it in the app view and she is done.
