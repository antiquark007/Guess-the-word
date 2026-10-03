package com.guesstheword.game;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;

@Component
public class WordSeeder {
    private static final String[] WORDS = {"APPLE", "HOUSE", "MOUSE", "TIGER", "WATER", "WORLD", "PLANT", "TRAIN", "CHAIR", "LIGHT", "STONE", "CLOUD", "BRAIN", "GREEN", "BLACK", "SMILE", "DREAM", "RIVER", "MUSIC", "POWER"};
    private final WordRepository words;

    public WordSeeder(WordRepository words) {
        this.words = words;
    }

    @PostConstruct
    void seed() {
        for (String word : WORDS) {
            if (!words.existsByWord(word)) words.save(new Word(word));
        }
    }
}
