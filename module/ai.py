import numpy as np
import random
import pickle
import os

class AI2048:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995):
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.games_played = 0
        self.best_score = 0
        self.best_tile = 0
        self.version = 1  # Modellversion
        # Lade vorheriges Modell (falls vorhanden)
        self.load_model()

    def get_state(self, grid):
        return tuple(map(tuple, grid))

    def choose_action(self, game):
        state = self.get_state(game.grid)
        if random.random() < self.exploration_rate:
            return random.choice([0, 1, 2, 3])  # Zufallsbewegung
        if state in self.q_table:
            return np.argmax(self.q_table[state])
        return random.choice([0, 1, 2, 3])

    def update_q_table(self, old_state, action, reward, new_state):
        old_q_value = self.q_table.get(old_state, np.zeros(4))[action]
        future_q_value = max(self.q_table.get(new_state, np.zeros(4)))
        new_q_value = old_q_value + self.learning_rate * (reward + self.discount_factor * future_q_value - old_q_value)

        if old_state not in self.q_table:
            self.q_table[old_state] = np.zeros(4)
        self.q_table[old_state][action] = new_q_value

    def decay_exploration(self):
        self.exploration_rate *= self.exploration_decay
        self.exploration_rate = max(0.01, self.exploration_rate)

        def save_model(self):
            """Speichert das Modell nur nach einem abgeschlossenen Spiel (kein ständiges Speichern mehr)."""
            self.version += 1  # Versionsnummer erhöhen
            filename = "ai_model.pkl"  # Überschreibt immer dieselbe Datei
            with open(filename, "wb") as f:
                pickle.dump(self.q_table, f)
            
            # Speichere Modellinfos mit Version
            with open("model_info.txt", "w") as f:
                f.write(f"Version: {self.version}\n")
                f.write(f"Best Score: {self.best_score}\n")
                f.write(f"Best Tile: {self.best_tile}\n")
                f.write(f"Games Played: {self.games_played}\n")
            
            print(f"💾 Modell gespeichert als {filename} (Version {self.version})")

    def load_model(self):
        """Lädt das bestehende Modell, falls vorhanden."""
        if os.path.exists("app_data/ai_model.pkl"):  # Pfad angepasst
            with open("app_data/ai_model.pkl", "rb") as f:
                self.q_table = pickle.load(f)
            print("📥 Modell geladen: app_data/ai_model.pkl")

        # Lade gespeicherte Infos und Versionsnummer
        if os.path.exists("app_data/model_info.txt"):  # Pfad angepasst
            with open("app_data/model_info.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if "Version" in line:
                        self.version = int(line.split(": ")[1])
                    elif "Best Score" in line:
                        self.best_score = int(line.split(": ")[1])
                    elif "Best Tile" in line:
                        self.best_tile = int(line.split(": ")[1])
                    elif "Games Played" in line:
                        self.games_played = int(line.split(": ")[1])

        print(f"🔄 Aktuelle Modell-Version: {self.version}")