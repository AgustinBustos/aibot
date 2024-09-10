
from keys import openai_key
from pydantic import BaseModel
from openai import OpenAI
 
def get_job_links(html):
    client = OpenAI(api_key=openai_key)
    class JobDescriptions(BaseModel):
        jobs_name: str
        jobs_link: str


    class ListOfLinks(BaseModel):
        jobs_list: list[JobDescriptions]

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "Extract a list of url links and names of job postings where the job is related to Data Science, economics, statistics or econometrics. At minimum extract 6 urls."},
            {"role": "user", "content": html},
        ],
        response_format=ListOfLinks,
    )

    result = completion.choices[0].message.parsed.jobs_list
    return result

# print(get_job_links(html))
# print(len(jobers))