from crewai import Crew, Process
from tasks import PostTasks
from agents import PostAgents
from printGen import print_agent_output, agent_names, agent_outputs, agent_finishes, agent_dict
import textstat
import re

def extract_score_from_feedback(feedback_text):
    # Convert to lowercase for case-insensitive matching
    feedback_lower = feedback_text.lower()
    # List of possible rating indicators
    rating_indicators = ['rate', 'rating', 'score', 'grade']
    for indicator in rating_indicators:
        # Look for the indicator followed by optional characters and then a number
        match = re.search(rf'{indicator}.*?(\d+(?:\.\d+)?)/?\s*10', feedback_lower)
        if match:
            # Extract the numerical value
            score = float(match.group(1))
            return min(score, 10.0)  # Ensure the score doesn't exceed 10
    # If no match is found, return None or a default value
    return None

def calculate_improvement(previous_score, current_score):
    if previous_score == 0:
        return 100  # Assume 100% improvement if previous score was 0
    return ((current_score - previous_score) / previous_score) * 100

def evaluate_post(post, feedback, previous_score):
    # Extract numerical score from feedback (assuming it's provided)
    score = extract_score_from_feedback(feedback)
    if score is None:
        score = 7  # or some default value
    # Calculate other metrics
    length = len(post)
    readability_score = textstat.flesch_reading_ease(post)
    hashtag_count = post.count('#')
    # Check for engagement elements (simplified)
    has_question = '?' in post
    has_call_to_action = any(cta in post.lower() for cta in ['comment', 'share', 'like', 'follow'])
    # Calculate improvement rate
    improvement_rate = calculate_improvement(previous_score, score)
    return {
        'score': score,
        'length': length,
        'readability': readability_score,
        'hashtags': hashtag_count,
        'has_question': has_question,
        'has_cta': has_call_to_action,
        'improvement_rate': improvement_rate
    }

def is_post_satisfactory(evaluation, iteration):
    return (
        (evaluation['score'] >= 8.0 and
        1000 <= evaluation['length'] <= 1300 and
        evaluation['readability'] >= 60 and
        3 <= evaluation['hashtags'] <= 5 and
        (evaluation['has_question'] or evaluation['has_cta']) and
        evaluation['improvement_rate'] < 5) or
        iteration >= 4
    )

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

iteration = 0
previous_score = 0

while True:
    evaluation = evaluate_post(agent_dict["Post Writer Agent"], agent_dict["Customer Feedback Agent"], previous_score)

    if is_post_satisfactory(evaluation, iteration):
        break
    
    previous_score = evaluation['score']
    iteration += 1

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
