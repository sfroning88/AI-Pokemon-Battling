# AI-Powered Pokemon Team Builder - MVP Stage

## Project Abstract
This project creates an AI-powered platform for competitive Pokemon team building, currently in MVP development stage focusing on frontend functionality and user workflow.<br> The application allows users to authenticate via Google OAuth, submit natural language prompts for team building requests, and receive AI-generated Pokemon team recommendations.<br> This initial stage implements a dummy AI backend that echoes user prompts while establishing the complete user authentication, data storage, and frontend interaction pipeline.<br> The platform is designed as a not-for-profit educational tool for the competitive Pokemon VGC community.<br>

## How to Use
-> Navigate to the application URL provided by ngrok after local deployment<br>
-> Click "Sign in with Google" to authenticate using Google OAuth flow<br>
-> Accept the legal disclaimer modal on first homepage visit<br>
-> View your API usage statistics and any previously created teams on the homepage<br>
-> Click "Create New Team" to access the team building interface<br>
-> Enter a natural language prompt describing your desired Pokemon team strategy<br>
-> Receive a formatted response confirming your prompt was received by the system<br>
-> Navigate to "Prior Teams" to view saved team requests and submit feedback on team performance<br>
-> Log out when finished to clear your session data<br>

## Tech Stack
-> Frontend: HTML, CSS, JavaScript with Flask templating for dynamic content rendering<br>
-> Backend: Python Flask application handling routing, authentication, and database operations<br>
-> Database: Supabase PostgreSQL with Row Level Security for user data isolation<br>
-> Authentication: Google OAuth 2.0 integration through Google Cloud Console<br>
-> Deployment: Flask development server with ngrok for public URL access during MVP stage<br>
-> Future Migration: Planned transition to Vercel for production deployment with improved scaling<br>

## Warnings
-> This is an MVP implementation with dummy AI responses only - no actual AI model integration yet<br>
-> Google OAuth credentials must be properly configured in Google Cloud Console before authentication will function<br>
-> Supabase database connection requires valid project credentials and proper table schema setup<br>
-> ngrok provides temporary public URLs that change on restart - not suitable for production use<br>
-> No rate limiting or advanced security measures implemented in this MVP stage<br>
-> Legal considerations regarding Pokemon intellectual property are acknowledged but not fully addressed in MVP<br>

## Requirements
-> Python 3.8+ with Flask framework and Supabase client library installed<br>
-> Google Cloud Console project with OAuth 2.0 credentials configured for web application<br>
-> Supabase project with authentication enabled and Google OAuth provider configured<br>
-> ngrok account and installation for public URL generation during development<br>
-> Environment variables properly set for Supabase connection and Google OAuth credentials<br>
-> Basic understanding of Flask routing, HTML templating, and database operations<br>

## Cursor Agent
-> This project focuses exclusively on MVP frontend functionality and user workflow implementation<br>
-> Do not implement actual AI model integration, RAG systems, or embedding generation at this stage<br>
-> Prioritize simple, functional code over complex features or optimizations<br>
-> Use dummy responses for all AI-related functionality to avoid API costs during development<br>
-> Maintain focus on user authentication, database operations, and page navigation workflows<br>
-> Follow the step-by-step roadmap outlined in project documentation for proper implementation sequence<br>
-> Avoid adding features beyond the core MVP scope until basic functionality is fully operational<br>
-> Test each component thoroughly before proceeding to the next development stage<br>
