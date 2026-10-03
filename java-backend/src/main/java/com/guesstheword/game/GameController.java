package com.guesstheword.game;

import com.guesstheword.user.User;
import com.guesstheword.user.UserRepository;
import java.util.Map;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;

@RestController
@RequestMapping("/api/game")
public class GameController {
    private final GameService gameService;
    private final UserRepository users;

    public GameController(GameService gameService, UserRepository users) {
        this.gameService = gameService;
        this.users = users;
    }

    @PostMapping("/start")
    public Map<String, Object> start(@RequestHeader("Authorization") String authorization) {
        User user = currentUser(authorization);
        Game game = gameService.start(user);
        return Map.of("game_id", game.getId(), "message", "Game started");
    }

    @PostMapping("/{gameId}/guess")
    public Map<String, Object> guess(@PathVariable Long gameId, @RequestParam String guess,
                                     @RequestHeader("Authorization") String authorization) {
        return gameService.submit(gameId, currentUser(authorization), guess);
    }

    private User currentUser(String authorization) {
        if (authorization == null || !authorization.startsWith("Bearer java-session-")) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid authentication credentials");
        }
        try {
            Long id = Long.parseLong(authorization.substring("Bearer java-session-".length()));
            return users.findById(id).orElseThrow();
        } catch (RuntimeException exception) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid authentication credentials");
        }
    }
}
