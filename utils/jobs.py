import requests

API_KEY = "YOUR_RAPIDAPI_KEY"

def get_jobs(skills):

    query = " ".join(skills[:2])  # use first 2 skills as job keyword

    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {
        "query": query,
        "page": "1",
        "num_pages": "1"
    }

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    jobs = []

    if response.status_code == 200:

        data = response.json()

        for job in data["data"][:5]:

            title = job["job_title"]
            company = job["employer_name"]
            city = job["job_city"]

            jobs.append(f"{title} – {company} – {city}")

    return jobs