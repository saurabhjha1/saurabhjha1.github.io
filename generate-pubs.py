#!/usr/bin/env python3
import json
from datetime import datetime

url_template='\
<a href="{url}" class="pub-link" target="_blank">{tag}</a>\
'

media_coverage_template='\
<a href="{url}" class="pub-media" target="_blank">{tag}</a>\
'

conference_template='\
\t<td class="pub-left">\n\
    \t\t{venue}\n\
\t</td>\n\
\t<td class="pub-right" id={td_class}>\n\
    \t\t<span class="pub-title">{title}</span></br>\n\
    \t\t{authors}</br>\n\
    \t\t{publication}</br>\n\
    \t\t{materials}\
    \t\t{awards}\
    \t\t{media_coverage}\
\t</td>\
'

def get_dt(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()

def generate_conference(ofh, pubs):
    # generate header
    ofh.write('<table id="pub"><tbody>\n')
    conf_html = ""
    pubs = sorted(pubs, key=lambda item: get_dt(item["date"]), reverse=True)
    for pub in pubs:
        conf_html +="<tr id={}>"
        pub_materials = ""
        for tag in pub["urls"]:
            if pub["urls"][tag] != "":
                pub_materials+=url_template.format(url = pub["urls"][tag], tag=tag)
        media_coverage=""
        if "media_coverage" in pub:
            for tag in pub["media_coverage"]:
                media_coverage+=media_coverage_template.format(url = pub["media_coverage"][tag], tag=tag)

        awards=""
        if "awards" in pub:
            for award in pub["awards"]:
                awards += '<span class="awards">'
                awards += award
                awards += "</span>"
        conf_html += conference_template.format(
            venue=pub["venue"], 
            title=pub["title"], 
            authors=", ".join(pub["authors"]).replace("Saurabh Jha", "<u>Saurabh Jha</u>"),
            publication=pub["publication"],
            materials=pub_materials,
            awards=awards, 
            media_coverage=media_coverage, 
            td_class=pub["pub_type"]
            )
        conf_html += "</tr>\n"
    ofh.write(conf_html)
    ofh.write("</tbody></table></br>\n")
    # ofh.write("</div>")

def generate_html():
    ofh = open("publications.md", 'w')
    # write the header of the file
    ofh.write("\
---\n\
title: Publications\n\
layout: publication\n\
---\n")
    
    pubs = json.load(open("pub.json"))
    
    generate_conference(ofh, pubs["all_pubs"])
    
    ofh.close()

if __name__ == "__main__":
    generate_html()
    