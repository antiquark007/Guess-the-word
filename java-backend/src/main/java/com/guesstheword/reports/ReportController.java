package com.guesstheword.reports;

import com.guesstheword.game.Game;
import com.guesstheword.game.GameRepository;
import com.guesstheword.user.User;
import com.guesstheword.user.UserRepository;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/api/admin/report")
public class ReportController {
    private final GameRepository games;
    private final UserRepository users;

    public ReportController(GameRepository games, UserRepository users) {
        this.games = games;
        this.users = users;
    }

    @GetMapping("/day")
    public Map<String, Object> day(@RequestParam LocalDate report_date, @RequestHeader("Authorization") String authorization) {
        requireAdmin(authorization);
        LocalDateTime start = report_date.atStartOfDay();
        List<Game> matches = games.findByStartedAtGreaterThanEqualAndStartedAtLessThan(start, start.plusDays(1));
        long usersCount = matches.stream().map(Game::getUserId).distinct().count();
        long wins = matches.stream().filter(game -> game.getStatus().equals("WON")).count();
        return Map.of("date", report_date.toString(), "number_of_users", usersCount, "number_of_correct_guesses", wins);
    }

    @GetMapping("/user/{userId}")
    public List<Map<String, Object>> user(@PathVariable Long userId, @RequestHeader("Authorization") String authorization) {
        requireAdmin(authorization);
        Map<LocalDate, long[]> totals = new LinkedHashMap<>();
        for (Game game : games.findByUserIdOrderByStartedAtDesc(userId)) {
            LocalDate date = game.getStartedAt().toLocalDate();
            long[] values = totals.computeIfAbsent(date, ignored -> new long[2]);
            values[0]++;
            if (game.getStatus().equals("WON")) values[1]++;
        }
        List<Map<String, Object>> response = new ArrayList<>();
        totals.forEach((date, values) -> response.add(Map.of("date", date.toString(), "words_tried", values[0], "correct_guesses", values[1])));
        return response;
    }

    private void requireAdmin(String authorization) {
        if (authorization == null || !authorization.startsWith("Bearer java-session-")) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid authentication credentials");
        }
        try {
            Long id = Long.parseLong(authorization.substring("Bearer java-session-".length()));
            User user = users.findById(id).orElseThrow();
            if (!user.getRole().equals("ADMIN")) throw new ResponseStatusException(HttpStatus.FORBIDDEN, "Admin access required");
        } catch (ResponseStatusException exception) {
            throw exception;
        } catch (RuntimeException exception) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid authentication credentials");
        }
    }
}
