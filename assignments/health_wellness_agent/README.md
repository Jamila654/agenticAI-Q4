# 🧠 Health & Wellness AI Assistant

## Overview
The Health & Wellness AI Assistant is a cutting-edge conversational AI designed to empower users in achieving their fitness and health goals. Built with advanced natural language processing and a modular architecture, it offers personalized, data-driven support for a healthier lifestyle.

### Features
- 🎯 **Personalized Goal Analysis:** Interprets user health objectives from natural language input.
- 🥗 **Custom Meal Planning:** Generates 7-day meal plans for dietary preferences (e.g., vegetarian, keto, balanced).
- 🏋️‍♀️ **Workout Recommendations:** Delivers fitness routines tailored to user goals and experience levels.
- 📈 **Progress Tracking:** Monitors progress with motivational feedback.
- 📅 **Automated Check-ins:** Schedules regular reminders for consistency.
- 🤖 **Expert Agent Handoff:** Routes complex queries to specialized agents for nutrition, injury support, or human assistance.
- 🧠 **Context-Aware:** Retains user goals, preferences, and conversation history.
- 🧱 **Modular Design:** Easily extensible with plug-and-play tools and agents.

## 🚀 Architecture
The project leverages a modular, agent-based framework:

- **Agent Core:** Manages conversation flow, context, and tool orchestration.
- **Tools:** Async modules for meal planning, workout generation, scheduling, and tracking.
- **Context Model:** Stores session-specific data like goals and progress logs.
- **Lifecycle Hooks:** Ensures robust logging and monitoring.
- **Custom Agents:** Handles escalations and expert-level advice.
- **Gemini Integration:** Powered by Gemini-2.0-Flash for advanced natural language processing.

## 🌐 Deployment

- **FastAPI Backend:** [https://agentic-ai-q4-lfx4.vercel.app/](https://agentic-ai-q4-lfx4.vercel.app/)
- **Next.js Frontend:** [https://healthwellness-two.vercel.app/](https://healthwellness-two.vercel.app/)

## 🛠️ Getting Started

1. Visit the Next.js frontend to interact with the AI Assistant.
2. Access the FastAPI backend for API integrations.
3. Contribute by cloning the repository and extending functionality with custom tools or agents.
