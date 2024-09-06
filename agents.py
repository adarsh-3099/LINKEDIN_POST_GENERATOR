from crewai import Agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import load_tools
import os
from langchain_groq import ChatGroq
from printGen import print_agent_output
from langchain.tools import Tool
import re
from collections import Counter
import textstat

llm_research = ChatGroq(
            api_key="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",
            model="llama3-70b-8192"
        )

llm_post = ChatGroq(
            api_key="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",
            model="llama-3.1-70b-versatile"
        )

llm_review = ChatGroq(
            api_key="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",
            model="mixtral-8x7b-32768"
        )

class LinkedInSearchTool(DuckDuckGoSearchRun):
    def _run(self, query: str) -> str:
        linkedin_query = f"site:linkedin.com {query}"
        return super()._run(linkedin_query)

linkedin_search_tool = Tool(
    name="LinkedInSearch",
    func=LinkedInSearchTool().run,
    description="Searches for LinkedIn posts and content related to the given query."
)

def suggest_hashtags(text, num_tags=3):
    words = re.findall(r'\w+', text.lower())
    word_counts = Counter(words)
    return [f"#{word}" for word, _ in word_counts.most_common(num_tags)]

hashtag_tool = Tool(
    name="HashtagRecommendation",
    func=suggest_hashtags,
    description="Suggests hashtags based on the post content."
)


class PostAgents():
    def make_researcher_agent(self):
        return Agent(
            role='Info Researcher Agent',
            goal="""take in a topic from a human and search any relevant information regarding the topic
            """,
            backstory="""You are a master at understanding what information we need to post regarding the topic""",
            llm=llm_research,
            verbose=True,
            max_iter=5,
            allow_delegation=False,
            memory=True,
            tools=[linkedin_search_tool],
            step_callback=lambda x: print_agent_output(x,"Info Researcher Agent"),
        )

    def make_posts_writer_agent(self):
        return Agent(
            role='Post Writer Agent',
            goal="""take in a post from a human and the research from the research agent and \
            write a helpful linkedin post in a thoughtful way as a content creator would do.
            """,
            backstory="""You are a master at synthesizing a variety of information and writing a helpful post""",
            llm=llm_post,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
            memory=True,
            step_callback=lambda x: print_agent_output(x,"Post Writer Agent"),
        )

    def make_customer_feedback_agent(self):
        return Agent(
            role='Customer Feedback Agent',
            goal="""Provide constructive and detailed feedback on the drafts of posts written by the Post Writer Agent \
            to help improve the content, tone, and engagement potential.""",
            backstory="""You have extensive experience in reviewing and critiquing content with a focus on improving readability, engagement, and overall quality.""",
            llm=llm_review,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
            memory=True,
            step_callback=lambda x: print_agent_output(x, "Customer Feedback Agent"),
        )

    