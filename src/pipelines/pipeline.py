from src.agents.agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:

    state = {}               #dict to use as state memory

    print("\n" + "="*50)
    print("Step 1: Search agent is working...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })

    state["search_results"] = search_result['messages'][-1].content

    print("\n search_result ", state['search_results'])




    print("\n"+"="*50)
    print("Step 2: Reader agent is working...")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [
            ("user",
             f"Based on the following search results about {topic}"
             f"pick the most relevant URL and scrape it for deeper content"
             f"Search results:\n {state['search_results'][:800]}"
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScraped content: \n", state['scraped_content'])



    print("\n"+"="*50)
    print("Step 3: Writer chain is working....")
    print("="*50)

    combined_research = (
        f"SEARCH RESULTS: \n {state['search_results']}\n\n"
        f"SCRAPED CONTENT: \n {state['scraped_content']}\n\n"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": combined_research
    })

    print("Final report: ", state["report"])



    print("\n"+"="*50)
    print("Step 4: Critic chain is working....")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print('\n Critic Report: \n', state["feedback"])

    return state