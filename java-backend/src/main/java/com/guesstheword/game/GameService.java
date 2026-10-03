package com.guesstheword.game;

import com.guesstheword.user.User;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

@Service
public class GameService {
    private static final int MAX_GAMES_PER_DAY = 3;
    private static final int MAX_GUESSES_PER_GAME = 5;
    private final GameRepository games;
    private final WordRepository words;
    private final GuessRepository guesses;
    private final Random random = new Random();

    public GameService(GameRepository games, WordRepository words, GuessRepository guesses) {
        this.games = games;
        this.words = words;
        this.guesses = guesses;
    }

    public Game start(User user) {
        LocalDateTime start = LocalDate.now().atStartOfDay();
        LocalDateTime end = start.plusDays(1);
        if (games.countByUserIdAndStartedAtGreaterThanEqualAndStartedAtLessThan(user.getId(), start, end)
                >= MAX_GAMES_PER_DAY) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "You can play only 3 games per day.");
        }
        List<Word> availableWords = words.findAll();
        if (availableWords.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "No words available.");
        }
        return games.save(new Game(user.getId(), availableWords.get(random.nextInt(availableWords.size())).getId()));
    }

    public Map<String, Object> submit(Long gameId, User user, String guess) {
        Game game = games.findById(gameId)
                .filter(value -> value.getUserId().equals(user.getId()))
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Game not found."));
        if (!game.getStatus().equals("IN_PROGRESS")) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "This game is already completed.");
        }
        if (guess.length() != 5 || !guess.matches("[A-Z]{5}")) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Guess must contain exactly 5 uppercase letters.");
        }
        if (game.getNumberOfGuesses() >= MAX_GUESSES_PER_GAME) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Maximum 5 guesses allowed.");
        }
        String target = words.findById(game.getWordId()).orElseThrow().getWord();
        int guessNumber = game.getNumberOfGuesses() + 1;
        guesses.save(new Guess(game.getId(), guess, guessNumber));
        game.setNumberOfGuesses(guessNumber);
        boolean won = guess.equals(target);
        if (won) {
            game.setStatus("WON");
            game.setCompletedAt(LocalDateTime.now());
        } else if (guessNumber >= MAX_GUESSES_PER_GAME) {
            game.setStatus("LOST");
            game.setCompletedAt(LocalDateTime.now());
        }
        games.save(game);
        Map<String, Object> response = new HashMap<>();
        response.put("game_id", game.getId());
        response.put("guess", guess);
        response.put("result", evaluate(target, guess));
        response.put("guess_number", guessNumber);
        response.put("status", game.getStatus());
        response.put("message", won ? "Congratulations!" : game.getStatus().equals("LOST") ? "Better luck next time!" : "Keep guessing!");
        return response;
    }

    private List<String> evaluate(String target, String guess) {
        List<String> result = new ArrayList<>(List.of("GREY", "GREY", "GREY", "GREY", "GREY"));
        Map<Character, Integer> remaining = new HashMap<>();
        for (int index = 0; index < 5; index++) {
            if (guess.charAt(index) == target.charAt(index)) {
                result.set(index, "GREEN");
            } else {
                remaining.merge(target.charAt(index), 1, Integer::sum);
            }
        }
        for (int index = 0; index < 5; index++) {
            if (result.get(index).equals("GREEN")) continue;
            char letter = guess.charAt(index);
            int count = remaining.getOrDefault(letter, 0);
            if (count > 0) {
                result.set(index, "ORANGE");
                remaining.put(letter, count - 1);
            }
        }
        return result;
    }
}
