import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# STEP 1: LOAD CSV FILE
# ==========================================

try:
    df = pd.read_csv("movies.csv")
    print("\nCSV file loaded successfully!")

except FileNotFoundError:
    print("Error: movies.csv file not found!")
    exit()

except pd.errors.EmptyDataError:
    print("Error: CSV file is empty!")
    exit()

except Exception as e:
    print("Error while reading CSV:", e)
    exit()


# ==========================================
# STEP 2: EXPLORE DATA
# ==========================================

print("\n========== FIRST FIVE MOVIES ==========")
print(df.head())

print("\n========== DATA INFORMATION ==========")
df.info()

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe())


# ==========================================
# STEP 3: CHECK REQUIRED COLUMNS
# ==========================================

required_columns = ["Movie", "Genre", "Rating"]

if not all(column in df.columns for column in required_columns):
    print("\nError: CSV must contain Movie, Genre and Rating columns.")
    exit()


# ==========================================
# STEP 4: DATA CLEANING
# ==========================================

print("\n========== DATA CLEANING ==========")

# Create a copy of original data
df = df.copy()

# Remove extra spaces
df["Movie"] = df["Movie"].astype("string").str.strip()
df["Genre"] = df["Genre"].astype("string").str.strip()

# Convert rating into numeric values
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

# Check invalid rows
valid_rows = []

for index, row in df.iterrows():

    movie = row["Movie"]
    genre = row["Genre"]
    rating = row["Rating"]

    if pd.isna(movie) or movie == "":
        print(f"Row {index + 2} skipped: Missing movie name.")
    
    elif pd.isna(genre) or genre == "":
        print(f"Row {index + 2} skipped: Missing genre.")

    elif pd.isna(rating):
        print(f"Row {index + 2} skipped: Invalid rating.")

    elif rating < 0 or rating > 10:
        print(f"Row {index + 2} skipped: Rating must be between 0 and 10.")

    else:
        valid_rows.append(index)

# Keep only valid rows
df = df.loc[valid_rows].copy()

# Remove duplicate rows
before_duplicates = len(df)

df = df.drop_duplicates()

removed_duplicates = before_duplicates - len(df)

print("\nDuplicate rows removed:", removed_duplicates)
print("Valid rows:", len(df))

if df.empty:
    print("No valid movie data available!")
    exit()

print("\nData cleaned successfully!")


# ==========================================
# STEP 5: CREATE CHARTS FOLDER
# ==========================================

os.makedirs("charts", exist_ok=True)


# ==========================================
# STEP 6: MOVIE SUMMARY
# ==========================================

def movie_summary():

    print("\n========== MOVIE SUMMARY ==========")

    # Calculate average rating
    average_rating = df["Rating"].mean()

    # Find highest-rated movie
    top_movie = df.loc[df["Rating"].idxmax()]

    # Find lowest-rated movie
    lowest_movie = df.loc[df["Rating"].idxmin()]

    print("Average Rating:", round(average_rating, 2))

    print(
        "Top Rated Movie:",
        top_movie["Movie"],
        "(" + str(top_movie["Rating"]) + ")"
    )

    print(
        "Lowest Rated Movie:",
        lowest_movie["Movie"],
        "(" + str(lowest_movie["Rating"]) + ")"
    )

    print("\nMaximum Rating:", df["Rating"].max())
    print("Minimum Rating:", df["Rating"].min())


# ==========================================
# STEP 7: GENRE-WISE ANALYSIS
# ==========================================

def genre_analysis():

    print("\n========== GENRE-WISE ANALYSIS ==========")

    # Group movies by genre
    genre_average = df.groupby("Genre")["Rating"].mean()

    print("\nAverage Rating of Each Genre:")
    print(genre_average.round(2))

    # Find best genre
    best_genre = genre_average.idxmax()

    print("\nBest Genre:", best_genre)

    return genre_average


# ==========================================
# STEP 8: BAR CHART
# ==========================================

def show_bar_chart():

    genre_average = genre_analysis()

    plt.figure(figsize=(8, 5))

    genre_average.plot(
        kind="bar",
        color="skyblue",
        edgecolor="black"
    )

    plt.title("Genre-wise Average Movie Ratings")
    plt.xlabel("Movie Genre")
    plt.ylabel("Average Rating")

    plt.ylim(0, 10)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("charts/genre_bar_chart.png")

    plt.show()


# ==========================================
# STEP 9: HISTOGRAM
# ==========================================

def show_histogram():

    plt.figure(figsize=(8, 5))

    plt.hist(
        df["Rating"],
        bins=5,
        color="orange",
        edgecolor="black"
    )

    plt.title("Movie Rating Distribution")
    plt.xlabel("Movie Rating")
    plt.ylabel("Number of Movies")

    plt.tight_layout()

    plt.savefig("charts/rating_histogram.png")

    plt.show()


# ==========================================
# STEP 10: MAIN MENU
# ==========================================

while True:

    print("\n===================================")
    print("       MOVIE RATING ANALYZER")
    print("===================================")

    print("1. Movie Summary")
    print("2. Genre-wise Average Rating")
    print("3. Show Bar Chart")
    print("4. Show Histogram")
    print("5. Exit")

    choice = input("\nEnter your choice (1-5): ")

    if choice == "1":

        movie_summary()

    elif choice == "2":

        show_bar_chart()

    elif choice == "3":

        show_bar_chart()

    elif choice == "4":

        show_histogram()

    elif choice == "5":

        print("\nThank you for using Movie Rating Analyzer!")
        break

    else:

        print("\nInvalid choice! Please enter a number between 1 and 5.")