from crewai import Crew,Process
from tasks import PostTasks
from agents import PostAgents
from printGen import print_agent_output
import gradio as gr
import textstat

# def replay_with_feedback(tasks,posts_writer_agent, user_input, research_info_for_post, previous_post, user_feedback):
#     """
#     Replay the crew execution for the draft_post task with user feedback.
#     """ 
#     # Create a new task with the previous post and user feedback
#     new_task = tasks.draft_post(posts_writer_agent, customer_feedback_agent, user_input, research_info_for_post, previous_post, user_feedback)
        
#     # Replay the crew execution with the new task
#     crew = Crew(
#         agents=[posts_writer_agent, customer_feedback_agent],
#         tasks=[research_info_for_post, draft_post],
#         verbose=2,
#         process=Process.sequential,
#         full_output=True,
#         share_crew=False,
#         step_callback=lambda x: print_agent_output(x,"MasterCrew Agent")    
#     )
#     return result.raw
    

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

# res_replay = crew.replay(task_id="44154d15-0903-4c2d-b0b9-c811e9737ce7", inputs={"agent": customer_feedback_agent, "draft_post": rewrite_post})
# print(res_replay)

# Get user feedback
# optimize_post_res = optimize_post(result.raw)
# print("Results", optimize_post_res)

# # gr.ChatInterface(
# #     chat_function,
# #     textbox=gr.Textbox(placeholder="Enter message here", container=False, scale = 7),
# #     chatbot=gr.Chatbot(height=400),
# #     additional_inputs=[
# #         gr.Textbox("You are helpful AI", label="System Prompt"),
# #         gr.Slider(500,4000, label="Max New Tokens"),
# #         gr.Slider(0,1, label="Temperature")
# #     ]
# #     ).launch()

# from crewai import Crew, Process
# from tasks import PostTasks
# from agents import PostAgents
# from printGen import print_agent_output
# import gradio as gr

# ## Agents and Tasks 
# agents = PostAgents()
# tasks = PostTasks()

# ## Agents
# researcher_agent = agents.make_researcher_agent()
# posts_writer_agent = agents.make_posts_writer_agent()

# def chat_function(user_input, history):
#     # Instantiate your crew with a sequential process
#     print(user_input)
#     user_input_dict = {"input": user_input} 
#     research_info_for_post = tasks.research_info_for_post(researcher_agent, user_input)
#     draft_post= tasks.draft_post(posts_writer_agent, user_input, research_info_for_post)
#     crew = Crew(
#         agents=[researcher_agent, posts_writer_agent],
#         tasks=[research_info_for_post, draft_post],
#         verbose=2,
#         process=Process.sequential,
#         full_output=True,
#         share_crew=False,
#         step_callback=lambda x: print_agent_output(x,"MasterCrew Agent")
#     )

#     # start the task execution process with the user's input
#     result = crew.kickoff(user_input_dict)
#     return result.raw

# gr.ChatInterface(
#     chat_function,
#     textbox=gr.Textbox(placeholder="Enter message here", container=False),
#     ).launch()
