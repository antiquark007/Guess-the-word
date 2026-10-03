package com.guesstheword.game;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.LocalDateTime;

@Entity
@Table(name = "guesses")
public class Guess {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private Long gameId;
    private String guessedWord;
    private int guessNumber;
    private LocalDateTime guessedAt = LocalDateTime.now();

    protected Guess() {
    }

    public Guess(Long gameId, String guessedWord, int guessNumber) {
        this.gameId = gameId;
        this.guessedWord = guessedWord;
        this.guessNumber = guessNumber;
    }
}
