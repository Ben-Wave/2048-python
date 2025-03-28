import pygame
import random
import os
from module.const import GameConfig
from module.ai import AI2048

class Game2048:
    def __init__(self):
        self.config = GameConfig()  # Konfiguration des Spiels
        # Logisches Raster: Zahl in jeder Zelle
        self.grid = [[0 for _ in range(self.config.GRID_SIZE)] for _ in range(self.config.GRID_SIZE)]
        self.score = 0
        self.high_score_path = os.path.join("app_data", "highscore.txt")
        self.high_score = self._load_high_score()
        self.best_tile = 0  # Höchster Wert, der erreicht wurde
        self.game_over = False
        self.game_won = False
        self.continue_after_win = False
        
        # Animationen
        self.spawn_animations = {}
        self.animations = []
        self.moving = False
        self.move_anim_progress = 0
        self.new_grid = None
        
        # Merges für Merge-Animation
        self.merges = []
        self.merge_scale = 1.0
        self.merge_phase = 0  # 0: nicht aktiv, 1: wachsen, 2: schrumpfen
        
        # Zu Beginn zwei zufällige Kacheln
        self.add_new_tile()
        self.add_new_tile()
        
        # AI
        self.ai = AI2048()
        self.ai.load_model()
        
    def _load_high_score(self):
        """Lädt den Highscore aus der Datei app_data/highscore.txt oder gibt 0 zurück, falls nicht vorhanden."""
        try:
            with open(self.high_score_path, "r") as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def _save_high_score(self):
        """Speichert den aktuellen Highscore in der Datei app_data/highscore.txt."""
        os.makedirs("app_data", exist_ok=True)  # Falls app_data nicht existiert, erstelle es
        with open(self.high_score_path, "w") as f:
            f.write(str(self.high_score))

    def add_new_tile(self):
        """Fügt an einer leeren Stelle eine 2 oder 4 hinzu und startet den Spawn-Effekt."""
        empty_cells = [(i, j) for i in range(self.config.GRID_SIZE) for j in range(self.config.GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            value = 2 if random.random() < 0.9 else 4
            self.grid[i][j] = value
            self.spawn_animations[(i, j)] = 0  # Startet Spawn-Animation
            
            # Aktualisiere best_tile wenn nötig
            if value > self.best_tile:
                self.best_tile = value

    def process_line(self, line):
        """
        Verarbeitet eine Zeile oder Spalte (als Liste von Zahlen).
        Gibt (neue Linie, animations_info, Punkte) zurück.
        """
        non_zero = [(val, idx) for idx, val in enumerate(line) if val != 0]
        new_line = []
        anims = []
        points = 0
        merge_positions = []  # Für Merge-Animationen
        
        i = 0
        while i < len(non_zero):
            if i < len(non_zero) - 1 and non_zero[i][0] == non_zero[i+1][0]:
                merged_value = non_zero[i][0] * 2
                points += merged_value
                new_line.append(merged_value)
                target_index = len(new_line) - 1
                
                # Bei einem Merge beide Kacheln zum Ziel bewegen
                anims.append({'value': non_zero[i][0], 'start_index': non_zero[i][1], 
                             'end_index': target_index, 'merge': True})
                anims.append({'value': non_zero[i+1][0], 'start_index': non_zero[i+1][1], 
                             'end_index': target_index, 'merge': True})
                
                # Speichere Position für Merge-Animation
                merge_positions.append(target_index)
                
                # Aktualisiere best_tile wenn nötig
                if merged_value > self.best_tile:
                    self.best_tile = merged_value
                
                i += 2
            else:
                new_line.append(non_zero[i][0])
                target_index = len(new_line) - 1
                anims.append({'value': non_zero[i][0], 'start_index': non_zero[i][1], 
                             'end_index': target_index, 'merge': False})
                i += 1
                
        # Fülle mit Nullen auf
        while len(new_line) < self.config.GRID_SIZE:
            new_line.append(0)
            
        return new_line, anims, points, merge_positions

    def compute_move(self, direction):
        """
        Berechnet das neue Raster und erstellt Animationsdaten für den Zug.
        direction: 0=Up, 1=Right, 2=Down, 3=Left
        """
        moved = False
        total_points = 0
        new_grid = [[0 for _ in range(self.config.GRID_SIZE)] for _ in range(self.config.GRID_SIZE)]
        animations = []
        merges = []  # Liste aller Merge-Positionen (row, col)

        # Hilfsfunktion zum Vergleich zweier Zeilen
        def different(line1, line2):
            return any(a != b for a, b in zip(line1, line2))

        if direction in (3, 1):  # Horizontal (Left:3, Right:1)
            for i in range(self.config.GRID_SIZE):
                row = self.grid[i][:]
                if direction == 1:  # Rechts
                    row_rev = row[::-1]
                    new_line, anims, pts, merge_pos = self.process_line(row_rev)
                    new_line = new_line[::-1]
                    
                    # Konvertiere Merge-Positionen für rechte Richtung
                    row_merges = [(i, self.config.GRID_SIZE - 1 - pos) for pos in merge_pos]
                    merges.extend(row_merges)
                    
                    total_points += pts
                    if different(row, new_line):
                        moved = True
                    new_grid[i] = new_line
                    
                    # Passe Animationsdaten an
                    for anim in anims:
                        orig = self.config.GRID_SIZE - 1 - anim['start_index']
                        target = self.config.GRID_SIZE - 1 - anim['end_index']
                        animations.append({
                            'value': anim['value'],
                            'horizontal': True,
                            'row': i,
                            'start_idx': orig,
                            'end_idx': target,
                            'merge': anim['merge']
                        })
                else:  # Links
                    new_line, anims, pts, merge_pos = self.process_line(row)
                    
                    # Speichere Merge-Positionen
                    row_merges = [(i, pos) for pos in merge_pos]
                    merges.extend(row_merges)
                    
                    total_points += pts
                    if different(row, new_line):
                        moved = True
                    new_grid[i] = new_line
                    
                    for anim in anims:
                        animations.append({
                            'value': anim['value'],
                            'horizontal': True,
                            'row': i,
                            'start_idx': anim['start_index'],
                            'end_idx': anim['end_index'],
                            'merge': anim['merge']
                        })
        else:  # Vertikal (Up:0, Down:2)
            for j in range(self.config.GRID_SIZE):
                col = [self.grid[i][j] for i in range(self.config.GRID_SIZE)]
                if direction == 2:  # Runter
                    col_rev = col[::-1]
                    new_col, anims, pts, merge_pos = self.process_line(col_rev)
                    new_col = new_col[::-1]
                    
                    # Konvertiere Merge-Positionen für Abwärtsbewegung
                    col_merges = [(self.config.GRID_SIZE - 1 - pos, j) for pos in merge_pos]
                    merges.extend(col_merges)
                    
                    total_points += pts
                    if different(col, new_col):
                        moved = True
                    for i in range(self.config.GRID_SIZE):
                        new_grid[i][j] = new_col[i]
                        
                    for anim in anims:
                        orig = self.config.GRID_SIZE - 1 - anim['start_index']
                        target = self.config.GRID_SIZE - 1 - anim['end_index']
                        animations.append({
                            'value': anim['value'],
                            'horizontal': False,
                            'col': j,
                            'start_idx': orig,
                            'end_idx': target,
                            'merge': anim['merge']
                        })
                else:  # Hoch
                    new_col, anims, pts, merge_pos = self.process_line(col)
                    
                    # Speichere Merge-Positionen
                    col_merges = [(pos, j) for pos in merge_pos]
                    merges.extend(col_merges)
                    
                    total_points += pts
                    if different(col, new_col):
                        moved = True
                    for i in range(self.config.GRID_SIZE):
                        new_grid[i][j] = new_col[i]
                        
                    for anim in anims:
                        animations.append({
                            'value': anim['value'],
                            'horizontal': False,
                            'col': j,
                            'start_idx': anim['start_index'],
                            'end_idx': anim['end_index'],
                            'merge': anim['merge']
                        })
                        
        return new_grid, animations, total_points, moved, merges

    def move(self, direction):
        """
        Löst einen Zug aus – berechnet neue Positionen und startet die Bewegungsanimation.
        direction: 0=Up, 1=Right, 2=Down, 3=Left
        """
        if self.moving or (self.game_over and not self.game_won) or (self.game_won and not self.continue_after_win):
            return False

        new_grid, anims, pts, moved, merges = self.compute_move(direction)
        if moved:
            self.moving = True
            self.move_anim_progress = 0
            self.new_grid = new_grid
            self.animations = anims
            self.merges = merges
            self.score += pts
            
            # Highscore aktualisieren
            if self.score > self.high_score:
                self.high_score = self.score
                self._save_high_score()
                
        return moved

    def is_game_over(self):
        """Überprüft, ob keine Züge mehr möglich sind."""
        # Prüfe auf leere Zellen
        if any(self.grid[i][j] == 0 for i in range(self.config.GRID_SIZE) for j in range(self.config.GRID_SIZE)):
            return False
            
        # Prüfe horizontal
        for i in range(self.config.GRID_SIZE):
            for j in range(self.config.GRID_SIZE - 1):
                if self.grid[i][j] == self.grid[i][j+1]:
                    return False
                    
        # Prüfe vertikal
        for i in range(self.config.GRID_SIZE - 1):
            for j in range(self.config.GRID_SIZE):
                if self.grid[i][j] == self.grid[i+1][j]:
                    return False
                    
        return True

    def check_win(self):
        """Überprüft, ob 2048 erreicht wurde."""
        if not self.game_won and any(self.grid[i][j] >= 2048 for i in range(self.config.GRID_SIZE) for j in range(self.config.GRID_SIZE)):
            self.game_won = True
            return True
        return False

    def continue_game(self):
        """Ermöglicht das Weiterspielen nach dem Erreichen von 2048."""
        self.continue_after_win = True

    def reset_game(self):
        """Startet ein neues Spiel."""
        self.grid = [[0 for _ in range(self.config.GRID_SIZE)] for _ in range(self.config.GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.game_won = False
        self.continue_after_win = False
        self.best_tile = 0
        self.spawn_animations = {}
        self.animations = []
        self.moving = False
        self.merges = []
        self.merge_phase = 0
        self.merge_scale = 1.0
        
        # Zu Beginn zwei zufällige Kacheln
        self.add_new_tile()
        self.add_new_tile()

    def update(self, dt):
        """Aktualisiert die Animationen."""
        if self.moving:
            self.move_anim_progress += dt
            if self.move_anim_progress >= self.config.MOVE_ANIMATION_DURATION:
                # Bewegungsanimation beendet
                self.grid = self.new_grid
                self.moving = False
                self.animations = []
                self.new_grid = None
                
                # Starte Merge-Animation wenn Merges vorhanden
                if self.merges:
                    self.merge_phase = 1  # Wachstumsphase
                    self.merge_scale = 1.0
                else:
                    # Wenn keine Merge-Animation, direkt neue Kachel hinzufügen
                    self.add_new_tile()
                    self.check_win()
                    if self.is_game_over():
                        self.game_over = True
        
        # Update Merge-Animation
        if self.merge_phase > 0:
            scale_change = dt / self.config.MERGE_ANIMATION_DURATION * 0.3  # Max 30% Größenänderung
            
            if self.merge_phase == 1:  # Wachsen
                self.merge_scale += scale_change
                if self.merge_scale >= 1.3:  # 30% größer
                    self.merge_scale = 1.3
                    self.merge_phase = 2  # Umschalten auf Schrumpfen
            else:  # Schrumpfen
                self.merge_scale -= scale_change
                if self.merge_scale <= 1.0:  # Zurück zur Normalgröße
                    self.merge_scale = 1.0
                    self.merge_phase = 0  # Animation beenden
                    self.merges = []
                    
                    # Merge-Animation beendet, neue Kachel hinzufügen
                    self.add_new_tile()
                    self.check_win()
                    if self.is_game_over():
                        self.game_over = True
        
        # Update Spawn-Animationen
        keys_to_remove = []
        for key in self.spawn_animations:
            self.spawn_animations[key] += dt
            if self.spawn_animations[key] >= self.config.SPAWN_ANIMATION_DURATION:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del self.spawn_animations[key]

    def draw(self, screen):
        """Zeichnet das Spielfeld."""
        screen.fill(self.config.BACKGROUND_COLOR)
        
        # Zeichne alle Zellen als Hintergrund (leere Felder)
        for i in range(self.config.GRID_SIZE):
            for j in range(self.config.GRID_SIZE):
                x = self.config.GRID_PADDING + j * (self.config.CELL_SIZE + self.config.CELL_MARGIN)
                y = self.config.GRID_PADDING + i * (self.config.CELL_SIZE + self.config.CELL_MARGIN)
                pygame.draw.rect(screen, self.config.TILE_COLORS.get(0, self.config.EMPTY_CELL_COLOR),
                                 (x, y, self.config.CELL_SIZE, self.config.CELL_SIZE), 0, 5)

        # Erstelle eine Menge der Zellen, die animiert werden
        animated_origins = set()
        for anim in self.animations:
            if anim['horizontal']:
                animated_origins.add((anim['row'], anim['start_idx']))
            else:
                animated_origins.add((anim['start_idx'], anim['col']))
        
        # Zeichne stationäre Kacheln
        for i in range(self.config.GRID_SIZE):
            for j in range(self.config.GRID_SIZE):
                # Falls diese Zelle gerade animiert wird, überspringen
                if (i, j) in animated_origins:
                    continue
                    
                value = self.grid[i][j]
                if value != 0:
                    x = self.config.GRID_PADDING + j * (self.config.CELL_SIZE + self.config.CELL_MARGIN)
                    y = self.config.GRID_PADDING + i * (self.config.CELL_SIZE + self.config.CELL_MARGIN)
                    
                    # Skalieren, wenn diese Zelle Teil eines Merges ist
                    scale = 1.0
                    if (i, j) in self.merges and self.merge_phase > 0:
                        scale = self.merge_scale
                    
                    # Berechne skalierte Position und Größe
                    if scale != 1.0:
                        scaled_size = int(self.config.CELL_SIZE * scale)
                        offset = (self.config.CELL_SIZE - scaled_size) // 2
                        rect = (x + offset, y + offset, scaled_size, scaled_size)
                    else:
                        rect = (x, y, self.config.CELL_SIZE, self.config.CELL_SIZE)
                    
                    pygame.draw.rect(screen, self.config.TILE_COLORS.get(value, self.config.TILE_COLORS[2048]),
                                     rect, 0, 5)
                                     
                    # Wähle Schriftgröße basierend auf Ziffernanzahl
                    if value < 10:
                        f = self.config.font['large']
                    elif value < 100:
                        f = self.config.font['medium']
                    elif value < 1000:
                        f = self.config.font['small']
                    else:
                        f = self.config.font['extra_small']
                        
                    text = f.render(str(value), True, self.config.TEXT_COLORS.get(value, self.config.FONT_COLOR))
                    
                    # Positioniere Text im Zentrum der skalierten Kachel
                    text_rect = text.get_rect(center=(x + self.config.CELL_SIZE // 2, y + self.config.CELL_SIZE // 2))
                    
                    screen.blit(text, text_rect)
        
        # Zeichne Bewegungsanimationen
        if self.moving:
            t = min(self.move_anim_progress / self.config.MOVE_ANIMATION_DURATION, 1.0)
            for anim in self.animations:
                if anim['horizontal']:
                    row = anim['row']
                    start_x = self.config.GRID_PADDING + anim['start_idx'] * (self.config.CELL_SIZE + self.config.CELL_MARGIN)
                    end_x = self.config.GRID_PADDING + anim['end_idx'] * (self.config.CELL_SIZE + self.config.CELL_MARGIN)
                    y = self.config.GRID_PADDING + row * (self.config.CELL_SIZE + self.config.CELL_MARGIN)
                    current_x = start_x + (end_x - start_x) * t
                    current_y = y
                else:
                    col = anim['col']
                    start_y = self.config.GRID_PADDING + anim['start_idx'] * (self.config.CELL_SIZE + self.config.CELL_MARGIN)
                    end_y = self.config.GRID_PADDING + anim['end_idx'] * (self.config.CELL_SIZE + self.config.CELL_MARGIN)
                    x = self.config.GRID_PADDING + col * (self.config.CELL_SIZE + self.config.CELL_MARGIN)
                    current_y = start_y + (end_y - start_y) * t
                    current_x = x
                
                # Zeichne die animierte Kachel
                pygame.draw.rect(screen, self.config.TILE_COLORS.get(anim['value'], self.config.TILE_COLORS[2048]),
                                 (current_x, current_y, self.config.CELL_SIZE, self.config.CELL_SIZE), 0, 5)
                
                # Zeichne den Text
                if anim['value'] < 10:
                    f = self.config.font['large']
                elif anim['value'] < 100:
                    f = self.config.font['medium']
                elif anim['value'] < 1000:
                    f = self.config.font['small']
                else:
                    f = self.config.font['extra_small']
                    
                text = f.render(str(anim['value']), True, self.config.TEXT_COLORS.get(anim['value'], self.config.FONT_COLOR))
                text_rect = text.get_rect(center=(current_x + self.config.CELL_SIZE // 2, current_y + self.config.CELL_SIZE // 2))
                screen.blit(text, text_rect)

        # Zeichne Spawn-Animationen
        for (i, j), anim_time in self.spawn_animations.items():
            value = self.grid[i][j]
            x = self.config.GRID_PADDING + j * (self.config.CELL_SIZE + self.config.CELL_MARGIN)
            y = self.config.GRID_PADDING + i * (self.config.CELL_SIZE + self.config.CELL_MARGIN)
            scale = min(anim_time / self.config.SPAWN_ANIMATION_DURATION, 1.0)
            scaled_size = int(self.config.CELL_SIZE * scale)
            offset = (self.config.CELL_SIZE - scaled_size) // 2
            rect = (x + offset, y + offset, scaled_size, scaled_size)
            pygame.draw.rect(screen, self.config.TILE_COLORS.get(value, self.config.TILE_COLORS[2048]),
                             rect, 0, 5)
                             
            if scale >= 0.5:  # Text erst anzeigen, wenn Kachel groß genug
                if value < 10:
                    f = self.config.font['large']
                elif value < 100:
                    f = self.config.font['medium']
                elif value < 1000:
                    f = self.config.font['small']
                else:
                    f = self.config.font['extra_small']
                    
                text = f.render(str(value), True, self.config.TEXT_COLORS.get(value, self.config.FONT_COLOR))
                text_rect = text.get_rect(center=(x + self.config.CELL_SIZE // 2, y + self.config.CELL_SIZE // 2))
                
                # Skaliere Textgröße mit der Animation
                text_scale = min(1.0, (scale - 0.5) * 2)  # 0.5 -> 0, 1.0 -> 1.0
                if text_scale > 0:
                    scaled_text = pygame.transform.scale(
                        text, 
                        (int(text.get_width() * text_scale), 
                         int(text.get_height() * text_scale))
                    )
                    scaled_rect = scaled_text.get_rect(center=(x + self.config.CELL_SIZE // 2, y + self.config.CELL_SIZE // 2))
                    screen.blit(scaled_text, scaled_rect)
        
        # Zeichne Statistikbereich
        pygame.draw.rect(screen, (187, 173, 160), 
                         (0, self.config.WINDOW_HEIGHT - 50, self.config.WINDOW_WIDTH, 50))
        
        # Zeige Punktzahl und Highscore
        score_text = self.config.font['small'].render(f"Score: {self.score}", True, self.config.TEXT_COLOR_BRIGHT)
        high_score_text = self.config.font['small'].render(f"Best: {self.high_score}", True, self.config.TEXT_COLOR_BRIGHT)
        best_tile_text = self.config.font['extra_small'].render(f"Best Tile: {self.best_tile}", True, self.config.TEXT_COLOR_BRIGHT)
        
        screen.blit(score_text, (10, self.config.WINDOW_HEIGHT - 45))
        screen.blit(high_score_text, (self.config.WINDOW_WIDTH - high_score_text.get_width() - 10, self.config.WINDOW_HEIGHT - 45))
        screen.blit(best_tile_text, (self.config.WINDOW_WIDTH // 2 - best_tile_text.get_width() // 2, self.config.WINDOW_HEIGHT - 35))
        
        # Zeichne Win-Bildschirm
        if self.game_won and not self.continue_after_win:
            overlay = pygame.Surface((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 180))
            screen.blit(overlay, (0, 0))
            
            win_text = self.config.font['large'].render("You Win!", True, (119, 110, 101))
            continue_text = self.config.font['medium'].render("Drücke C zum Weiterspielen", True, (119, 110, 101))
            restart_text = self.config.font['medium'].render("Drücke R zum Neustart", True, (119, 110, 101))
            
            screen.blit(win_text, (self.config.WINDOW_WIDTH // 2 - win_text.get_width() // 2, 
                                  self.config.WINDOW_HEIGHT // 2 - win_text.get_height() // 2 - 60))
            screen.blit(continue_text, (self.config.WINDOW_WIDTH // 2 - continue_text.get_width() // 2, 
                                      self.config.WINDOW_HEIGHT // 2 - continue_text.get_height() // 2))
            screen.blit(restart_text, (self.config.WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 
                                     self.config.WINDOW_HEIGHT // 2 - restart_text.get_height() // 2 + 60))
        
        # Zeichne Game Over-Bildschirm
        elif self.game_over:
            overlay = pygame.Surface((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 180))
            screen.blit(overlay, (0, 0))
            
            go_text = self.config.font['large'].render("Game Over", True, (119, 110, 101))
            retry_text = self.config.font['medium'].render("Drücke R zum Neustart", True, (119, 110, 101))
            final_score_text = self.config.font['medium'].render(f"Score: {self.score}", True, (119, 110, 101))
            
            screen.blit(go_text, (self.config.WINDOW_WIDTH // 2 - go_text.get_width() // 2, 
                                 self.config.WINDOW_HEIGHT // 2 - go_text.get_height() // 2 - 60))
            screen.blit(final_score_text, (self.config.WINDOW_WIDTH // 2 - final_score_text.get_width() // 2, 
                                         self.config.WINDOW_HEIGHT // 2 - final_score_text.get_height() // 2))
            screen.blit(retry_text, (self.config.WINDOW_WIDTH // 2 - retry_text.get_width() // 2, 
                                   self.config.WINDOW_HEIGHT // 2 - retry_text.get_height() // 2 + 60))
            
            
    def auto_move(self):
        """Wählt eine Richtung basierend auf der Strategie aus."""
        
        # Überprüfen, ob die rechte Spalte vollständig gefüllt ist
        right_column_full = all(self.grid[i][self.config.GRID_SIZE - 1] != 0 for i in range(self.config.GRID_SIZE))
        
        # Bevorzugte Richtung: Rechts
        if self.move(1):  # Rechts (1)
            return
        
        # Zweite Wahl: Nach unten (wenn die rechte Spalte voll ist)
        if right_column_full and self.move(2):  # Unten (2)
            return
        
        # Falls Rechts und Unten nicht möglich sind, Notfallstrategie:
        if self.move(0):  # Hoch (0)
            return
        
        if self.move(3):  # Links (3) als letzter Ausweg
            return
        
    def auto_ai_move(self):
        """Lässt die KI das Spiel spielen."""
        old_state = self.ai.get_state(self.grid)
        action = self.ai.choose_action(self)
        moved = self.move(action)

        if moved:
            reward = self.score  # Belohnung = aktuelle Punktzahl
            new_state = self.ai.get_state(self.grid)
            self.ai.update_q_table(old_state, action, reward, new_state)
            self.ai.decay_exploration()  # Exploration reduzieren