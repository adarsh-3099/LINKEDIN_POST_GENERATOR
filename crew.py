from crewai import Crew,Process
from tasks import PostTasks
from agents import PostAgents
from printGen import print_agent_output
import gradio as gr
import textstat
    

user_input = input()

## Agents and Tasks 
agents = PostAgents()
tasks = PostTasks()

## Agents
researcher_agent = agents.make_researcher_agent()
posts_writer_agent = agents.make_posts_writer_agent()
customer_feedback_agent = agents.make_customer_feedback_agent()

## Tasks
research_info_for_post = tasks.research_info_for_post(researcher_agent, user_input)
draft_post= tasks.draft_post(posts_writer_agent, user_input, research_info_for_post)
feedback_on_post = tasks.feedback_on_post(customer_feedback_agent, draft_post)
rewrite_post = tasks.post_writing_with_feedback(posts_writer_agent, draft_post, feedback_on_post)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher_agent, posts_writer_agent, customer_feedback_agent],
    tasks=[research_info_for_post, draft_post, feedback_on_post, rewrite_post],
    verbose=2,
    process=Process.sequential,
    full_output=True,
    share_crew=False,
    step_callback=lambda x: print_agent_output(x,"MasterCrew Agent")
)

result=crew.kickoff({"topic": user_input})

#Print the results
print("Crew Work Results:")
print(result)
