from crewai import Crew, Process
from tasks import PostTasks
from agents import PostAgents
from printGen import print_agent_output, agent_names, agent_outputs, agent_finishes, agent_dict

user_input = input("Enter your topic for the LinkedIn post: ")

## Agents and Tasks 
agents = PostAgents()
tasks = PostTasks()

## Agents
researcher_agent = agents.make_researcher_agent()
posts_writer_agent = agents.make_posts_writer_agent()
customer_feedback_agent = agents.make_customer_feedback_agent()

## Tasks
research_info_for_post = tasks.research_info_for_post(researcher_agent, user_input)
draft_post = tasks.draft_post(posts_writer_agent, user_input, research_info_for_post)
feedback_on_post = tasks.feedback_on_post(customer_feedback_agent, draft_post)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher_agent, posts_writer_agent, customer_feedback_agent],
    tasks=[research_info_for_post, draft_post, feedback_on_post],
    verbose=2,
    process=Process.sequential,
    full_output=True,
    share_crew=False,
)

result = crew.kickoff()

print("Initial Post:")
print(agent_dict["Post Writer Agent"])
print("\nInitial Feedback:")
print(agent_dict["Customer Feedback Agent"])

while True:
    user_choice = input("Do you want to regenerate the post based on feedback? (yes/no): ").lower()
    if user_choice != 'yes':
        break

    # Regenerate post based on feedback
    regenerate_post = tasks.post_writing_with_feedback(
        posts_writer_agent,
        agent_dict["Post Writer Agent"],
        agent_dict["Customer Feedback Agent"]
    )
    
    # Create a new crew for the regeneration task
    regenerate_crew = Crew(
        agents=[posts_writer_agent],
        tasks=[regenerate_post],
        verbose=2,
        process=Process.sequential,
        full_output=True,
    )
    
    regenerate_result = regenerate_crew.kickoff()

    # Update the agent_dict with the new post
    agent_dict["Post Writer Agent"] = agent_dict.get("Post Writer Agent", "")
    
    # Generate new feedback
    new_feedback = tasks.feedback_on_post(
        customer_feedback_agent,
        {"Post Writer Agent": agent_dict["Post Writer Agent"]}
    )
    
    feedback_crew = Crew(
        agents=[customer_feedback_agent],
        tasks=[new_feedback],
        verbose=2,
        process=Process.sequential,
        full_output=True,
    )
    
    feedback_result = feedback_crew.kickoff()

    print("\nRegenerated Post:")
    print(agent_dict["Post Writer Agent"])
    print("\nNew Feedback:")
    print(agent_dict["Customer Feedback Agent"])

print("Final Post:")
print(agent_dict["Post Writer Agent"])
