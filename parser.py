import json
import glob

def get_all_followers(data_folder):
    all_followers = set()
    files = glob.glob(f"{data_folder}/followers_*.json")
    
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"--- Processing {file}: {len(data)} total entries found in file ---")
            
            for i, entry in enumerate(data):
                username = None
                
                # Strategy A: Look in string_list_data
                if 'string_list_data' in entry and entry['string_list_data']:
                    username = entry['string_list_data'][0].get('value')
                
                # Strategy B: Look in title (backup)
                if not username:
                    username = entry.get('title')
                
                if username:
                    all_followers.add(username.lower().strip())
                else:
                    # This is the "Aha!" moment
                    print(f"Skipping entry {i}: No username found. Data: {entry}")
                    
    return all_followers

def get_following(data_folder):
    # Following is an object {} with a 'relationships_following' key
    with open(f"{data_folder}/following.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        following_set = set()
        
        # Based on your snippet, the username is in the 'title' field
        for entry in data.get('relationships_following', []):
            try:
                username = entry.get('title')
                if username:
                    following_set.add(username)
            except Exception:
                continue
                
        return following_set