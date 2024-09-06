from crewai import Task

class PostTasks():
    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100!"

    def research_info_for_post(self, agent, topic):
        return Task(
            description=f"""Conduct a comprehensive analysis of the topic provided and the category \
            provided and search the web to find info needed for the linkedin post
            POST CONTENT:\n\n {topic} \n\n
            Only provide the info needed DONT try to write the LinkedIn Post {self.__tip_section()}""",
            expected_output="""A set of bullet points of useful info for the post writer \
            or clear instructions that no useful material was found.""",
            output_file=f"research_info.txt",
            agent=agent
          )

    def draft_post(self, agent, topic, research_info_for_post):
        return Task(
            description=f"""
                Conduct a comprehensive analysis of the topic provided and the info provided from the research specialist to write a LinkedIn post.
                Use the information provided by the research specialist, but write the post in your own words. Keep the tone professional, yet conversational.
                POST CONTENT:
                A detailed LinkedIn post on {topic}
                {self.__tip_section()}
                """,
            expected_output="""
                A catchy Linkedin Post with proper hashtags.
            """,
            context=[research_info_for_post],
            agent=agent,
            output_file=f"draft_post.txt",
    )

    # def feedback_on_post(self, agent, draft_post):
    #     return Task(
    #         name="Provide Feedback on Post",
    #         description="""The task is to provide constructive feedback on the given post based on the customer feedback \
    #         The goal is to identify areas of improvement in the post and suggest enhancements. \
    #         If you do your BEST WORK, I'll tip you $100!
    #         """,
    #         agent=agent,
    #         prompt_template="""You have received a post and corresponding customer feedback. Your task is to critically assess the post and provide suggestions or edits to improve it based on the feedback. The feedback is as follows:
    #             Post Data
    #             Feedback
    #             Please provide your improved version of the post or suggest edits that would make the post more effective.
    #             """,
    #         expected_output="""
    #             A full fledged rating for the post and review it and give rating out of 10 for the post.
    #         """,
    #         context=[draft_post],
    #         step_callback=lambda x: print_agent_output(x, "Feedback Task"),
    #         output_file=f"suggestion.txt",
    #     )

    def feedback_on_post(self, agent, draft_post):
        return Task(
            description=f"""
            Review the following LinkedIn post and provide constructive feedback:

            {draft_post}

            Your feedback should cover:
            1. Content relevance and value
            2. Structure and readability
            3. Engagement potential
            4. Use of hashtags
            5. Overall impact and effectiveness
            6. An overall rating out of 10

            Be specific in your critique and offer suggestions for improvement.
            {self.__tip_section()}
            """,
            expected_output="""
            A comprehensive review of the post, including:
            - Strengths of the current post
            - Areas for improvement
            - Specific suggestions for enhancing engagement and reach
            - A rating out of 10 for the overall quality of the post
            """,
            agent=agent,
            step_callback=lambda x: print_agent_output(x, "Feedback Task"),
            output_file=f"suggestion.txt",
        )


    # def post_writing_with_feedback(self, agent, draft_post, feedback_on_post):
    #     return Task(
    #         name="LinkedIn Post Optimization",
    #         description=f"""
    #         Refine and optimize the LinkedIn post based on the initial draft and feedback provided.
    #         Your goal is to create a high-impact, engaging post that will reach a wider audience.

    #         Follow these guidelines:
    #         1. Incorporate the feedback from {feedback_on_post} thoughtfully.
    #         2. Ensure the post is concise yet impactful (aim for 1000-1300 characters).
    #         3. Use compelling language and a clear call-to-action.
    #         4. Include relevant hashtags (3-5) to increase discoverability.
    #         5. Structure the post for readability (short paragraphs, bullet points if appropriate).
    #         6. Incorporate a hook or question to encourage engagement.
    #         7. Ensure the content is valuable and relevant to the target audience.
    #         8. Polish the tone to match LinkedIn's professional yet conversational style.

    #         Original draft:
    #         {draft_post}

    #         Remember, your task is to significantly improve the post's potential reach and engagement.
    #         If you produce an EXCEPTIONAL post, you'll receive a $100 tip!
    #         """,
    #         max_iter=3,  # Increased to allow for more refinement
    #         agent=agent,
    #         expected_output=f"""
    #         A highly refined and optimized LinkedIn post that:
    #         - Addresses the feedback from {feedback_on_post}
    #         - Is engaging, concise, and formatted for maximum impact
    #         - Includes relevant hashtags
    #         - Has a clear call-to-action
    #         - Is designed to reach and resonate with a wider audience
    #         """,
    #         context=[draft_post, feedback_on_post],
    #         step_callback=lambda x: print_agent_output(x, "LinkedIn Post Optimization Task"),
    #         output_file="optimized_linkedin_post.txt",
    #     )

    def post_writing_with_feedback(self, agent, current_post, feedback):
        return Task(
            name="LinkedIn Post Optimization",
            description=f"""
            Refine and optimize the LinkedIn post based on the current post and feedback provided.
            Your goal is to create a high-impact, engaging post that addresses the feedback and reaches a wider audience.

            Follow these guidelines:
            1. Carefully consider and incorporate the feedback provided.
            2. Ensure the post is concise yet impactful (aim for 1000-1300 characters).
            3. Use compelling language and a clear call-to-action.
            4. Include relevant hashtags (3-5) to increase discoverability.
            5. Structure the post for readability (short paragraphs, bullet points if appropriate).
            6. Incorporate a hook or question to encourage engagement.
            7. Ensure the content is valuable and relevant to the target audience.
            8. Polish the tone to match LinkedIn's professional yet conversational style.

            Current post:
            {current_post}

            Feedback:
            {feedback}

            Remember, your task is to significantly improve the post's potential reach and engagement while addressing the feedback.
            {self.__tip_section()}
            """,
            agent=agent,
            expected_output=f"""
            A highly refined and optimized LinkedIn post that:
            - Addresses the provided feedback
            - Is engaging, concise, and formatted for maximum impact
            - Includes relevant hashtags
            - Has a clear call-to-action
            - Is designed to reach and resonate with a wider audience
            """,
            step_callback=lambda x: print_agent_output(x, "Rewrite Task"),
            output_file=f"rewrite.txt",
        )