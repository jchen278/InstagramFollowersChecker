from parser import get_all_followers, get_following

def analyze_relationships(data_dir):
    """
    Takes a directory path and returns the sets of relationships.
    """
    followers = get_all_followers(data_dir)
    following = get_following(data_dir)
    
    # Calculate different categories
    not_following_back = following - followers
    fans = followers - following
    mutuals = following & followers
    
    return {
        "not_following_back": sorted(list(not_following_back)),
        "fans": sorted(list(fans)),
        "mutuals": sorted(list(mutuals)),
        "counts": {
            "following": len(following),
            "followers": len(followers)
        }
    }