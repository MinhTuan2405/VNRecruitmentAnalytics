import time
import requests as rq
from bs4 import BeautifulSoup
import csv
from datetime import datetime

header = ['job_id', 'title', 'income', 'location', 'experience', 
          'deadline', 'tags', 'job_description', 'candidate_requirements', 
          'income_details', 'benefits', 'work_location', 'work_time',
          'logo_url', 'company_name', 'company_size', 'company_industries', 'company_location',
          'job_level', 'candidate_education', 'quantity',
          'last_mod']
job_id = 1
last_mod = datetime.now ()
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


# job decriptions
jd = soup.find ('div', class_ = 'job-description')
jd_items = jd.find_all ('div', class_ = 'job-description__item')
job_description, candidate_requirements, income_details, benefits, work_location, work_time = None, None, None, None, None, None

#########           job_description
job_desc_div = jd_items[0].find('div', class_='job-description__item--content')
job_description = job_desc_div.get_text(separator="\n", strip=True) if job_desc_div else None

#########           candidate_requirements
req_div = jd_items[1].find('div', class_='job-description__item--content')
if req_div:
    requirements = [li.get_text(strip=True) for li in req_div.find_all("li")]
    candidate_requirements = ''
    for r in requirements:
        candidate_requirements += (r + '\n')

#########           income_details
income_div = jd_items[2].find("div", class_="job-description__item--content")

if income_div:
    income_details = ''
    details = [li.get_text(strip=True) for li in income_div.find_all("li")]
    for d in details:
        income_details += (d + '\n')

#########           benefits
benefits_div = jd_items[3].find("div", class_="job-description__item--content")
if benefits_div:
    benes = [li.get_text(strip=True) for li in benefits_div.find_all("li")]
    benefits = ''
    for b in benes:
        benefits += (b + '\n')

#########           work_location
location_div = jd_items[4].find("div", class_="job-description__item--content")
if location_div:
    locations = [div.get_text(strip=True) for div in location_div.find_all("div")]
    work_location = ''
    for l in locations:
        work_location += (l.replace ('- ', '') + '\n')


#########           work_time
work_time_div = jd_items[5].find("div", class_="job-description__item--content")
if work_time_div:
    work_time = work_time_div.get_text(strip=True)


# about company
logo_url, company_name, company_size, company_industries, company_location = None, None, None, None, None
# ================= ABOUT COMPANY =================
company_info = soup.find("div", class_="job-detail__company--information")

# logo
logo_tag = company_info.find("a", class_="company-logo") if company_info else None
if logo_tag and logo_tag.img:
    logo_url = logo_tag.img["src"]

# company_name
name_tag = company_info.find("a", class_="name") if company_info else None
if name_tag:
    company_name = name_tag.get_text(strip=True)

# company_size
size_tag = company_info.find("div", class_="job-detail__company--information-item company-scale") if company_info else None
if size_tag:
    value = size_tag.find("div", class_="company-value")
    company_size = value.get_text(strip=True) if value else None

# company_industries
industry_tag = company_info.find("div", class_="job-detail__company--information-item company-field") if company_info else None
if industry_tag:
    value = industry_tag.find("div", class_="company-value")
    company_industries = value.get_text(strip=True) if value else None

# company_location
location_tag = company_info.find("div", class_="job-detail__company--information-item company-address") if company_info else None
if location_tag:
    value = location_tag.find("div", class_="company-value")
    company_location = value.get_text(strip=True) if value else None


# about candidate and job
job_level, candidate_education, quantity = None, None, None

general_info_blocks = soup.find_all("div", class_="box-general-group")
for block in general_info_blocks:
    title_tag = block.find(class_="box-general-group-info-title")
    value_tag = block.find(class_="box-general-group-info-value")
    if not title_tag or not value_tag:
        continue

    label = title_tag.get_text(strip=True)
    text_value = value_tag.get_text(strip=True)

    if "Cấp bậc" in label:
        job_level = text_value
    elif "Học vấn" in label:
        candidate_education = text_value
    elif "Số lượng tuyển" in label: 
        quantity = text_value



print("Job id:", job_id)
print("Title:", title_text)
print("Income:", income_text)
print("Location:", location_text)
print("Experience:", exp_text)
print("Deadline:", deadline_text)
print("All tags:", tag_list)
print("job_description:", job_description)
print("candidate_requirements:", candidate_requirements)
print("income_details:", income_details)
print("benefits:", benefits)
print("work_location:", work_location)
print("work_time:", work_time)
print("last_mod:", last_mod)
print("logo_url:", logo_url)
print("company_name:", company_name)
print("company_size:", company_size)
print("company_industries:", company_industries)
print("company_location:", company_location)
print("job_level:", job_level)
print("candidate_education:", candidate_education)
print("quantity:", quantity)

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
        "tags": tag_list,
        "job_description": job_description,
        "candidate_requirements": candidate_requirements,
        "income_details": income_details,
        "benefits": benefits,
        "work_location": work_location,
        "work_time": work_time,
        "logo_url": logo_url,
        "company_name": company_name,
        "company_size": company_size,
        "company_industries": company_industries,
        "company_location": company_location,
        "job_level": job_level,
        "candidate_education": candidate_education,
        "quantity": quantity,
        "last_mod": last_mod
    })