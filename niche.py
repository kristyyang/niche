import requests
from bs4 import BeautifulSoup
import pyexcel
from addict import Dict
import json

def na(value):
  return value if value != {} else "N/A"

def extract_school(school):
  badge = school.badge
  content = school.content
  return {
    "ordinal": "N/A" if badge.ordinal == {} else badge.ordinal,
    "total": "N/A" if badge.total == {} else badge.total,
    "name": na(content.entity.name),
    "acceptance_rate": na(content.facts[0].value),
    "net_price": na(content.facts[1].value),
    "sat_range": na(content.facts[2].value)
  }

def get_page_count(list_url="best-colleges-for-finance-accounting"):
  url_format = "https://www.niche.com/api/renaissance/results/?sat=0-1600&listURL={1}&page={0}&searchType=college"
  r = requests.get(url_format.format(1, list_url))
  
  data = Dict(json.loads(r.text))

  return data.total // 25 + 1

def get_options():
  data = Dict(json.loads(open("options.json").read()))
  return data.options

# r = requests.get("https://www.niche.com/colleges/search/best-colleges-for-accounting/?sat=0-1600&page=1", cookies=cookies)
def one_page(page_no, list_url="best-colleges-for-finance-accounting"):
  url_format = "https://www.niche.com/api/renaissance/results/?sat=0-1600&listURL={1}&page={0}&searchType=college"
  r = requests.get(url_format.format(page_no, list_url))
  
  with open("niche_{1}_{0}.json".format(page_no, list_url), "w") as f:
    f.write(r.text)
  
  data = Dict(json.loads(r.text))
  schools = data.entities

  return [extract_school(school) for school in schools]

options = get_options()

for option in options:
  print("Option", option)
  page_count = get_page_count(option)
  print("Page count", page_count)
  school_list = []
  for page in range(1, page_count + 1):
    print("Page", page)
    school_list.extend(one_page(page, option))
  print("Saving")
  pyexcel.save_as(records=school_list, dest_file_name="{0}.xlsx".format(option))
  print("Done")

# school_list = []
# for i in range(1, 35):
#   school_list.extend(one_page(i))

# pyexcel.save_as(records=school_list, dest_file_name="best-colleges-for-finance-accounting.xlsx")

html_options = '''
<div>
  <option value="best-colleges">All</option>
  <option selected value="best-colleges-for-finance-accounting">Accounting/Finance</option>
  <option value="best-colleges-for-administrative-and-clerical">Administrative Work</option>
  <option value="best-colleges-for-agricultural-sciences">Agricultural Sciences</option>
  <option value="best-colleges-for-alternative-medicine">Alternative Medicine</option>
  <option value="best-colleges-for-anthropology-archaeology">Anthropology</option>
  <option value="best-colleges-for-architecture">Architecture</option>
  <option value="best-colleges-for-visual-arts">Art</option>
  <option value="best-colleges-for-arts-management">Arts Management</option>
  <option value="best-colleges-for-biology">Biology</option>
  <option value="best-colleges-for-building-and-construction">Building and Construction</option>
  <option value="best-colleges-for-business-management">Business</option>
  <option value="best-colleges-for-chemistry">Chemistry</option>
  <option value="best-colleges-for-communications-journalism">Communications</option>
  <option value="best-colleges-for-computer-science">Computer Science</option>
  <option value="best-colleges-for-cosmetology">Cosmetology</option>
  <option value="best-colleges-for-criminal-justice">Criminal Justice</option>
  <option value="best-colleges-for-culinary-arts-and-food-service">Culinary Arts</option>
  <option value="best-colleges-for-dental">Dental Studies</option>
  <option value="best-colleges-for-design">Design</option>
  <option value="best-colleges-for-economics">Economics</option>
  <option value="best-colleges-for-education">Education</option>
  <option value="best-colleges-for-engineering">Engineering</option>
  <option value="best-colleges-for-english">English</option>
  <option value="best-colleges-for-earth-and-environmental-sciences">Environmental Science</option>
  <option value="best-colleges-for-film-video-and-photography">Film/Photography</option>
  <option value="best-colleges-for-food-and-nutrition">Food and Nutrition</option>
  <option value="best-colleges-for-foreign-languages">Foreign Languages</option>
  <option value="best-colleges-for-general-studies">General Studies</option>
  <option value="best-colleges-for-health-professions">Health Professions</option>
  <option value="best-colleges-for-history">History</option>
  <option value="best-colleges-for-humanities">Humanities/Social Sciences</option>
  <option value="best-colleges-for-information-technology">Information Technology</option>
  <option value="best-colleges-for-international-relations">International Relations</option>
  <option value="best-colleges-for-rehabilitation-and-therapy">Kinesiology and Therapy</option>
  <option value="best-colleges-for-legal-studies">Legal Studies</option>
  <option value="best-colleges-for-mathematics">Math</option>
  <option value="best-colleges-for-mechanics-repair">Mechanics</option>
  <option value="best-colleges-for-medical-assistant-technician">Medical Technicians</option>
  <option value="best-colleges-for-music">Music</option>
  <option value="best-colleges-for-nursing">Nursing</option>
  <option value="best-colleges-for-performing-arts">Performing Arts/Theater</option>
  <option value="best-colleges-for-pharmacy">Pharmacy</option>
  <option value="best-colleges-for-philosophy">Philosophy</option>
  <option value="best-colleges-for-physics">Physics</option>
  <option value="best-colleges-for-political-science">Political Science</option>
  <option value="best-colleges-for-protective-services">Protective Services</option>
  <option value="best-colleges-for-psychology">Psychology</option>
  <option value="best-colleges-for-religious-studies-theology">Religious Studies</option>
  <option value="best-colleges-for-trades-and-personal-services">Trades and Personal Services</option>
  <option value="best-colleges-for-veterinary-studies">Veterinary Studies</option>
</div>
'''

# from bs4 import BeautifulSoup
# import json
# soup = BeautifulSoup(html_options, 'html.parser')
# with open("options.json", "w") as f:
#   data = { "options": [] }
#   for option in soup.find_all("option"):
#     data["options"].append(option["value"])
#   f.write(json.dumps(data))