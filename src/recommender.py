from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def score_song(self, song: Song, user: UserProfile) -> float:
        """
        Calculate the score for a song based on user preferences.
        +2.0 points for genre match
        +1.0 point for mood match
        Similarity points (0-1) based on energy closeness
        """
        score = 0.0
        
        # Genre match: +2.0
        if song.genre == user.favorite_genre:
            score += 2.0
        
        # Mood match: +1.0
        if song.mood == user.favorite_mood:
            score += 1.0
        
        # Energy similarity: 1.0 - absolute difference (ranges from 0 to 1)
        energy_similarity = 1.0 - abs(song.energy - user.target_energy)
        score += energy_similarity
        
        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # Score all songs and sort by score descending
        scored_songs = [(song, self.score_song(song, user)) for song in self.songs]
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [song for song, score in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score = self.score_song(song, user)
        reasons = []
        
        if song.genre == user.favorite_genre:
            reasons.append("genre match (+2.0)")
        if song.mood == user.favorite_mood:
            reasons.append("mood match (+1.0)")
        
        energy_diff = abs(song.energy - user.target_energy)
        energy_score = 1.0 - energy_diff
        reasons.append(f"energy similarity ({energy_score:.2f})")
        
        reason_str = ", ".join(reasons)
        return f"Total score: {score:.2f} - {reason_str}"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            song_dict = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness'])
            }
            songs.append(song_dict)
    return songs

def score_song(song: Dict, user_prefs: Dict) -> float:
    """
    Calculate the score for a song based on user preferences.
    +2.0 points for genre match
    +1.0 point for mood match
    Similarity points (0-1) based on energy closeness
    """
    score = 0.0
    
    # Genre match: +2.0
    if song['genre'] == user_prefs['genre']:
        score += 2.0
    
    # Mood match: +1.0
    if song['mood'] == user_prefs['mood']:
        score += 1.0
    
    # Energy similarity: 1.0 - absolute difference (ranges from 0 to 1)
    energy_similarity = 1.0 - abs(song['energy'] - user_prefs['energy'])
    score += energy_similarity
    
    return score

def explain_score(song: Dict, user_prefs: Dict) -> str:
    """
    Generate explanation for the song score.
    """
    score = score_song(song, user_prefs)
    reasons = []
    
    if song['genre'] == user_prefs['genre']:
        reasons.append("genre match (+2.0)")
    if song['mood'] == user_prefs['mood']:
        reasons.append("mood match (+1.0)")
    
    energy_diff = abs(song['energy'] - user_prefs['energy'])
    energy_score = 1.0 - energy_diff
    reasons.append(f"energy similarity ({energy_score:.2f})")
    
    reason_str = ", ".join(reasons)
    return f"Total score: {score:.2f} - {reason_str}"

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Score all songs
    scored_songs = []
    for song in songs:
        score = score_song(song, user_prefs)
        explanation = explain_score(song, user_prefs)
        scored_songs.append((song, score, explanation))
    
    # Sort by score descending
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    return scored_songs[:k]
