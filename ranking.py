import random
import csv

# Load songs from CSV
def load_songs(filename):
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        songs = [
            {
                "Name": row["Name"],
                "Artist": row["Artist"],
                "Score": int(row["Score"]),
                "Appearances": int(row["Appearances"]),
                "Likeability": float(row.get("Likeability", 0))  # Default to 0 if not present
            }
            for row in reader
        ]
    return songs

# Save songs to CSV
def save_songs(filename, songs):
    for song in songs:
        # Calculate Likeability: (Score / Appearances) * 100
        if song["Appearances"] > 0:
            song["Likeability"] = (song["Score"] / song["Appearances"]) * 100
        else:
            song["Likeability"] = 0  # Avoid division by zero

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "Artist", "Score", "Appearances", "Likeability"])
        writer.writeheader()
        writer.writerows(songs)

# Weighted random selection
def choose_songs(songs):
    weights = [1 / (song["Appearances"] + 1) for song in songs]  # +1 to avoid division by zero
    return random.choices(songs, weights=weights, k=2)

# Weighted random selection based on Likeability
def choose_songs_based_on_likeability(songs):
    # Ensure likeability is non-zero
    high_likeability_songs = [song for song in songs if song["Likeability"] >= 0 and song["Likeability"] <= 20]
    return random.sample(high_likeability_songs, 2)

# Voting mechanism
def vote(song1, song2):
    print(f"\nWhich song do you prefer?\n1: {song1['Name']} - {song1['Artist']}\n2: {song2['Name']} - {song2['Artist']}")
    choice = input("Enter 1, 2, or 'q' to quit: ").strip()
    if choice == "1":
        song1["Score"] += 1
    elif choice == "2":
        song2["Score"] += 1
    elif choice.lower() == "q":
        return False  # Quit signal
    else:
        print("Invalid choice. Try again.")
        return vote(song1, song2)
    song1["Appearances"] += 1
    song2["Appearances"] += 1
    return True

# Main function
def main():
    filename = "songs.csv"
    songs = load_songs(filename)

    print("Welcome to the song ranking system!")
    while True:  # Allow for repeated rounds
        song1, song2 = choose_songs(songs)
        while song1 == song2:  # Ensure two distinct songs
            song2 = random.choice(songs)

        if not vote(song1, song2):
            print("Saving progress and exiting...")
            save_songs(filename, songs)
            break

    # Display rankings
    sorted_songs = sorted(songs, key=lambda x: x["Likeability"], reverse=True)
    print("\nCurrent Rankings:")
    for idx, song in enumerate(sorted_songs, 1):
        print(f"{idx}: {song['Name']} - {song['Artist']} (Likeability: {song['Likeability']:.2f}%, Score: {song['Score']}, Appearances: {song['Appearances']})")

if __name__ == "__main__":
    main()
