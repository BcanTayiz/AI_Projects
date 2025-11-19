import trueskill

# Initialize TrueSkill environment
env = trueskill.TrueSkill(draw_probability=0)

def compare_pair(text1_score, text2_score):
    """
    Compare two CV scores and return winner/loser for TrueSkill update
    """
    rating1 = env.Rating(mu=text1_score)
    rating2 = env.Rating(mu=text2_score)
    
    if text1_score >= text2_score:
        rating1, rating2 = env.rate_1vs1(rating1, rating2)
        winner = "CV1"
    else:
        rating2, rating1 = env.rate_1vs1(rating2, rating1)
        winner = "CV2"
    
    return winner, rating1, rating2
