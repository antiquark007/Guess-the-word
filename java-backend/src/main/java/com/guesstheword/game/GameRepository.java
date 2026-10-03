package com.guesstheword.game;

import java.time.LocalDateTime;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface GameRepository extends JpaRepository<Game, Long> {
    long countByUserIdAndStartedAtGreaterThanEqualAndStartedAtLessThan(Long userId, LocalDateTime start, LocalDateTime end);
    List<Game> findByUserIdOrderByStartedAtDesc(Long userId);
    List<Game> findByStartedAtGreaterThanEqualAndStartedAtLessThan(LocalDateTime start, LocalDateTime end);
}
