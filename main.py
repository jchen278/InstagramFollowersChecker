from parser import get_all_followers, get_following

def main():
    # Define the folder where your JSONs live
    data_dir = "test_data"
    
    # Use the functions from parser.py
    followers = get_all_followers(data_dir)
    following = get_following(data_dir)
    
    # Logic: Set Difference
    not_following_back = following - followers
    print(f"You follow {len(following)}")
    print(f"{len(followers)} people follow you")
    print(f"Found {len(not_following_back)} people who don't follow you back.")

    for user in sorted(not_following_back):
        print(user)
    

if __name__ == "__main__":
    main()