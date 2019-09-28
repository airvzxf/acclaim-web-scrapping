#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Main script for get data for salaries.

References:
    https://docs.python.org/3/library/multiprocessing.html
    https://medium.com/@urban_institute/using-multiprocessing-to-make-python-code-faster-23ea5ef996ba
    https://www.ellicium.com/python-multiprocessing-pool-process/
"""
# from _csv import writer
# from functools import partial
# from math import ceil
# from multiprocessing import Manager
# from multiprocessing.pool import Pool
# from re import findall
# from time import time
#
# from requests import get
# from urllib3 import disable_warnings
# from urllib3.exceptions import InsecureRequestWarning
#
#
# def get_response_from_url(url):
#     disable_warnings(InsecureRequestWarning)
#     response = get(url, verify=False)
#     return response
#
#
# def generate_badges_from_url(url, company, badges):
#     disable_warnings(InsecureRequestWarning)
#
#     regex = r'c-grid-item c-grid-item--stack-lt-sm cr-public-organization-badge-template-grid-item.* ' + \
#             'href="/org/{company}/badge/([a-zA-Z0-9-.]+)"'.format(company=company)
#     response = get(url, verify=False)
#     extraction = findall(regex, response.text)
#     badges += extraction
#
#
# def generate_jobs_from_url(url, badge, country, company, row_headers, jobs):
#     disable_warnings(InsecureRequestWarning)
#
#     response = get(url, verify=False)
#     jobs += get_jobs(response, badge, country, company, row_headers)
#
#
# def get_jobs(response, badge, country, company, row_headers):
#     if response.json() is None or response.json()['data'] is None:
#         return []
#
#     jobs = []
#     jobs_data = response.json()['data']
#
#     for job in jobs_data:
#         row_job = []
#
#         for header in row_headers:
#             if header == 'badge':
#                 row_job.append(badge)
#                 continue
#
#             if header == 'country':
#                 row_job.append(country)
#                 continue
#
#             if header == 'company':
#                 row_job.append(company)
#                 continue
#
#             if header in job.keys():
#                 row_job.append(job[header])
#
#         jobs.append(row_job)
#
#     return jobs
#
#
# def store_data(rows, company, country, rewrite=False):
#     mode = 'a' if rewrite else 'w'
#     file_name = 'data_processing_{company}_{country}.csv'.format(company=company, country=country)
#
#     with open(file_name, mode, encoding='utf-8', newline='') as file:
#         csv = writer(file)
#         csv.writerows(rows)
#
#
# def main() -> None:
#     """
#     Start the python script for get the data for salaries.
#     :rtype: None
#     """
#     # ------------------------------------------------
#     # Constants.
#     # ------------------------------------------------
#     # Max Multi-processing request by every Pool
#     # max_requests = 15
#     max_requests = 40
#
#     # ibm, oracle
#     # companies = ['ibm', ]
#     # companies = ['oracle', ]
#     companies = ['ibm', 'oracle', ]
#
#     # 'AU', 'BR', 'CA', 'FR', 'DE', 'IN', 'GB', 'US'
#     # countries = ['US', ]
#     # countries = ['AU', 'FR', 'US', ]
#     countries = ['AU', 'BR', 'CA', 'FR', 'DE', 'GB', 'US', ]
#
#     # 1, 2, 3, 4, 5
#     # salary_ranges = [5, ]
#     salary_ranges = [1, 2, 3, 4, 5, ]
#
#     # Enter some badge.
#     badges = ['enterprise-design-thinking-practitioner']
#     # badges = ['ibm-champion-analytics-3-year-milestone']
#
#     # If it's true then scrape the badges pages.
#     # If it's false then take the above badges list.
#     needs_request_badges = True
#     # needs_request_badges = False
#
#     # None: Scrape all the badges pages.
#     # 1: Scrape only the first page.
#     # 2: Scrape only the first and the second page.
#     max_badges_pages = None
#     # max_badges_pages = 1
#
#     row_headers = [
#         'id', 'salary', 'badge', 'title', 'company', 'employer',
#         'country', 'city', 'state', 'job_type',
#         'posting_date', 'application_url'
#     ]
#
#     badges_per_page = 48
#     url_badges_base = 'https://www.youracclaim.com/organizations/{company}/badges?page={page_number}'
#
#     jobs_per_page = 12
#     url_jobs_base = 'https://www.youracclaim.com/api/v1/jobs/{company}/{badge}?' \
#                     'country={country}&' + \
#                     'salary_ranges[id]={salary_ranges}&' + \
#                     'salary_ranges[name]=&' + \
#                     'page={page_number}&'
#
#     # ------------------------------------------------
#     # Init the Scraping for Jobs.
#     # ------------------------------------------------
#     for company in companies:
#
#         # ------------------------------------------------
#         # Check if the badges were requested.
#         # ------------------------------------------------
#         if needs_request_badges:
#             regex = r'(\d+) badges'
#             url = url_badges_base.format(company=company, page_number=1)
#             html_body = get_response_from_url(url).text
#             extraction = findall(regex, html_body)
#
#             # ------------------------------------------------
#             # Check if it returns the badges.
#             # ------------------------------------------------
#             if extraction and len(extraction) > 0:
#                 total_badges = int(extraction[0])
#                 total_pages = max_badges_pages
#                 if max_badges_pages is None:
#                     total_pages = ceil(total_badges / badges_per_page)
#
#                 print('# -------------------------------------------')
#                 print('# Get badges.')
#                 print('# Badges per page:', badges_per_page)
#                 print('# Total pages:    ', total_pages)
#                 print('# Total badges:   ', total_badges)
#
#                 if total_badges == 0:
#                     print('# -------------------------------------------')
#                     continue
#
#                 # ------------------------------------------------
#                 # Init the Multi-process Scraping for badges.
#                 # ------------------------------------------------
#                 init_time = time()
#                 with Manager() as manager:
#                     badges_multiprocess = manager.list()
#                     urls = [
#                         url_badges_base.format(company=company, page_number=page_number)
#                         for page_number in range(1, total_pages + 1)
#                     ]
#                     # ------------------------------------------------
#                     # Request the badges handling with the Pool.
#                     # ------------------------------------------------
#                     pool = Pool(max_requests)
#                     pool.map(
#                         partial(
#                             generate_badges_from_url,
#                             company=company,
#                             badges=badges_multiprocess,
#                         ),
#                         urls
#                     )
#                     pool.close()
#                     badges = list(badges_multiprocess)
#                     difference = int(time() - init_time)
#
#                     print('# Badges obtained:', len(badges_multiprocess))
#                     print('# Execution time: ', difference)
#                     print('# -------------------------------------------')
#
#         if not badges:
#             continue
#
#         for country in countries:
#             # ------------------------------------------------
#             # Create the CSV file with the headers.
#             # ------------------------------------------------
#             store_data([row_headers], company, country)
#
#             for badge in badges:
#                 for salary_range in salary_ranges:
#                     # ------------------------------------------------
#                     # Get the number of pages and jobs from API.
#                     # ------------------------------------------------
#                     url = url_jobs_base.format(
#                         page_number=1,
#                         company=company,
#                         badge=badge,
#                         country=country,
#                         salary_ranges=salary_range,
#                     )
#                     response = get_response_from_url(url)
#
#                     if response.json()['metadata'] is None:
#                         continue
#
#                     total_jobs = response.json()['metadata']['total_count']
#                     total_pages = response.json()['metadata']['total_pages']
#                     print('# -------------------------------------------')
#                     print('# Company:       ', company)
#                     print('# Badge:         ', badge)
#                     print('# Country:       ', country)
#                     print('# Salary:        ', salary_range)
#                     print('# Url:           ', url)
#                     print('# Jobs per page: ', jobs_per_page)
#                     print('# Total pages:   ', total_pages)
#                     print('# Total jobs:    ', total_jobs)
#
#                     if total_jobs == 0:
#                         print('# -------------------------------------------')
#                         continue
#
#                     # ------------------------------------------------
#                     # Init the Multi-process.
#                     # ------------------------------------------------
#                     init_time = time()
#                     with Manager() as manager:
#                         jobs_multiprocess = manager.list()
#                         urls = [
#                             url_jobs_base.format(
#                                 page_number=page_number,
#                                 company=company,
#                                 badge=badge,
#                                 country=country,
#                                 salary_ranges=salary_range,
#                             )
#                             for page_number in range(1, total_pages + 1)
#                         ]
#                         # ------------------------------------------------
#                         # Request the jobs handling with the Pool.
#                         # ------------------------------------------------
#                         pool = Pool(max_requests)
#                         pool.map(
#                             partial(
#                                 generate_jobs_from_url,
#                                 badge=badge,
#                                 country=country,
#                                 company=company,
#                                 row_headers=row_headers,
#                                 jobs=jobs_multiprocess,
#                             ),
#                             urls
#                         )
#                         pool.close()
#                         difference = int(time() - init_time)
#
#                         print('# Jobs:          ', len(jobs_multiprocess))
#                         print('# Execution time:', difference)
#                         print('# -------------------------------------------')
#
#                         # ------------------------------------------------
#                         # Store all the jobs in teh CSV file.
#                         # ------------------------------------------------
#                         store_data(jobs_multiprocess, company, country, rewrite=True)
#
#
# if __name__ == "__main__":
#     main()
