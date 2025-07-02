# type: ignore
import streamlit as st
import asyncio
import nest_asyncio
from context import UserSessionContext
from utils.streaming import stream_conversation
from hooks import HealthPlannerHooks, HealthPlannerRunHooks
from dotenv import load_dotenv
from agent import create_health_agent
import time
load_dotenv()

# Apply nest_asyncio to allow nested event loops in Streamlit
nest_asyncio.apply()

async def async_stream_response(agent, user_input, context, runner_hooks, placeholder):
    response_text = ""
    async for chunk in stream_conversation(agent, user_input, context, runner_hooks):
        response_text += chunk
        placeholder.markdown(response_text)
    return response_text

def main():
    st.set_page_config(page_title="Health & Wellness Assistant", page_icon="🥗", layout="wide")

    st.title("🌟 Health & Wellness Assistant 🌟")
    st.markdown("🏃‍♂️ Your guide to fitness goals, meal planning, and workouts! 💪")
    st.markdown("💡 Enter your query below or type 'quit', 'exit', or 'bye' to end the conversation.")

    if "context" not in st.session_state:
        st.session_state.name = st.text_input("👤 What's your name?", key="name_input")
        if st.session_state.name:
            st.session_state.context = UserSessionContext(name=st.session_state.name, uid=1)
            st.session_state.agent = create_health_agent()
            st.session_state.agent_hooks = HealthPlannerHooks()
            st.session_state.agent.hooks = st.session_state.agent_hooks
            st.session_state.runner_hooks = HealthPlannerRunHooks()
            st.session_state.debug_mode = True
            st.success(f"✅ Agent ready with hooks: {type(st.session_state.agent_hooks).__name__}")
            st.info(f"🐛 Debug mode: {'ON' if st.session_state.debug_mode else 'OFF'}")
        else:
            st.warning("Please enter your name to start.")
            return

    if st.button("🐛 Toggle Debug Mode"):
        st.session_state.debug_mode = not st.session_state.debug_mode
        st.info(f"🐛 Debug mode: {'ON' if st.session_state.debug_mode else 'OFF'}")

    user_input = st.text_input(f"👤 {st.session_state.name}:", key="user_input")

    if user_input:
        if user_input.lower() in ['quit', 'exit', 'bye']:
            st.success("👋 Stay healthy! Goodbye!")
            time.sleep(1)  # Give a moment for the user to read the message
            st.session_state.clear()
            #refresh the page to reset the session
            st.rerun()
            return

        st.markdown("\n🤖 Assistant Response:")
        st.markdown("-" * 40)

        if st.session_state.debug_mode:
            st.markdown(f"🔍 Context logs before: {len(st.session_state.context.handoff_logs)} entries")

        placeholder = st.empty()

        try:
            asyncio.run(
                async_stream_response(
                    st.session_state.agent,
                    user_input,
                    st.session_state.context,
                    st.session_state.runner_hooks,
                    placeholder
                )
            )
        except Exception as e:
            st.error(f"❌ Error in conversation: {str(e)}")
            if st.session_state.debug_mode:
                import traceback
                st.markdown("🔍 Debug Traceback:")
                st.markdown("-" * 40)
                st.code(traceback.format_exc())
                st.markdown("-" * 40)

        st.markdown("\n📜 Log Summary:")
        st.markdown("-" * 40)
        if st.session_state.context.handoff_logs:
            st.markdown(f"📋 Total logs: {len(st.session_state.context.handoff_logs)}")
            if st.session_state.debug_mode:
                with st.expander("🔍 Recent logs:", expanded=True):
                    for log in st.session_state.context.handoff_logs:
                        st.markdown(f"📝 {log}")
        else:
            st.warning("⚠️ No logs generated")

        st.markdown("=" * 40)

if __name__ == "__main__":
    main()
