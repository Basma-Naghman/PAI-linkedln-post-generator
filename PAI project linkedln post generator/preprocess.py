import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

def process_post(raw_file_path,processed_file_path="data/processed_posts.json"):
    enriched_posts = []
    with open(raw_file_path,encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata 
            enriched_posts.append(post_with_metadata)
            

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags[tag] for tag in current_tags}
        post['tags'] = list(new_tags)

    with open(processed_file_path,encoding='utf-8',mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4)        

def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])

    unique_tags_list = ', '.join(unique_tags)  

    template = '''
    I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list.
       Example 1: "Jobseeker" , "Job Hunting can be all merged into a single tags "Job Search".
       Example 2: "Scam Alert" , "Job Scam" etc can be mapped to "Scams"
       Example 3: "Motivation" , "Inspiration" ,"Drive"  can be mapped as "Motivation"
    2. Each tag should be follow title case convection. example "Motivetion" , "Scams"
    3. Output should be JSON object, no preamble
    4. Output should have mapping of original tags and unified tags.
      For example {{"Jobseeker" : "Job Search" , "Scam Alert" : "Scams" , "Motivation" : "Motivation"}}
    Here is the list of tags:
    {tags}        
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'tags': str(unique_tags_list)})
    
    try : 
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)

    except OutputParserException:
        raise OutputParserException("Content too big. Unable to parse jobsb.")     
    return res


def extract_metadata(post):
    template = '''
    You are given a linkedln post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON .No preamble.
    2. JSON object should have exactly three keys: line_count , language , tags.
    3. tags is an array of text tags . Extract maximum two tags.
    4. Language  should be English or Hinglish (Hinglish mean hindi + english)

    Here is the actual post on which you need to perforn this tasl:
    {post} 
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'post' : post})

   
    try : 
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)

    except OutputParserException:
        raise OutputParserException("Content too big. Unable to parse jobsb.")     
    return res



    

if __name__ == "__main__":
    process_post("data/raw_posts.json","data/processed_posts.json")