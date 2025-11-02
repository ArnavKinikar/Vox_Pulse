import datetime
from Config import *
from Pipeline.Orchestrator import NewsPipeline
from Pipeline.Modules.InsertDatabase import close_connection


# ----------------------------------
# Create the pipeline
# ----------------------------------
pipeline = NewsPipeline()

# ----------------------------------
# Define categories you want to fetch
# ----------------------------------
CATEGORIES = [
    "World",
]

# ----------------------------------
# Run pipeline once
# ----------------------------------
def run_pipeline():
    print("\n===================================")
    print("🚀 Starting News Pipeline Run")
    print(f"Timestamp: {datetime.datetime.now()}")
    print("===================================\n")

    for category in NEWS_API_QUERIES:
        try:
            print(f"\n📰 Running pipeline for: {category}")

            # Run the pipeline for each category
            results = pipeline.run(category)
            print(f"✅ Finished category: {category}\n")

        except Exception as e:
            print(f"❌ Error processing category '{category}': {e}")

    close_connection()

    print("\n✅ All categories processed successfully.")
    print("===================================\n")

# ----------------------------------
# Main Entry
# ----------------------------------
if __name__ == "__main__":
    # (A) Run once manually
    run_pipeline()

    # (B) Run every 24 hours automatically (optional)
    # while True:
    #     run_pipeline()
    #     print("Sleeping for 24 hours...")
    #     time.sleep(24 * 60 * 60)
