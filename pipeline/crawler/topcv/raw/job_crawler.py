import requests as rq
from bs4 import BeautifulSoup
import csv


header = ['job_id', 'title', 'income', 'location', 'experience', 'deadline', 'tags']
job_id = 1
url = 'https://www.topcv.vn/viec-lam/truong-phong-kinh-doanh-xe-o-to-vinfast/1802279.html'
raw_html = rq.get(url)

soup = BeautifulSoup(raw_html.text, 'html.parser')

# title
job_detail_body = soup.find('div', class_='job-detail__body')
title_tag = job_detail_body.find("h1", class_="job-detail__info--title")
title_text = title_tag.get_text(strip=True) if title_tag else None

# info blocks
income_text, location_text, exp_text, deadline_text = None, None, None, None
info_sections = soup.find_all('div', class_='job-detail__info--section-content')

for sec in info_sections:
    sec_title = sec.find('div', class_='job-detail__info--section-content-title')
    sec_value = sec.find('div', class_='job-detail__info--section-content-value')
    if not sec_title or not sec_value:
        continue

    label = sec_title.get_text(strip=True).lower()
    value = sec_value.get_text(strip=True)

    if "thu nhập" in label or "mức lương" in label:
        income_text = value
    elif "địa điểm" in label:
        location_text = value
    elif "kinh nghiệm" in label:
        exp_text = value

# deadline
deadline_div = soup.find('div', class_='job-detail__info--deadline')
if deadline_div:
    deadline_text = deadline_div.get_text(strip=True).replace("Hạn nộp hồ sơ:", "").strip()


# job tags
tags = soup.find ('div', class_ = 'job-tags')
all_tags = tags.find_all ('a')
tag_list = ''
for tag in all_tags:
    value = tag.get_text (strip=True)
    tag_list += (value + ', ')
    


print("Job id:", job_id)
print("Title:", title_text)
print("Income:", income_text)
print("Location:", location_text)
print("Experience:", exp_text)
print("Deadline:", deadline_text)
print("All tags:", tag_list)

# save to CSV
with open('data.csv', 'w', encoding='utf-8-sig', newline="") as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerow({
        "job_id": job_id,
        "title": title_text,
        "income": income_text,
        "location": location_text,
        "experience": exp_text,
        "deadline": deadline_text,
        "tags": tag_list
    })
