from flask import Blueprint, request, jsonify, session
import logging
from langchain_core.messages import HumanMessage
from langchain_integration.langgraph_flow import get_langgraph

logger = logging.getLogger(__name__)
chat_api = Blueprint('chat_api', __name__)

graph = get_langgraph()

def get_response(user_msg, session_id):
    config = {"configurable": {"thread_id":session_id, "user_id": session_id}}

    stream = graph.stream({"messages": [user_msg]}, config, stream_mode="values")

    outputs = []
    for step in stream:
        # Log each step
        logger.info(f"Graph step output: {step}")
        if hasattr(step["messages"][-1], "content"):
            outputs.append(step["messages"][-1].content)
    return outputs


@chat_api.route("/chat", methods=["POST"])
def chat_new():
    msg = request.json.get("message")
    if not msg:
        return jsonify({"error": "Invalid json payload. Provide message in message field"}), 400

    # Currently implemented for single thread
    session_id = request.cookies.get("session_id")
    if not session_id:
        return jsonify({"error": "Cookie not set. Sign up or Sign in if already a user"}), 400
    session['session_id'] = session_id

    # Convert to proper HumanMessage
    user_msg = HumanMessage(content=msg)

    outputs = get_response(user_msg, session_id)

    if outputs:
        return jsonify({"response": outputs[-1]})
    else:
        return jsonify({"response": "No response generated", "debug_info": str(outputs)})

