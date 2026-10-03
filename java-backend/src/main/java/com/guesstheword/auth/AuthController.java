package com.guesstheword.auth;

import com.guesstheword.user.User;
import com.guesstheword.user.UserRepository;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.regex.Pattern;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/api")
public class AuthController {
    private static final Pattern USERNAME = Pattern.compile("^(?=.*[a-z])(?=.*[A-Z]).{5,}$");
    private static final Pattern PASSWORD = Pattern.compile("^(?=.*[A-Za-z])(?=.*\\d)(?=.*[$%*\\)]).{5,}$");

    private final UserRepository users;
    private final PasswordEncoder passwordEncoder;

    public AuthController(UserRepository users, PasswordEncoder passwordEncoder) {
        this.users = users;
        this.passwordEncoder = passwordEncoder;
    }

    @PostMapping("/register")
    public ResponseEntity<Map<String, String>> register(
            @RequestParam String username,
            @RequestParam String password,
            @RequestParam(defaultValue = "PLAYER") String role) {
        username = decodeQueryValue(username);
        password = decodeQueryValue(password);
        role = decodeQueryValue(role);
        role = role.toUpperCase();
        if (!role.equals("PLAYER") && !role.equals("ADMIN")) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Role must be PLAYER or ADMIN.");
        }
        if (!USERNAME.matcher(username).matches()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "Username must contain at least 5 letters and include uppercase and lowercase letters.");
        }
        if (!PASSWORD.matcher(password).matches()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "Password must be at least 5 characters and contain letters, numbers and $, %, *, or ).");
        }
        if (users.findByUsername(username).isPresent()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Username already exists");
        }
        users.save(new User(username, passwordEncoder.encode(password), role));
        return ResponseEntity.ok(Map.of("message", "Registration successful", "username", username));
    }

    @PostMapping("/login")
    public Map<String, String> login(@RequestParam String username, @RequestParam String password) {
        final String decodedUsername = decodeQueryValue(username);
        final String decodedPassword = decodeQueryValue(password);
        User user = users.findByUsername(decodedUsername)
            .filter(value -> passwordEncoder.matches(decodedPassword, value.getPasswordHash()))
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid username or password"));
        return Map.of("access_token", "java-session-" + user.getId(), "token_type", "bearer",
                "username", user.getUsername(), "role", user.getRole());
    }

    private String decodeQueryValue(String value) {
        return URLDecoder.decode(value, StandardCharsets.UTF_8);
    }

}