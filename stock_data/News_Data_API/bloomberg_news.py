import blpapi
from datetime import datetime

# Bloomberg API session
def create_session():
    session = blpapi.Session()
    if not session.start():
        raise Exception("Failed to start Bloomberg session.")
    return session

# Retrieve news for a specific query
def retrieve_news(session, query, start_date, end_date):
    try:
        # Attempt to open the Bloomberg News service
        if not session.openService("//blp/news"):
            raise Exception("Failed to open Bloomberg News service. Ensure you have access to //blp/news.")

        news_service = session.getService("//blp/news")
        request = news_service.createRequest("newsQueryRequest")
        
        # Set query parameters
        request.set("query", query)  # Search for related terms (S&P 500, Nasdaq-100)
        request.set("startDateTime", start_date.isoformat())
        request.set("endDateTime", end_date.isoformat())
        request.set("maxResults", 10)  # Adjust for how many articles you want

        print(f"Requesting news for: {query} from {start_date} to {end_date}")
        
        # Send the request and process the response
        session.sendRequest(request)
        while True:
            event = session.nextEvent()
            for msg in event:
                if msg.messageType() == blpapi.Name("newsStory"):
                    story_id = msg.getElementAsString("storyId")
                    headline = msg.getElementAsString("headline")
                    print(f"Headline: {headline} (Story ID: {story_id})")
            if event.eventType() == blpapi.Event.RESPONSE:
                break
    except Exception as e:
        print(f"Error retrieving news: {e}")

if __name__ == "__main__":
    session = None
    try:
        # Create and start Bloomberg session
        session = create_session()
        
        # Test if other services like mktdata are accessible
        if not session.openService("//blp/mktdata"):
            raise Exception("Failed to open Bloomberg Market Data service. Please check your Bloomberg API setup.")
        print("Successfully connected to Bloomberg Market Data service.")
        
        # Define your parameters for the news request
        query = "S&P 500 OR Nasdaq-100"  # Customize search terms as needed
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 11, 25)  # Adjust to your desired date range
        
        # Retrieve and display news data
        retrieve_news(session, query, start_date, end_date)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Ensure session is properly stopped
        if session is not None:
            session.stop()
