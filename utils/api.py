import json, time

def get_query(client, assistant_id, thread_id, user_prompt, timeout = 30, poll_wait_seconds = 2):
    
    # cancel existing potentially still open runs
    runs = client.beta.threads.runs.list(thread_id)
    for r in runs.data:
        if r.status not in ("succeeded", "completed", "expired", "failed", "cancelled"):
            client.beta.threads.runs.cancel(
                thread_id=thread_id,
                run_id=r.id
            )
        

    # Set timed out flag to tell whether to return normally or raise an exception
    TIMED_OUT = False
    
    # create the message object
    message = client.beta.threads.messages.create(
        thread_id=thread_id, 
        role="user",
        content=user_prompt
    )

    # create the run object
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    
    # Start the clock
    START_TIME = time.time()
    
    # Poll for completion
    while True:
        
        # Get the latest state of the run
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        print(run_status)
        
        
        # Submit the tool output
        if run_status.status in ("requires_action"):
            tool_call_id = run_status.required_action.submit_tool_outputs.tool_calls[0].id
            tool_output = json.loads(run_status.required_action.submit_tool_outputs.tool_calls[0].function.arguments).get('query')
            run_update = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool_call_id,
                        "output": tool_output
                    }
                ]
            )
            
            # return the tool output
            return tool_output
            
            # later we can put code that actually does stuff but for now i need to get the run status in my environment and mess with it
            #break
        
        if run_status.status == "failed":
            print("Exception occurred:")
            print(run_status)

            if run_status.last_error is not None:
                errmsg = run_status.last_error.message
            
            raise Exception(errmsg)
        
        # Check if the run is completed
        if run_status.status in ("succeeded", "completed"):
            break

        # Wait a bit before polling again to avoid rate limits or excessive polling
        time.sleep(poll_wait_seconds)
        
        if ((time.time() - START_TIME) > timeout):
            TIMED_OUT = True
            break
        
    if TIMED_OUT:
        raise Exception(f"Call to assistant timed out. Here is the run ID: {run.id}")
    
    
    return ''