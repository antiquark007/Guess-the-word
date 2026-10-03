package com.guesstheword.game;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.LocalDateTime;

@Entity
@Table(name = "games")
public class Game {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private Long userId;
    private Long wordId;
    private LocalDateTime startedAt = LocalDateTime.now();
    private LocalDateTime completedAt;
    private String status = "IN_PROGRESS";
    private int numberOfGuesses;

    protected Game() {
    }

    public Game(Long userId, Long wordId) {
        this.userId = userId;
        this.wordId = wordId;
    }

    public Long getId() { return id; }
    public Long getUserId() { return userId; }
    public Long getWordId() { return wordId; }
    public LocalDateTime getStartedAt() { return startedAt; }
    public LocalDateTime getCompletedAt() { return completedAt; }
    public String getStatus() { return status; }
    public int getNumberOfGuesses() { return numberOfGuesses; }
    public void setNumberOfGuesses(int numberOfGuesses) { this.numberOfGuesses = numberOfGuesses; }
    public void setStatus(String status) { this.status = status; }
    public void setCompletedAt(LocalDateTime completedAt) { this.completedAt = completedAt; }
}
