package com.guesstheword.game;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface WordRepository extends JpaRepository<Word, Long> {
    boolean existsByWord(String word);
}
