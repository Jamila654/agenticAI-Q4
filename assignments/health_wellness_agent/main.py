#type: ignore
import asyncio
from context import UserSessionContext
from utils.streamingformain import stream_conversation
from hooks import HealthPlannerHooks, HealthPlannerRunHooks
from dotenv import load_dotenv
from agent import create_health_agent

load_dotenv()

async def main():
    
    print("\n🌟 === Health & Wellness Assistant === 🌟")
    print("🏃‍♂️ Your guide to fitness goals, meal planning, and workouts! 🥗")
    print("💡 Type 'quit' to exit or 'debug' to toggle debug mode\n")
    
    debug_mode = True  # Debug mode enabled by default
    
    try:
        name = input("👤 What's your name? ")
        context = UserSessionContext(name=name, uid=1)
        
        agent = create_health_agent()
        agent_hooks = HealthPlannerHooks()
        agent.hooks = agent_hooks
        
        print(f"\n✅ Agent ready with hooks: {type(agent_hooks).__name__}")
        print(f"🐛 Debug mode: {'ON' if debug_mode else 'OFF'}")
        
        runner_hooks = HealthPlannerRunHooks()
        

        while True:
            try:
                print("\n" + "="*40)
                user_input = input(f"👤 {name}: ")
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Stay healthy! Goodbye!")
                    break
                elif user_input.lower() == 'debug':
                    debug_mode = not debug_mode
                    print(f"\n🐛 Debug mode: {'ON' if debug_mode else 'OFF'}")
                    continue
                    
                print("\n🤖 Assistant Response:")
                print("-"*40)
                
                if debug_mode:
                    print(f"🔍 Context logs before: {len(context.handoff_logs)} entries")
                
                await stream_conversation(agent, user_input, context, runner_hooks)
                
                print("\n📜 Log Summary:")
                print("-"*40)
                if context.handoff_logs:
                    print(f"📋 Total logs: {len(context.handoff_logs)}")
                    if debug_mode:
                        print("🔍 Recent logs (last 5):")
                        for log in context.handoff_logs[-5:]:
                            print(f"  📝 {log}")
                else:
                    print("⚠️ No logs generated")
                    
                print("="*40 + "\n")
                
            except KeyboardInterrupt:
                print("\n👋 Stay healthy! Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error in conversation: {str(e)}")
                if debug_mode:
                    import traceback
                    print("\n🔍 Debug Traceback:")
                    print("-"*40)
                    traceback.print_exc()
                    print("-"*40)
                    
    except KeyboardInterrupt:
        print("\n👋 Stay healthy! Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        if debug_mode:
            import traceback
            print("\n🔍 Error Traceback:")
            print("-"*40)
            traceback.print_exc()
            print("-"*40)

if __name__ == "__main__":
    asyncio.run(main())




